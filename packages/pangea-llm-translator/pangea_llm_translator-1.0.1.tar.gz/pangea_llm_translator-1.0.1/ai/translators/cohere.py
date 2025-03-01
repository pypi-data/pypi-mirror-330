# Copyright 2021 Pangea Cyber Corporation
# Author: Pangea Cyber Corporation
import logging

from ai.model.model import PangeaAiInput, PangeaMessage, PangeaRoles, FieldMapping

from .base import Translator

logger = logging.getLogger(__name__)

COHERE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-2020-12/schema",
    "title": "Cohere prompt input",
    "description": "Accepts either an object with 'messages' or a direct array of messages.",
    "oneOf": [
        {"$ref": "#/components/schemas/messages"},
        {"$ref": "#/components/schemas/llm_input"},
    ],
    "components": {
        "schemas": {
            "messages": {
                "title": "Messages",
                "description": "Cohere styled prompt input messages",
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["role", "content"],
                    "properties": {
                        "role": {
                            "type": "string",
                            "enum": ["assistant", "user", "system", "tool"],
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
                "type": "object",
                "description": "Cohere styled full prompt input messages",
                "properties": {
                    "messages": {
                        "$ref": "#/components/schemas/messages",
                    },
                    "model": {
                        "type": "string",
                        "description": "Cohere model ",
                    },
                },
                "required": ["messages", "model"],
                "additionalProperties": True,
            },
        }
    },
}


class CohereTranslator(Translator):
    """Translates Cohere-formatted input to PangeaAiPrompt"""

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
        return "cohere"

    @classmethod
    def schema(cls):
        return COHERE_SCHEMA

    def get_pangea_messages(self) -> PangeaAiInput:
        """Returns a PangeaAiInput struct containing translated input fields

        Roles: system, user, assistant, tool

        messages: [
          {
            "role": "system",
            "content": "You are a helpful system administrator.",
          },
          {
            "role": "user",
           "content": "How do I install a k8 operator?",
          },
          {
            "role": "assistant",
            "content": "by installing it",
          }
        ]

        OR

          messages: [
            {
              "role": "system",
              "content": "you are a joker"
            },
            {
              "role": "user",
              "content": [{ "type": "text", "text": "knock knock" }]
            },
            {
              "role": "assistant",
              "content": [{ "type": "text", "text": "Who's there?" }]
            }
          ]
        OR
        full payload
        """
        pangea_prompt = PangeaAiInput()
        prefix_path = "$"
        messages = self._input
        if isinstance(self._input, dict):
            prefix_path = f"{prefix_path}.messages"
            messages = self._input.get("messages", [])

        msg_count = 0
        for idx, prompt in enumerate(messages):
            role = prompt["role"]

            if role == "system":
                role = PangeaRoles.PromptRoleSystem.value
            elif role == "user":
                role = PangeaRoles.PromptRoleUser.value
            elif role == "assistant":
                role = PangeaRoles.PromptRoleLlm.value

            content = prompt["content"]

            if isinstance(content, str):
                p = PangeaMessage(
                    role=role,
                    content=content,
                )
                pangea_prompt.messages.append(p)
                self._mappings.append(FieldMapping(InputPath=f"{prefix_path}[{idx}].content",
                                                   PangeaPath=self._get_target_json_path(msg_count)))
                msg_count+=1

            else:
                for idx2, part in enumerate(content):
                    # text only support
                    if part.get("type", "") == "text":
                        p = PangeaMessage(
                            role=role,
                            content=part["text"],
                        )
                        pangea_prompt.messages.append(p)
                        self._mappings.append(FieldMapping(InputPath=f"{prefix_path}[{idx}].content[{idx2}].text",
                                                           PangeaPath=self._get_target_json_path(msg_count)))
                        msg_count+=1
        return pangea_prompt
