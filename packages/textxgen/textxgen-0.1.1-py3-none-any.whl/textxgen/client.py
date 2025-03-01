# textxgen/client.py

# textxgen/client.py

import json
import requests
from typing import Iterator, Dict, Any
from .config import Config
from .exceptions import APIError, InvalidInputError


class APIClient:
    """
    Handles API requests to OpenRouter.
    """

    def __init__(self):
        self.base_url = Config.BASE_URL
        self.headers = Config.HEADERS

    def _make_request(self, endpoint: str, method: str = "POST", data: dict = None, stream: bool = False) -> Any:
        """
        Makes an API request to OpenRouter.

        Args:
            endpoint (str): API endpoint (e.g., "/chat/completions").
            method (str): HTTP method (default: "POST").
            data (dict): Request payload.
            stream (bool): Whether to stream the response (default: False).

        Returns:
            Union[dict, Iterator[dict]]: API response or a generator for streaming.

        Raises:
            APIError: If the API request fails.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, json=data, stream=stream)
            response.raise_for_status()

            if stream:
                return self._handle_streaming_response(response)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(str(e), getattr(e.response, "status_code", None))

    def _handle_streaming_response(self, response: requests.Response) -> Iterator[Dict[str, Any]]:
        """
        Handles streaming responses from the API in SSE format.

        Args:
            response (requests.Response): The streaming response.

        Yields:
            dict: A chunk of the streaming response.

        Raises:
            APIError: If the streaming response cannot be decoded.
        """
        buffer = ""
        for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
            buffer += chunk
            while True:
                # Find the next complete SSE line
                line_end = buffer.find('\n')
                if line_end == -1:
                    break

                # Extract the line and remove it from the buffer
                line = buffer[:line_end].strip()
                buffer = buffer[line_end + 1:]

                # Skip empty lines and comments
                if not line or line.startswith(':'):
                    continue

                # Handle SSE data lines
                if line.startswith('data: '):
                    data = line[6:].strip()
                    if data == '[DONE]':
                        return  # End of stream

                    try:
                        # Parse the JSON data
                        data_obj = json.loads(data)
                        yield data_obj
                    except json.JSONDecodeError as e:
                        raise APIError(f"Failed to decode streaming response: {str(e)}")
                else:
                    # Handle unexpected lines
                    raise APIError(f"Unexpected streaming response: {line}")

    def chat_completion(self, messages: list, model: str = None, stream: bool = False) -> Any:
        """
        Sends a chat completion request to OpenRouter.

        Args:
            messages (list): List of messages for the chat.
            model (str): Model name (default: Config.DEFAULT_MODEL).
            stream (bool): Whether to stream the response (default: False).

        Returns:
            Union[dict, Iterator[dict]]: API response or a generator for streaming.

        Raises:
            InvalidInputError: If messages are not provided or are invalid.
        """
        if not messages or not isinstance(messages, list):
            raise InvalidInputError("Messages must be a non-empty list.")

        payload = {
            "model": model or Config.DEFAULT_MODEL,
            "messages": messages,
            "stream": stream,
        }
        return self._make_request("/chat/completions", data=payload, stream=stream)





