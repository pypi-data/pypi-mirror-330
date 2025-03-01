# textxgen/exceptions.py

class TextxGenError(Exception):
    """Base exception class for TextxGen package."""

    pass


class APIError(TextxGenError):
    """Exception raised for API-related errors."""

    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(f"API Error: {message} (Status Code: {status_code})")


class ModelNotSupportedError(TextxGenError):
    """Exception raised when an unsupported model is requested."""

    def __init__(self, model: str):
        self.model = model
        super().__init__(f"Model '{model}' is not supported.")


class InvalidInputError(TextxGenError):
    """Exception raised for invalid input parameters."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Invalid Input: {message}")