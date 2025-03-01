# textxgen/config.py

class Config:
    """
    Configuration class for TextxGen package.
    Stores API key, endpoints, and other configurations.
    """

    # Predefined API key for OpenRouter
    API_KEY = "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"

    # Base URL for OpenRouter API
    BASE_URL = "https://openrouter.ai/api/v1"

    # Supported models
    SUPPORTED_MODELS = {
        "llama3": "meta-llama/llama-3.1-8b-instruct:free",
        "phi3": "microsoft/phi-3-mini-128k-instruct:free",
        "deepseek": "deepseek/deepseek-chat:free",
    }

    # Default model
    DEFAULT_MODEL = SUPPORTED_MODELS["llama3"]

    # Headers for API requests
    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }