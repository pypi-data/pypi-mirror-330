# TextxGen

**TextxGen** is a Python package that provides a seamless interface to interact with **OpenRouter** models. It supports chat-based conversations and text completions using predefined models. The package is designed to be simple, modular, and easy to use, making it ideal for developers who want to integrate OpenRouter models into their applications.

---

## Features

- **Predefined API Key**: No need to provide your own API key—TextxGen uses a predefined key internally.
- **Supported Models**: Access popular models like:
  - `meta-llama/llama-3.1-8b-instruct:free`
  - `microsoft/phi-3-mini-128k-instruct:free`
  - `deepseek/deepseek-chat:free`
- **Chat and Completions**: Supports both chat-based conversations and text completions.
- **System Prompts**: Add system-level prompts to guide model interactions.
- **Error Handling**: Robust exception handling for API failures, invalid inputs, and network issues.
- **Modular Design**: Easily extendable to support additional models in the future.

---

## Installation

You can install TextxGen using `pip`:

```bash
pip install textxgen
```

## Usage

### 1. Chat Example

Use the `ChatEndpoint` to interact with chat-based models.

```python
from textxgen import ChatEndpoint

# Initialize the ChatEndpoint
chat = ChatEndpoint()

# Define the conversation messages
messages = [
    {"role": "user", "content": "What is the capital of France?"},
]

# Add a system prompt (optional)
system_prompt = "You are a helpful assistant."

# Send the chat request
response = chat.chat(
    messages=messages,
    model="llama3",  # Use the LLaMA 3 model
    system_prompt=system_prompt,
    temperature=0.7,  # Adjust creativity
    max_tokens=100,   # Limit response length
)

print("Chat Response:", response)
```

**Output:**

```
Chat Response: {'choices': [{'message': {'content': 'The capital of France is Paris.'}}]}
```

### 2. Completions Example

Use the `CompletionsEndpoint` to generate text completions.

```python
from textxgen import CompletionsEndpoint

# Initialize the CompletionsEndpoint
completions = CompletionsEndpoint()

# Define the input prompt
prompt = "Once upon a time"

# Send the completion request
response = completions.complete(
    prompt=prompt,
    model="phi3",      # Use the Phi-3 model
    temperature=0.7,   # Adjust creativity
    max_tokens=100,    # Limit response length
)

print("Completion Response:", response)
```

**Output:**

```
Completion Response: {'completions': [{'text': 'Once upon a time, in a land far, far away...'}]}
```

### 3. Listing Supported Models

Use the `ModelsEndpoint` to list and retrieve supported models.

```python
from textxgen import ModelsEndpoint

# Initialize the ModelsEndpoint
models = ModelsEndpoint()

# List all supported models
supported_models = models.list_models()
print("Supported Models:", supported_models)

# Retrieve a specific model ID
model_name = "llama3"
model_id = models.get_model(model_name)
print(f"Model ID for '{model_name}':", model_id)
```

**Output:**

```
Supported Models: {
    'llama3': 'meta-llama/llama-3.1-8b-instruct:free',
    'phi3': 'microsoft/phi-3-mini-128k-instruct:free',
    'deepseek': 'deepseek/deepseek-chat:free'
}
Model ID for 'llama3': meta-llama/llama-3.1-8b-instruct:free
```

## Supported Models

TextxGen currently supports the following models:

| Model Name                 | Model ID                                  |
| -------------------------- | ----------------------------------------- |
| LLaMA 3 (8B Instruct)      | `meta-llama/llama-3.1-8b-instruct:free`   |
| Phi-3 Mini (128K Instruct) | `microsoft/phi-3-mini-128k-instruct:free` |
| DeepSeek Chat              | `deepseek/deepseek-chat:free`             |

## Error Handling

TextxGen provides robust error handling for common issues:

- **Invalid Input**: Raised when invalid input is provided (e.g., empty messages or prompts).
- **API Errors**: Raised when the OpenRouter API returns an error (e.g., network issues or invalid requests).
- **Unsupported Models**: Raised when an unsupported model is requested.

**Example:**

```python
from textxgen.exceptions import InvalidInputError

try:
    response = chat.chat(messages=[])
except InvalidInputError as e:
    print("Error:", str(e))
```

## Contributing

Contributions are welcome! If you'd like to contribute to TextxGen, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## License

TextxGen is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/Sohail-ShaikhS--07/textxgen).
