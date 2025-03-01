# Copyright 2021 Pangea Cyber Corporation
# Author: Pangea Cyber Corporation
import logging

from ai.model.model import PangeaAiInput, PangeaMessage, PangeaRoles, FieldMapping

from .base import Translator

logger = logging.getLogger(__name__)

GEMINI_SCHEMA = {
    "$schema": "http://json-schema.org/draft-2020-12/schema",
    "title": "Gemini-styled prompt input",
    "description": "Accepts either an object with 'contents' in the payload or only contents.",
    "oneOf": [
        {"$ref": "#/components/schemas/messages_only"},
        {"$ref": "#/components/schemas/llm_input"},
    ],
    "components": {
        "schemas": {
            "contents-definition": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["parts"],
                    "properties": {
                        "role": {
                            "type": "string",
                            "default": "user",
                        },
                        "parts": {"$ref": "#/components/schemas/parts-definition"},
                    },
                },
            },
            "parts-definition": {
                "type": "array",
                "items": {"type": "object", "required": ["text"], "properties": {"text": {"type": "string"}}},
            },
            "single-parts-definition": {
                "type": "object",
                "required": ["text"],
                "properties": {"text": {"type": "string"}},
            },
            "contents": {
                "title": "Gemini-styled contents data ",
                "description": "The Gemini-styled prompt input",
                "oneOf": [
                    {
                        "description": "new contents style",
                        "$ref": "#/components/schemas/contents-definition",
                    },
                    {
                        "description": "older style",
                        "$ref": "#/components/schemas/contents-definition",
                    },
                ],
            },
            "system_instruction": {
                "type": "object",
                "required": ["parts"],
                "properties": {
                    "parts": {"$ref": "#/components/schemas/single-parts-definition"},
                },
            },
            "llm_input": {
                "type": "object",
                "description": "Gemini styled full llm prompt input",
                "properties": {
                    "contents": {
                        "$ref": "#/components/schemas/contents",
                    },
                    "system_instruction": {
                        "$ref": "#/components/schemas/system_instruction",
                    },
                    "model": {"type": "string"},
                    "temperature": {"type": "number"},
                    "top_p": {"type": "number"},
                },
                "required": ["contents"],
                "additionalProperties": True,
            },
            "messages_only": {
                "title": "Gemini-styled prompt input",
                "description": "The Gemini-styled prompt input",
                "oneOf": [
                    {
                        "description": "current style",
                        "type": "object",
                        "required": ["contents"],
                        "properties": {
                            "system_instruction": {
                                "type": "object",
                                "required": ["parts"],
                                "properties": {
                                    "parts": {"$ref": "#/components/schemas/single-parts-definition"},
                                },
                            },
                            "contents": {"$ref": "#/components/schemas/contents-definition"},
                        },
                    },
                    {
                        "description": "older style",
                        "$ref": "#/components/schemas/contents-definition",
                    },
                ],
            },
        }
    },
}


class GeminiTranslator(Translator):
    """Translates Gemini-formatted input to PangeaAiPrompt"""

    def __init__(self, input):
        super().__init__(input)

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
    def name(cls) -> str:
        return "gemini"

    @classmethod
    def schema(cls):
        return GEMINI_SCHEMA

    def _get_from_contents(self, contents: list, prefix_path: str, msg_count:int = 0) -> list[PangeaMessage]:
        """
        [
            {
                "parts": [
                    {
                        "text": "You are a helpful assistant."
                    }
                ],
                "role": "system"
            },
            {
                "parts": [
                    {
                        "text": "What is the capital of France?"
                    }
                ],
                "role": "user"
            }
        ]
        """
        messages = []

        for idx, content in enumerate(contents):
            role = content.get("role", None)
            if role == "system":
                role = PangeaRoles.PromptRoleSystem.value
            elif role == "user":
                role = PangeaRoles.PromptRoleUser.value
            elif role == "model":
                role = PangeaRoles.PromptRoleLlm.value

            content_prefix = f"{prefix_path}[{idx}]"
            for idx2, part in enumerate(content["parts"]):
                p = PangeaMessage(
                    role=role,
                    content=part["text"],
                )
                messages.append(p)
                self._mappings.append(FieldMapping(InputPath=f"{content_prefix}.parts[{idx2}].text",
                                                   PangeaPath=self._get_target_json_path(msg_count)))
                msg_count+=1

        return messages

    def get_pangea_messages(self) -> PangeaAiInput:
        """Returns a PangeaAiInput struct containing translated input fields

        Roles: system_instruction, user, model
        Two distinct styles:

        Old
        [
            {
                "parts": [
                    {
                        "text": "You are a helpful assistant."
                    }
                ],
                "role": "system"
            },
            {
                "parts": [
                    {
                        "text": "What is the capital of France?"
                    }
                ],
                "role": "user"
            }
        ]

        New
        {
            "system_instruction":
                {
                    "parts": {"text": "You are Neko the cat respond like one"}
                },
            "contents": [
                {
                    "parts":[
                        {"text": "Hello cat."}
                    ]
                },
                {
                    "role": "model",
                    "parts":[
                        {"text": "Meow? \n"}
                    ]
                },
                {
                    "role": "user",
                    "parts":[
                        {"text": "What is your name? What do like to drink?"}
                    ]
                }
            ]
        }
        """
        pangea_prompt = PangeaAiInput()
        prefix_path = "$"
        if isinstance(self._input, list):
            # old
            pangea_prompt.messages = self._get_from_contents(self._input, prefix_path)
        elif isinstance(self._input, dict):
            # new
            msg_count = 0
            key = "system_instruction"
            system_prompt = self._input.get(key, None)
            if system_prompt:
                p = PangeaMessage(
                    role=PangeaRoles.PromptRoleSystem.value,
                    content=system_prompt["parts"]["text"],
                )
                pangea_prompt.messages.append(p)
                self._mappings.append(FieldMapping(InputPath=f"{prefix_path}.{key}.parts.text",
                                                   PangeaPath=self._get_target_json_path(msg_count)))
                msg_count +=1

            contents = self._input.get("contents", [])
            if contents:
                message = self._get_from_contents(contents, f"{prefix_path}.contents", msg_count=msg_count)
                pangea_prompt.messages.extend(message)
        else:
            logger.error(f"[{self.name()}] Unexpected input format")

        return pangea_prompt
