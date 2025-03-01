# Copyright 2021 Pangea Cyber Corporation
# Author: Pangea Cyber Corporation
import logging

from ai.model.model import PangeaAiInput, PangeaMessage, PangeaRoles
from ai.model.model import FieldMapping

from .base import Translator

logger = logging.getLogger(__name__)

OPENAI_SCHEMA = {
    "$schema": "http://json-schema.org/draft-2020-12/schema",
    "title": "OpenAi-styled prompt input",
    "description": "Accepts either an object with 'messages' or a direct array of messages.",
    "oneOf": [
        {"$ref": "#/components/schemas/messages"},
        {"$ref": "#/components/schemas/llm_input"},
    ],
    "components": {
        "schemas": {
            "messages": {
                "title": "OpenAi-styled messages input",
                "description": "The OpenAi-styled messages input",
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["role", "content"],
                    "properties": {
                        "role": {
                            "type": "string",
                            "enum": ["developer", "system", "user", "assistant", "function", "tool"],
                        },
                        "content": {
                            "oneOf": [
                                {"type": "string"},
                                {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "required": ["type", "text"],
                                        "properties": {
                                            "type": {"type": "string", "enum": ["text"]},
                                            "text": {"type": "string"},
                                        },
                                    },
                                },
                            ]
                        },
                    },
                },
            },
            "llm_input": {
                "title": "OpenAi-styled full prompt input",
                "description": "The OpenAi-styled full prompt input",
                "type": "object",
                "properties": {
                    "model": {
                        "type": "string",
                        "description": "The model to use for generating completions (e.g., gpt-3.5-turbo, gpt-4). Not required for Azure OpenAI.",
                    },
                    "messages": {
                        "$ref": "#/components/schemas/messages",
                    },
                    "temperature": {
                        "type": "number",
                        "description": "Controls randomness of the output. Higher values = more random.",
                        "minimum": 0,
                    },
                    "top_p": {
                        "type": "number",
                        "description": "Alternative to temperature for nucleus sampling. 1 means no filtering.",
                        "minimum": 0,
                        "maximum": 1,
                    },
                    "max_tokens": {
                        "type": "integer",
                        "description": "Maximum number of tokens to generate in the chat completion.",
                        "minimum": 1,
                    },
                    "frequency_penalty": {"type": "number", "description": "Penalizes repeated tokens.", "minimum": 0},
                    "presence_penalty": {"type": "number", "description": "Penalizes repeating topics.", "minimum": 0},
                    "stop": {
                        "description": "Up to 4 sequences where the API will stop generating further tokens. Can be a string, array of strings, or null.",
                        "oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}, {"type": "null"}],
                    },
                    "functions": {
                        "type": "array",
                        "description": "List of function definitions for function calling (optional).",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "The function name to be called by the model.",
                                },
                                "description": {
                                    "type": "string",
                                    "description": "A brief description of what the function does.",
                                },
                                "parameters": {
                                    "type": "object",
                                    "description": "JSON Schema defining function arguments.",
                                },
                            },
                            "required": ["name", "parameters"],
                            "additionalProperties": False,
                        },
                    },
                    "function_call": {
                        "description": "Controls how the model responds about calling functions. 'auto' (default), 'none', or an object specifying which function to call.",
                        "oneOf": [
                            {"type": "string", "enum": ["auto", "none"]},
                            {
                                "type": "object",
                                "properties": {"name": {"type": "string"}},
                                "required": ["name"],
                                "additionalProperties": False,
                            },
                        ],
                    },
                },
                "required": ["messages", "model"],
                "additionalProperties": True,
            },
        }
    },
}


class OpenAiTranslator(Translator):
    """Translates OpenAi-formatted input to PangeaAiPrompt"""

    def __init__(self, input):
        super().__init__(input)

    @classmethod
    def name(cls) -> str:
        return "openai"

    def get_model_and_version(self) -> (str, str):
        """
        Return model name and version
        :return: tuple of model name and version tuple
        """
        if isinstance(self._input, dict) and 'model' in self._input:
            return self._input.get('model'), self._input.get('version', None)
        else:
            return self.name(), None

    @classmethod
    def schema(cls):
        return OPENAI_SCHEMA

    def get_pangea_messages(self) -> PangeaAiInput:
        """Returns a PangeaAiInput struct containing translated input fields

         Roles: developer, user, assistant

         input:
         {
         "messages": [
          {
            "role": "system",
            "content": "You are a helpful assistant."
          },
          {
            "role": "user",
            "content": "Tell me a fun fact about hummingbirds."
          }
        ],
        "max_tokens": 80,
        "temperature": 0.7
        ......
        }
        """
        pangea_prompt = PangeaAiInput()
        messages = self._input
        prefix_path = "$"
        if not isinstance(self._input, list):
            prefix_path = f"{prefix_path}.messages"
            messages = self._input.get("messages", [])

        msg_count = 0
        for idx, prompt in enumerate(messages):
            role = prompt["role"]
            if role == "developer" or role == "system":
                role = PangeaRoles.PromptRoleSystem.value
            elif role == "user":
                role = PangeaRoles.PromptRoleUser.value
            elif role == "assistant":
                role = PangeaRoles.PromptRoleLlm.value

            idx_content_path = f"{prefix_path}[{idx}].content"
            # content can be a string or array
            content = prompt["content"]
            if isinstance(content, str):
                p = PangeaMessage(
                    role=role,
                    content=content,
                )
                self._mappings.append(FieldMapping(InputPath=idx_content_path, PangeaPath=self._get_target_json_path(msg_count)))
                pangea_prompt.messages.append(p)
                msg_count +=1
            else:
                for idx2, part in enumerate(content):
                    # we only support "text" for now
                    if "text" == part.get("type", ""):
                        p = PangeaMessage(
                            role=role,
                            content= part["text"],
                        )
                        idx2_content_path = f"{idx_content_path}[{idx2}].text"
                        self._mappings.append(FieldMapping(InputPath=idx2_content_path, PangeaPath=self._get_target_json_path(msg_count)))
                        pangea_prompt.messages.append(p)
                        msg_count +=1

        return pangea_prompt
