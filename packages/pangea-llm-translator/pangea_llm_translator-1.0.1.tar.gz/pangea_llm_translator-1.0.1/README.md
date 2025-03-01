# pangea-llm-translators

## Description
llm-message-translator is a Python library designed to convert, transform, and censor messages for various LLM (Large Language Model) providers. It supports multiple AI models and platforms, including:
* OpenAI
* Mistral
* LangChain
* Gemini (Google AI)
* DBRX (Databricks)
* Cohere
* Claude (Anthropic)
* AWS Bedrock
* Pangea

### Features
* Seamlessly convert various LLM message formats to the Pangea Messages format.
Preserve message structure while transforming the original input using responses from Pangea AI Guard APIs.

## Installation
```shell
pip install llm-message-translator
```
## Usage Example
```python
from ai import get_translator

# Define an OpenAI-style LLM input
openapi_message = {
   "model": "gpt-4o",
   "messages": [
      {"role": "developer", "content": "you are a joker"},
      {"role": "user", "content": [{"type": "text", "text": "knock knock"}]},
      {"role": "assistant", "content": [{"type": "text", "text": "Who's there?"}]},
   ],
}

# Initialize the translator
translator = get_translator(openapi_message, llm_hint="openai")

# Convert to Pangea format
pangea_messages = translator.get_pangea_messages()

# Print transformed messages
print(pangea_messages.get_messages_list())
# [{'role': 'system', 'content': 'you are a joker'}, {'role': 'user', 'content': 'knock knock'}, {'role': 'assistant', 'content': "Who's there?"}]

# Mimic some api behavior like modify content (Example: Censor "joker")
for message in pangea_messages.messages:
   message.content = message.content.replace("joker", "*****")

# Convert back to OpenAPI input format
original_output = translator.transformed_original_input(messages=pangea_messages.get_messages_list())

print(original_output)

```

# 

## Prerequisites
Ensure you have the following installed:

- Python 3.9+
- [Poetry](https://python-poetry.org/docs/#installation)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/pangeacyber/pangea-llm-translators.git
   cd pangea-llm-translators
   ```
2. Install dependencies using Poetry:
   ```sh
   poetry install
   ```

## Running Tests
To run the test suite, use:
```sh
poetry run pytest
```

## Running the Application
To run the application, use:
```sh
poetry run python examples/openai_translator.py
```

## Virtual Environment
To activate the virtual environment:
```sh
poetry shell
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please create an issue or submit a pull request.

