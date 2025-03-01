from typing import Optional, Generator
from .__http_client import _HTTPClient
from ..types.agent.requests import AgentCreateRequest, AgentUpdateRequest, AgentDeleteRequest
# from ..types.agent.requests import ChatRequest
from ..types.agent.responses import AgentCreateResponse, AgentGetResponse, AgentListResponse, AgentUpdateResponse, AgentDeleteResponse
# from ..types.chat.responses import ChatResponse
from pydantic import ValidationError
from ..types.shared.enums import ResourcePath


class _Agent:
    """Client for interacting with the AI Library Agent API."""

    # _RESOURCE_PATH = ResourcePath.AGENT
    _RESOURCE_PATH = "/agent"

    def __init__(self, http_client: _HTTPClient):
        self._http_client = http_client


    def _validate_response(self, response: dict, validation_class) -> dict:
        try:
            validation_class(**response)
            return response
        except ValidationError as e:
            raise e


    def create(self, title: str, **kwargs) -> dict:
        """Create a new agent with the specified parameters."""
        payload = AgentCreateRequest(title=title, **kwargs).model_dump()
        response = self._http_client._request("POST", f"{self._RESOURCE_PATH}/create", json=payload)
        return self._validate_response(response, AgentCreateResponse)


    def get(self, namespace: str) -> dict:
        """Retrieve information about an agent."""
        if not isinstance(namespace, str) or not namespace:
            raise ValueError("Namespace must be a non-empty string")
        response = self._http_client._request("GET", f"{self._RESOURCE_PATH}/{namespace}")
        if "status" in response and response["status"] == "failure":
            return response
        return self._validate_response(response, AgentGetResponse)


    def list_agents(self) -> dict:
        """List all agents."""
        response = self._http_client._request("GET", self._RESOURCE_PATH)
        return self._validate_response(response, AgentListResponse)


    def update(self, namespace: str, **kwargs) -> dict:
        """Update an existing agent."""
        payload = AgentUpdateRequest(namespace=namespace, **kwargs).model_dump()
        response = self._http_client._request("PUT", f"{self._RESOURCE_PATH}/{namespace}", json=payload)
        return self._validate_response(response, AgentUpdateResponse)


    def delete(self, namespace: str, delete_connected_resources: bool) -> dict:
        """Delete an agent."""
        payload = AgentDeleteRequest(namespace=namespace, delete_connected_resources=delete_connected_resources).model_dump()
        response = self._http_client._request("DELETE", f"{self._RESOURCE_PATH}/{namespace}", json=payload)
        return self._validate_response(response, AgentDeleteResponse)


    # ### WORK IN PROGRESS ###
    # def chat(self, namespace: str, messages: list[dict], stream: bool = False) -> Generator[str, None, None]:
    #     """Chat with an agent."""
    #     request = ChatRequest(messages=messages)
    #     url = f"{self._http_client.base_url}/v1/agent/{namespace}/chat"
    #     payload = request.model_dump_json()
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'X-Library-Key': self._http_client.headers["X-Library-Key"]
    #     }

    #     with requests.request("POST", url, headers=headers, data=payload, stream=True) as response:
    #         response.raise_for_status()
    #         for chunk in response.iter_content(chunk_size=8192):
    #             if chunk:
    #                 yield chunk.decode('utf-8')
        
