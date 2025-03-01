# Copyright 2021 Pangea Cyber Corporation
# Author: Pangea Cyber Corporation
import logging

from ai.model.model import PangeaAiInput, PangeaMessage, PangeaRoles, FieldMapping

from .base import Translator

logger = logging.getLogger(__name__)

CLAUDE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-2020-12/schema",
    "title": "Anthropic Chat Completion Request",
    "type": "object",
    "properties": {
        "model": {"type": "string", "description": "The Anthropic model name, e.g. 'claude-v1'."},
        "system": {"type": "string", "description": "A description of the AI system."},
        "messages": {
            "type": "array",
            "description": "List of messages comprising the conversation so far. The last message is treated as the user's input.",
            "items": {
                "type": "object",
                "properties": {
                    "role": {
                        "type": "string",
                        "description": "Sender of the message: 'system', 'user', or 'assistant'.",
                    },
                    "content": {"type": "string", "description": "The text content of the message."},
                },
                "required": ["role", "content"],
                "additionalProperties": True,
            },
            "minItems": 1,
        },
        "max_tokens_to_sample": {
            "type": "integer",
            "minimum": 1,
            "description": "Max number of tokens to generate in the response.",
        },
        "temperature": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "Controls randomness. 0 = deterministic, 1 = maximum randomness.",
        },
        "top_k": {
            "type": "integer",
            "minimum": 0,
            "maximum": 10000,
            "description": "The number of highest-probability tokens to keep for sampling.",
        },
        "top_p": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "Probability threshold. Tokens beyond this cumulative probability are not considered.",
        },
        "metadata": {
            "type": "object",
            "description": "Optional metadata about the request or user context.",
            "properties": {
                "user_id": {"type": "string", "description": "Unique ID representing the end user."},
                "user_agent": {
                    "type": "string",
                    "description": "Identifier of the software agent sending the request.",
                },
            },
            "additionalProperties": True,
        },
        "stream": {"type": "boolean", "description": "If true, partial responses are streamed."},
        "stop_sequences": {
            "type": "array",
            "description": "List of strings upon which to stop generation.",
            "items": {"type": "string"},
        },
    },
    "required": ["messages"],
    "additionalProperties": True,
}


class ClaudeTranslator(Translator):
    """Translates Cladue-formatted input to PangeaAiPrompt"""

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
        return "claude"

    @classmethod
    def schema(cls):
        return CLAUDE_SCHEMA

    def get_pangea_messages(self) -> PangeaAiInput:
        """Returns a PangeaAiInput struct containing translated input fields

        Roles: system, user, assistant
        [
        {"role": "user", "content": "Hello there."},
        {"role": "assistant", "content": "Hi, I'm Claude. How can I help you?"},
        {"role": "user", "content": "Can you explain LLMs in plain English?"},
        ]
        """
        prefix_path = "$"
        msg_count = 0
        pangea_prompt = PangeaAiInput()
        if self._input.get("system"):
            pangea_prompt.messages.append(
                PangeaMessage(
                    role=PangeaRoles.PromptRoleSystem.value,
                    content=self._input.get("system"),
                )
            )
            self._mappings.append(FieldMapping(InputPath=f"{prefix_path}.system",
                                               PangeaPath=self._get_target_json_path(msg_count)))
            msg_count+=1
        for idx, prompt in enumerate(self._input.get("messages", [])):
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
                    content=prompt.get("content"),
                )
            )
            self._mappings.append(FieldMapping(InputPath=f"{prefix_path}.messages[{idx}].content",
                                               PangeaPath=self._get_target_json_path(msg_count)))
            msg_count+=1
        return pangea_prompt
