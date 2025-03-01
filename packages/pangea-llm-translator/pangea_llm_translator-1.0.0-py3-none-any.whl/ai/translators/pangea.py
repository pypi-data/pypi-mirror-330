# Copyright 2021 Pangea Cyber Corporation
# Author: Pangea Cyber Corporation
import logging

from ai.model.model import PangeaAiInput, PangeaMessage, PangeaRoles
from ai.model.model import FieldMapping

from .base import Translator

logger = logging.getLogger(__name__)

PANGEAAI_SCHEMA = {
    "$schema": "http://json-schema.org/draft-2020-12/schema",
    "title": "Pangea-styled prompt input",
    "description": "The Pangea-styled prompt input",
    "type": "array",
    "items": {
        "type": "object",
        "required": ["role", "content"],
        "properties": {
            "role": {
                "type": "string",
            },
            "content": {
                "type": "string"
            },
        },
    },
}


class PangeaAiTranslator(Translator):
    """Translates Pangea-formatted input to PangeaAiPrompt"""

    def __init__(self, input):
        super().__init__(input)

    def get_model_and_version(self) -> (str, str):
        """
        Return model name and version
        :return: tuple of model name and version tuple
        """
        return self.name(), None

    @classmethod
    def name(cls) -> str:
        return "pangea"

    @classmethod
    def schema(cls):
        return PANGEAAI_SCHEMA

    def get_pangea_messages(self) -> PangeaAiInput:
        """Returns a PangeaAiInput struct containing translated input fields

        Roles: system, user, assistant
        [
            {
                "role": "system",
                "content": "you are a joker"
            },
            {
                "role": "user",
                "content": "knock knock"
            },
            {
                "role": "assistant",
                "content": "Who's there?"
            }
        ]
        """
        pangea_prompt = PangeaAiInput()

        for idx, prompt in enumerate(self._input):
            role = prompt["role"]

            if role == "system":
                role = PangeaRoles.PromptRoleSystem.value
            elif role == "user":
                role = PangeaRoles.PromptRoleUser.value
            elif role == "assistant" or role == "llm_response":
                role = PangeaRoles.PromptRoleLlm.value

            p = PangeaMessage(
                role=role,
                content=prompt["content"],
            )
            # holding the mapping to transform the original input
            mapping=FieldMapping(
                InputPath=self._get_target_json_path(idx),
                PangeaPath=self._get_target_json_path(idx),
            )
            self._mappings.append(mapping)

            pangea_prompt.messages.append(p)

        return pangea_prompt
