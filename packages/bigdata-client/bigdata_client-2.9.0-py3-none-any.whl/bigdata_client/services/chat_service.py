from bigdata_client.api.chat import CreateNewChat
from bigdata_client.connection_protocol import BigdataConnectionProtocol
from bigdata_client.models.chat import Chat


class ChatService:
    """For interacting with Chat objects"""

    def __init__(self, api_connection: BigdataConnectionProtocol):
        self._api = api_connection

    def new(self, name: str) -> Chat:
        """Create a new chat"""
        response = self._api.create_chat(CreateNewChat(name=name))
        return response.to_chat_model(self._api)

    def list(self) -> list[Chat]:
        response = self._api.get_all_chats()
        return response.to_chat_list(self._api)

    def get(self, id_: str) -> Chat:
        """Return a Chat by its id"""
        response = self._api.get_chat(id_)
        return response.to_chat_model(self._api)

    def delete(self, id_: str):
        """Delete a Chat by its id"""
        self._api.delete_chat(id_)
