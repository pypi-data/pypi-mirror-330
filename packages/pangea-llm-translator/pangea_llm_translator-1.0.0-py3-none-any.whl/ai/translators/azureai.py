# Copyright 2021 Pangea Cyber Corporation
# Author: Pangea Cyber Corporation
import logging

from .openai import OpenAiTranslator

logger = logging.getLogger(__name__)


class AzureAiTranslator(OpenAiTranslator):
    """Azure AI as similar format as OpenAI, so we just inherit the functionality from open ai"""

    def __init__(self, input):
        super().__init__(input)

    @classmethod
    def name(cls) -> str:
        return "azureai"
