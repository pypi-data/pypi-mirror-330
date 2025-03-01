# Copyright 2021 Pangea Cyber Corporation
# Author: Pangea Cyber Corporation
import logging

from ai.model.model import PangeaAiInput, PangeaMessage, PangeaRoles

from .base import Translator

logger = logging.getLogger(__name__)


class PlainTextTranslator(Translator):
    """Dummy translator for string input to PangeaAiPrompt"""

    def __init__(self, input):
        super().__init__(input)
        self._is_text = True

    def get_model_and_version(self) -> (str, str):
        """
        Return model name and version
        :return: tuple of model name and version tuple
        """
        return self.name(), None

    @classmethod
    def name(cls) -> str:
        return "plaintext"

    @classmethod
    def schema(cls):
        return {}

    def get_pangea_messages(self) -> PangeaAiInput:
        """
        Treat as single user prompt
        """
        pangea_prompt = PangeaAiInput(
            messages=[
                PangeaMessage(
                    role=PangeaRoles.PromptRoleUser.value,
                    content=self._input,
                )
            ]
        )

        return pangea_prompt
