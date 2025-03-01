# Copyright 2021 Pangea Cyber Corporation
# Author: Pangea Cyber Corporation
from dataclasses import dataclass, field, asdict
from enum import Enum
import typing as t

@dataclass
class FieldMapping:
    InputPath: str
    PangeaPath: str

class PangeaRoles(str, Enum):
    PromptRoleSystem = "system"
    PromptRoleUser = "user"
    PromptRoleLlm = "assistant"


@dataclass
class PangeaMessage:
    role: str
    content: t.Any


@dataclass
class PangeaAiInput:
    """Defines the prompt schema used by Pangea"""

    messages: t.List[PangeaMessage] = field(default_factory=list)

    def get_prompts(self, pangea_role: PangeaRoles) -> t.List[PangeaMessage]:
        """Returns all prompts of type"""
        result = []
        for prompt in self.messages:
            if prompt.role == pangea_role:
                result.append(prompt)
        return result

    def as_dict(self):
        return {k: v for (k, v) in asdict(self).items() if v is not None}

    def get_messages_list(self) -> list:
        """
        Returns a list of all prompts messages list in dict format
        """
        messages = []
        for message in self.messages:
            messages.append(asdict(message))
        return messages