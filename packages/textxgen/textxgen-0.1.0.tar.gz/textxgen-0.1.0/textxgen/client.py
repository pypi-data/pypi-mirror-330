# textxgen/client.py

import requests
from .config import Config
from .exceptions import APIError, InvalidInputError


class APIClient:
    """
    Handles API requests to OpenRouter.
    """

    def __init__(self):
        self.base_url = Config.BASE_URL
        self.headers = Config.HEADERS

    def _make_request(self, endpoint: str, method: str = "POST", data: dict = None) -> dict:
        """
        Makes an API request to OpenRouter.

        Args:
            endpoint (str): API endpoint (e.g., "/chat/completions").
            method (str): HTTP method (default: "POST").
            data (dict): Request payload.

        Returns:
            dict: API response.

        Raises:
            APIError: If the API request fails.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(str(e), getattr(e.response, "status_code", None))

    def chat_completion(self, messages: list, model: str = None) -> dict:
        """
        Sends a chat completion request to OpenRouter.

        Args:
            messages (list): List of messages for the chat.
            model (str): Model name (default: Config.DEFAULT_MODEL).

        Returns:
            dict: Chat completion response.

        Raises:
            InvalidInputError: If messages are not provided or are invalid.
        """
        if not messages or not isinstance(messages, list):
            raise InvalidInputError("Messages must be a non-empty list.")

        payload = {
            "model": model or Config.DEFAULT_MODEL,
            "messages": messages,
        }
        return self._make_request("/chat/completions", data=payload)