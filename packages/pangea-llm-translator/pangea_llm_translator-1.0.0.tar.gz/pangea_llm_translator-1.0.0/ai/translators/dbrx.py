# Copyright 2021 Pangea Cyber Corporation
# Author: Pangea Cyber Corporation
import logging

from ai.model.model import PangeaAiInput, PangeaMessage, PangeaRoles, FieldMapping

from .base import Translator

logger = logging.getLogger(__name__)

DBRX_SCHEMA = {
    "$schema": "http://json-schema.org/draft-2020-12/schema",
    "title": "DBRX/Databricks prompt input",
    "description": "Accepts either an object with 'messages' or a direct array of messages.",
    "oneOf": [
        {"$ref": "#/components/schemas/messages"},
        {"$ref": "#/components/schemas/llm_input"},
    ],
    "components": {
        "schemas": {
            "messages": {
                "title": "DBRX/Databricks prompt input messages",
                "description": "DBRX/Databricks styled prompt input messages",
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "role": {"type": "string"},
                        "content": {"type": "string"},
                    },
                    "required": ["role", "content"],
                },
            },
            "llm_input": {
                "type": "object",
                "description": "DBRX/Databricks styled full prompt input messages",
                "properties": {
                    "messages": {
                        "$ref": "#/components/schemas/messages",
                    },
                    "model": {
                        "type": "string",
                        "description": "DBRX/Databricks model name",
                    },
                },
                "required": ["messages", "model"],
                "additionalProperties": True,
            },
        }
    },
}


class DBRXTranslator(Translator):
    """Translates DBRX/Databricks-formatted input to PangeaAiPrompt"""

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
        return "dbrx"

    @classmethod
    def schema(cls):
        return DBRX_SCHEMA

    def get_pangea_messages(self) -> PangeaAiInput:
        """Returns a PangeaAiInput struct containing translated input fields

          Roles: system, user, assistant

        "messages": [
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Hello!"},
          {"role": "assistant", "content": "by installing it"}
        ]

        """
        pangea_prompt = PangeaAiInput()
        prefix_path = "$"
        messages = self._input
        if isinstance(self._input, dict):
            prefix_path = f"{prefix_path}.messages"
            messages = self._input.get("messages", [])

        for idx, prompt in enumerate(messages):
            role = prompt.get("role")

            if role == "user":
                role = PangeaRoles.PromptRoleUser.value
            elif role == "assistant":
                role = PangeaRoles.PromptRoleLlm.value
            elif role == "system":
                role = PangeaRoles.PromptRoleSystem.value

            pangea_prompt.messages.append(
                PangeaMessage(
                    role=role,
                    content=prompt["content"],
                )
            )
            self._mappings.append(FieldMapping(InputPath=f"{prefix_path}[{idx}].content",
                                               PangeaPath=self._get_target_json_path(idx)))
        return pangea_prompt
