import os
import warnings
from typing import Optional, Union

from bigdata_client.auth import Auth, Proxy
from bigdata_client.connection import BigdataConnection, UploadsConnection
from bigdata_client.jwt_utils import get_token_claim
from bigdata_client.services.chat_service import ChatService
from bigdata_client.services.content_search import ContentSearch
from bigdata_client.services.knowledge_graph import KnowledgeGraph
from bigdata_client.services.subscription import Subscription
from bigdata_client.services.uploads import Uploads
from bigdata_client.services.watchlists import Watchlists
from bigdata_client.settings import settings

JWT_CLAIM_ORGANIZATION_ID = "organization_id"


class Bigdata:
    """
    Represents a connection to RavenPack's Bigdata API.

    :ivar knowledge_graph: Proxy for the knowledge graph search functionality.
    :ivar search: Proxy object for the content search functionality.
    :ivar watchlists: Proxy object for the watchlist functionality.
    :ivar uploads: Proxy object for the internal content functionality.
    :ivar subscription: Proxy object for the subscription functionality.
    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        *,
        bigdata_api_url: Optional[str] = None,
        bigdata_ws_url: Optional[str] = None,
        upload_api_url: Optional[str] = None,
        proxy: Optional[Proxy] = None,
        verify_ssl: Union[bool, str] = True
    ):
        if password is None:
            password = os.environ.get("BIGDATA_PASSWORD")
        if username is None:
            username = os.environ.get("BIGDATA_USERNAME") or os.environ.get(
                "BIGDATA_USER"
            )
            if os.environ.get("BIGDATA_USER"):
                warnings.warn(
                    "BIGDATA_USER is deprecated, use BIGDATA_USERNAME instead",
                    DeprecationWarning,
                    stacklevel=2,
                )
        if username is None or password is None:
            raise ValueError("Username and password must be provided")
        auth = Auth.from_username_and_password(
            username,
            password,
            clerk_frontend_url=str(settings.CLERK_FRONTEND_URL),
            clerk_instance_type=settings.CLERK_INSTANCE_TYPE,
            pool_maxsize=settings.MAX_PARALLEL_REQUESTS,
            proxy=proxy,
            verify=verify_ssl,
        )
        organization_id = get_token_claim(
            token=auth._token_manager.get_session_token(),
            claim=JWT_CLAIM_ORGANIZATION_ID,
        )

        if bigdata_api_url is None:
            bigdata_api_url = str(settings.BACKEND_API_URL)
        if bigdata_ws_url is None:
            bigdata_ws_url = str(settings.BACKEND_WS_API_URL)
        if upload_api_url is None:
            upload_api_url = str(settings.UPLOAD_API_URL)

        self._api = BigdataConnection(auth, bigdata_api_url, bigdata_ws_url)
        self._upload_api = UploadsConnection(
            auth, upload_api_url, organization_id=organization_id
        )

        # Start the different services
        self.knowledge_graph = KnowledgeGraph(self._api)
        self.search = ContentSearch(self._api)
        self.watchlists = Watchlists(self._api)
        self.uploads = Uploads(uploads_api=self._upload_api)
        self.subscription = Subscription(
            api_connection=self._api, uploads_api_connection=self._upload_api
        )
        self.chat = ChatService(api_connection=self._api)
