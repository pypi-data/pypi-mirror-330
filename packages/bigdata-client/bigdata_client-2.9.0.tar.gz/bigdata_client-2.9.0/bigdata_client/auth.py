from __future__ import annotations

import asyncio
import json
import os
import ssl
import threading
import warnings
from functools import wraps
from http import HTTPStatus
from typing import Optional, Union
from urllib.parse import urlparse

import aiohttp
import nest_asyncio
import requests
from pydantic import BaseModel
from websockets import InvalidStatus
from websockets.sync.client import connect

from bigdata_client.clerk.constants import ClerkInstanceType
from bigdata_client.clerk.exceptions import (
    ClerkAuthError,
    ClerkAuthUnsupportedError,
    ClerkInvalidCredentialsError,
    ClerkTooManySignInAttemptsError,
    ClerkUnexpectedSignInParametersError,
)
from bigdata_client.clerk.models import SignInStrategyType
from bigdata_client.clerk.token_manager import ClerkTokenManager
from bigdata_client.clerk.token_manager_factory import token_manager_factory
from bigdata_client.constants import DEPRECATED_WARNING_AUTOSUGGEST
from bigdata_client.exceptions import (
    BigdataClientAuthFlowError,
    BigdataClientError,
    BigdataClientTooManySignInAttemptsError,
)
from bigdata_client.settings import settings
from bigdata_client.user_agent import get_user_agent

nest_asyncio.apply()  # Required for running asyncio in notebooks
THREAD_WAIT_TIMEOUT = 100


class AsyncRequestContext(BaseModel):
    """
    Context used to pass information to auth module for making async requests.
    Async requests are made in parallel, so each request is associated with an id to
    retrieve it from a list of responses.
    """

    id: str
    url: str
    params: dict


class AsyncResponseContext(BaseModel):
    """
    Structure used to return the response of an async request.
    Async requests are made in parallel, so each response is associated with the id it was
    used to make the request.
    """

    id: str
    response: dict


class Proxy(BaseModel):
    protocol: str = "https"
    url: str


def handle_clerk_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ClerkAuthUnsupportedError as e:
            raise BigdataClientAuthFlowError(e)
        except ClerkUnexpectedSignInParametersError as e:
            raise BigdataClientAuthFlowError(e)
        except ClerkInvalidCredentialsError as e:
            raise BigdataClientAuthFlowError(e)
        except ClerkTooManySignInAttemptsError as e:
            raise BigdataClientTooManySignInAttemptsError(e)
        except ClerkAuthError as e:
            raise BigdataClientError(e)

    return wrapper


class Auth:
    """
    Class that performs the authentication logic, and wraps all the http calls
    so that it can handle the token autorefresh when needed.
    """

    def __init__(
        self,
        token_manager: ClerkTokenManager,
        pool_maxsize: int,
        verify: Union[bool, str],
        proxies: Optional[dict] = None,
    ):
        self._session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_maxsize=pool_maxsize)
        self._session.mount("https://", adapter)
        if proxies:
            self._session.proxies.update(proxies)
        self.verify = verify
        self._session.verify = verify
        self._token_manager = TokenManagerWithConcurrency(token_manager)

    @classmethod
    @handle_clerk_exceptions
    def from_username_and_password(
        cls,
        username: str,
        password: str,
        clerk_frontend_url: str,
        clerk_instance_type: ClerkInstanceType,
        pool_maxsize: int,
        proxy: Optional[Proxy],
        verify: Union[bool, str],
    ) -> "Auth":

        proxies = {proxy.protocol: proxy.url} if proxy else None
        # A token manager handles the authentication flow and stores a jwt. It contains methods for refreshing it.
        token_manager = token_manager_factory(
            instance_type=clerk_instance_type,
            sign_in_strategy=SignInStrategyType.PASSWORD,
            clerk_frontend_url=clerk_frontend_url,
            email=username,
            password=password,
            pool_maxsize=pool_maxsize,
            proxies=proxies,
            verify=verify,
        )
        token_manager.refresh_session_token()
        return cls(
            token_manager=token_manager,
            pool_maxsize=pool_maxsize,
            proxies=proxies,
            verify=verify,
        )

    @staticmethod
    def get_headers(url: str, jwt: str, extra_headers: Optional[dict] = None) -> dict:
        # 'https://api.bigdata.com/cqs/query-chunks' -> 'https://api.bigdata.com'
        parsed_url = urlparse(url)
        url_no_path = f"{parsed_url.scheme}://{parsed_url.netloc}"
        headers = {
            "origin": url_no_path,
            "referer": url_no_path,
            # if "content-type" not in headers:
            # We may have to conditionally set the content type when uploading files
            "content-type": "application/json",
            "accept": "application/json",
            "user-agent": get_user_agent(settings.PACKAGE_NAME),
            "Authorization": f"Bearer {jwt}",
        }

        return {**headers, **(extra_headers or {})}

    @handle_clerk_exceptions
    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        json=None,
        stream=None,
    ):
        """Makes an HTTP request, handling the token refresh if needed"""
        # Wait until token is valid - do not make requests if token was marked as invalid/expired.
        self._token_manager.wait(timeout=THREAD_WAIT_TIMEOUT)
        token_used = self._token_manager.get_session_token()

        headers = self.get_headers(url=url, jwt=token_used, extra_headers=headers)

        # The request method has other arguments but we are not using them currently
        response = self._session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            json=json,
            stream=stream,
        )
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            self._token_manager.refresh_jwt(token_used)

            # This headers.copy() is needed for testing. Mock lib does not make a copy, instead it points to
            # the original headers, so asserting that the headers changed fails.
            headers = headers.copy()
            headers["Authorization"] = (
                f"Bearer {self._token_manager.get_session_token()}"
            )

            # Retry the request
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
                json=json,
                stream=stream,
            )

        return response

    @handle_clerk_exceptions
    def async_requests(
        self, method: str, request_contexts: list[AsyncRequestContext]
    ) -> list[AsyncResponseContext]:
        """Makes an async HTTP request, handling the token refresh if needed"""
        # 'https://api.bigdata.com/cqs/query-chunks' -> 'https://api.bigdata.com'
        if any(
            request_context.url != request_contexts[0].url
            for request_context in request_contexts
        ):
            raise ValueError(
                "All requests must have the same URL sice with the current logic origin/referer are "
                "shared across all requests."
            )
        parsed_url = urlparse(request_contexts[0].url)
        url_no_path = f"{parsed_url.scheme}://{parsed_url.netloc}"
        token_used = self._token_manager.get_session_token()
        headers = {
            "origin": url_no_path,
            "referer": url_no_path,
            "content-type": "application/json",
            "accept": "application/json",
            "user-agent": get_user_agent(settings.PACKAGE_NAME),
            "Authorization": f"Bearer {token_used}",
        }

        try:
            return asyncio.run(
                self._create_and_resolve_tasks(method, headers, request_contexts)
            )
        # If any request raises HTTPStatus.UNAUTHORIZED refresh the token and use it again for all of the requests
        except aiohttp.client_exceptions.ClientResponseError as err:
            if err.status != HTTPStatus.UNAUTHORIZED:
                raise

            # This headers.copy() is needed for testing. Mock lib does not make a copy, instead it points to
            # the original headers, so asserting that the headers changed fails.
            self._token_manager.refresh_jwt(token_used)
            headers = headers.copy()
            headers["Authorization"] = (
                f"Bearer {self._token_manager.get_session_token()}"
            )

            try:
                return asyncio.run(
                    self._create_and_resolve_tasks(method, headers, request_contexts)
                )
            except aiohttp.client_exceptions.ClientResponseError as err:
                if err.status == HTTPStatus.UNAUTHORIZED:
                    warnings.warn(DEPRECATED_WARNING_AUTOSUGGEST)
                raise

    async def _create_and_resolve_tasks(
        self, method: str, headers: dict, requests_contexts: list[AsyncRequestContext]
    ) -> list[AsyncResponseContext]:
        ssl_verification = self.verify
        if isinstance(self.verify, str):
            ssl_context = ssl.create_default_context()
            ssl_context.load_cert_chain(
                certfile=self.verify, keyfile=None, password=None
            )
            ssl_verification = ssl_context
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.ensure_future(
                    self._make_async_request(
                        method,
                        headers,
                        session,
                        request_context,
                        ssl_verification=ssl_verification,
                    )
                )
                for request_context in requests_contexts
            ]
            return await asyncio.gather(*tasks)

    async def _make_async_request(
        self,
        method: str,
        headers: dict,
        session: aiohttp.ClientSession,
        request_context: AsyncRequestContext,
        ssl_verification: Union[bool, ssl.SSLContext],
    ) -> AsyncResponseContext:

        target_scheme = urlparse(request_context.url).scheme

        proxy = (
            os.environ.get("ALL_PROXY")
            or os.environ.get(f"{target_scheme.upper()}_PROXY")
            or self._session.proxies.get(target_scheme)
        )

        async with session.request(
            method=method,
            headers=headers,
            params=request_context.params,
            url=request_context.url,
            raise_for_status=True,
            proxy=proxy,
            ssl=ssl_verification,
        ) as response:
            response = await response.json()

        return AsyncResponseContext(id=request_context.id, response=response)

    def get_ws_auth(self, ws_url: str) -> "WSAuth":
        return WSAuth(url=ws_url, token_manager=self._token_manager)


class WSAuth:
    """Use as a context manager"""

    def __init__(self, url: str, token_manager: TokenManagerWithConcurrency):
        self.url = url
        self.token_manager = token_manager

    def send(self, msg: dict):
        self.ws.send(json.dumps(msg))

    def recv(self) -> dict:
        response = self.ws.recv()
        return json.loads(response)

    def __enter__(self):
        token_used = self.token_manager.get_session_token()
        url_with_jwt = f"{self.url}?jwt_token={token_used}"
        try:
            self.ws = connect(url_with_jwt).__enter__()
        except InvalidStatus as e:
            if e.response.status_code == HTTPStatus.UNAUTHORIZED:
                self.token_manager.refresh_jwt(token_used)
                self.url_with_jwt = (
                    f"{self.url}?jwt_token={self.token_manager.get_session_token()}"
                )
                self.ws = connect(self.url_with_jwt).__enter__()
            else:
                raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ws.__exit__(exc_type, exc_val, exc_tb)


class TokenManagerWithConcurrency:
    """
    It checks if the token used must be refreshed by the thread and refreshes it if needed.
    """

    def __init__(self, token_manager: ClerkTokenManager):
        self.token_manager = token_manager
        self.lock = threading.Lock()
        self.event = threading.Event()
        self.event.set()  # So it starts unblocked

    def refresh_jwt(self, token_used: str):
        """
        Only one thread can refresh the token:
            - that is the thread that enters the block while event.is_set()
            - and the used token is the same as the current token
        """
        with self.lock:
            refresh_jwt = (
                self.event.is_set()
                and token_used == self.token_manager.get_session_token()
            )
            if refresh_jwt:
                self.event.clear()

        if refresh_jwt:
            self.token_manager.refresh_session_token()
            self.event.set()
        else:
            self.event.wait(timeout=THREAD_WAIT_TIMEOUT)

    def wait(self, timeout: int):
        self.event.wait(timeout=timeout)

    def get_session_token(self):
        return self.token_manager.get_session_token()
