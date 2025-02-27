import re
from datetime import datetime
from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel

from bigdata_client.exceptions import BigdataClientError
from bigdata_client.models.chat import Chat
from bigdata_client.models.chat import ChatInteraction as ChatInteractionModel


class CamelModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class ChatInteractionTextResponseBlock(CamelModel):
    type: Literal["TEXT"]
    value: str


class ChatInteractionEngineResponseBlock(CamelModel):
    type: Literal["ENGINE"]
    answer: str


class ChatInteraction(CamelModel):

    input_message: str
    response_block: Union[
        ChatInteractionTextResponseBlock, ChatInteractionEngineResponseBlock
    ]
    interaction_timestamp: str
    date_created: datetime
    last_updated: datetime

    def to_chat_interaction(self):
        if self.response_block.type == "TEXT":
            answer = self._strip_references(self.response_block.value)
            return ChatInteractionModel(
                question=self.input_message,
                answer=answer,
                interaction_timestamp=self.interaction_timestamp,
                date_created=self.date_created,
                last_updated=self.last_updated,
            )
        elif self.response_block.type == "ENGINE":
            answer = self._strip_references(self.response_block.answer)
            return ChatInteractionModel(
                question=self.input_message,
                answer=answer,
                interaction_timestamp=self.interaction_timestamp,
                date_created=self.date_created,
                last_updated=self.last_updated,
            )
        else:
            raise BigdataClientError(
                f"Unknown response block type: {self.response_block.type}"
            )

    @staticmethod
    def _strip_references(text):
        return re.sub(r"`:ref\[.*?\]`", "", text)


class ChatResponse(CamelModel):

    id: str
    name: str
    user_id: str
    date_created: datetime
    last_updated: datetime
    interactions: list[ChatInteraction]

    def to_chat_model(self, api_connection):
        return Chat(
            id=self.id,
            name=self.name,
            user_id=self.user_id,
            date_created=self.date_created,
            last_updated=self.last_updated,
            _interactions=[x.to_chat_interaction() for x in self.interactions],
            _api_connection=api_connection,
            _loaded=True,
        )


class GetChatListResponseItem(CamelModel):

    id: str
    name: str
    user_id: str
    date_created: datetime
    last_updated: datetime

    def to_chat_model(self, api_connection):
        return Chat(
            id=self.id,
            name=self.name,
            user_id=self.user_id,
            date_created=self.date_created,
            last_updated=self.last_updated,
            _interactions=[],
            _api_connection=api_connection,
            _loaded=False,
        )


class GetChatListResponse(CamelModel):
    root: list[GetChatListResponseItem]

    def to_chat_list(self, api_connection):
        return [x.to_chat_model(api_connection) for x in self.root]


class CreateNewChat(CamelModel):
    name: str = Field(min_length=1)


class ChatWSCompleteResponse(CamelModel):
    type: Literal["COMPLETE"]
    interaction_timestamp: str
    content_block: dict


class ChatAskRequest(CamelModel):

    request_id: str = ""  # Required, not used
    action: Literal["ChatWithMemoryRequest"] = "ChatWithMemoryRequest"
    chat_id: str
    input_message: str
    interaction_type: Literal["user_message"] = "user_message"
