# textxgen/endpoints/completions.py

from ..client import APIClient
from ..models import Models
from ..exceptions import InvalidInputError


class CompletionsEndpoint:
    """
    Handles text completion interactions with OpenRouter models.
    """

    def __init__(self):
        self.client = APIClient()
        self.models = Models()

    def complete(
        self,
        prompt: str,
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 100,
    ) -> dict:
        """
        Sends a text completion request to the OpenRouter API.

        Args:
            prompt (str): The input prompt for text completion.
            model (str): Name of the model to use (default: Config.DEFAULT_MODEL).
            temperature (float): Sampling temperature (default: 0.7).
            max_tokens (int): Maximum number of tokens to generate (default: 100).

        Returns:
            dict: API response containing the text completion.

        Raises:
            InvalidInputError: If the prompt is empty or invalid.
        """
        if not prompt or not isinstance(prompt, str):
            raise InvalidInputError("Prompt must be a non-empty string.")

        # Prepare the payload
        payload = {
            "model": self.models.get_model(model) if model else Models().list_models()["llama3"],
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        # Send the request
        return self.client._make_request("/completions", data=payload)