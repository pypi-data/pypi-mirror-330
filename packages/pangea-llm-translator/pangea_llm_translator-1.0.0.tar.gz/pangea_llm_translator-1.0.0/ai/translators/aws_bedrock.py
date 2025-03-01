# Copyright 2021 Pangea Cyber Corporation
# Author: Pangea Cyber Corporation
import logging
import re
import typing as t

from ai.model.model import PangeaAiInput, PangeaMessage, PangeaRoles, FieldMapping

from .base import Translator

logger = logging.getLogger(__name__)

AWSBEDROCK_SCHEMA = {
    "$schema": "http://json-schema.org/draft-2020-12/schema",
    "title": "AWS Bedrock prompt input",
    "description": "Accepts either an object with 'messages' or a direct array of messages.",
    "oneOf": [
        {"$ref": "#/components/schemas/messages"},
        {"$ref": "#/components/schemas/inputText"},
        {"$ref": "#/components/schemas/llm_input"},
    ],
    "components": {
        "schemas": {
            "role-content-list": {
                "type": "array",
                "description": "role content array",
                "items": {
                    "type": "object",
                    "properties": {
                        "role": {"type": "string", "description": "Role of the entity providing the message."},
                        "content": {
                            "$ref": "#/components/schemas/content-object",
                        },
                    },
                    "required": ["role", "content"],
                },
            },
            "text-list": {
                "type": "array",
                "description": "An array containing conversation content.",
                "items": {
                    "type": "object",
                    "properties": {"text": {"type": "string", "description": "The content of the message."}},
                    "required": ["text"],
                },
            },
            "content-object": {
                "title": "content-object",
                "description": "The system prompt messages.",
                "oneOf": [
                    {"$ref": "#/components/schemas/text-list"},
                    {
                        "type": "string",
                        "description": "Only content string",
                    },
                ],
            },
            "system": {
                "title": "system prompt messages",
                "description": "The system prompt messages.",
                "oneOf": [
                    {"$ref": "#/components/schemas/text-list"},
                    {
                        "type": "string",
                        "description": "Single system prompt messages",
                    },
                ],
            },
            "messages": {
                "title": "AWS Bedrock prompt input",
                "description": "The AWS Bedrock prompt input",
                "oneOf": [
                    {
                        "type": "object",
                        "properties": {
                            "role": {"type": "string", "description": "Role of the entity providing the message."},
                            "content": {
                                "$ref": "#/components/schemas/content-object",
                            },
                        },
                        "required": ["role", "content"],
                    },
                    {
                        "$ref": "#/components/schemas/role-content-list",
                    },
                    {
                        "$ref": "#/components/schemas/text-list",
                    },
                ],
            },
            "inputText": {
                "type": "object",
                "properties": {
                    "inputText": {
                        "type": "string",
                        "description": "The prompt or text to send to the model for processing when using a single prompt-based interaction.",
                    }
                },
                "required": ["inputText"],
            },
            "llm_input": {
                "type": "object",
                "description": "AWS Bedrock styled full prompt input messages",
                "properties": {
                    "messages": {
                        "$ref": "#/components/schemas/messages",
                    },
                    "inputText": {
                        "type": "string",
                        "description": "The prompt or text to send to the model for processing when using a single prompt-based interaction.",
                    },
                    "modelId": {
                        "type": "string",
                        "description": "The model identifier to use (e.g., 'claude-v1', 'palm-2').",
                    },
                    "temperature": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1,
                        "description": "Controls the randomness of the output. Higher values make output more random.",
                    },
                    "maxTokens": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "The maximum number of tokens to generate in the response.",
                    },
                    "topP": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1,
                        "description": "Controls the diversity of outputs using nucleus sampling.",
                    },
                    "stopSequences": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional stop sequences to halt text generation when encountered.",
                    },
                },
                "oneOf": [
                    {"required": ["modelId", "inputText"], "not": {"required": ["messages"]}},
                    {"required": ["modelId", "messages"], "not": {"required": ["inputText"]}},
                ],
                "required": ["modelId"],
                "additionalProperties": True,
            },
        }
    },
}


class AWSBedrockTranslator(Translator):
    """Translates AWSBedrock-formatted input to PangeaAiPrompt"""

    def __init__(self, input):
        super().__init__(input)

    @classmethod
    def name(cls) -> str:
        return "awsbedrock"

    def get_model_and_version(self) -> (str, str):
        """
        Return model name and version
        :return: tuple of model name and version tuple
        """
        if isinstance(self._input, dict) and 'modelId' in self._input:
            return self._input.get('modelId'), self._input.get('version', None)
        else:
            return self.name(), None

    @classmethod
    def schema(cls):
        return AWSBEDROCK_SCHEMA

    def _get_prompt_msg(self, prompt, prefix_path, msg_count=0) -> t.List[PangeaMessage]:
        # Regex to match role and content in the prompt
        pattern = r"(?:(\w+):\s*(.*?))(?:\n\n|$)"
        matches = re.findall(pattern, prompt, re.DOTALL)

        messages = []
        for match in matches:
            roleRaw, content = match
            role = roleRaw.strip().lower()
            if role == "user" or role == "human":
                role = PangeaRoles.PromptRoleUser.value
            elif role == "assistant" or role == "ai":
                role = PangeaRoles.PromptRoleLlm.value
            elif role == "system":
                role = PangeaRoles.PromptRoleSystem.value

            messages.append(
                PangeaMessage(
                    role=role,
                    content=content.strip()
                )
            )
            # Note: This can't work for multiple roles but single role or only text which is applicable for most the
            # cases
            self._mappings.append(FieldMapping(InputPath=f"{prefix_path}",
                                                PangeaPath=self._get_target_json_path(msg_count)))
            msg_count+=1
        return messages

    def _parse_content(
        self, role: str, content, prefix_path, is_text: bool = False, msg_count=0
    ) -> t.List[PangeaMessage]:
        if role == "user" or role == "human":
            role = PangeaRoles.PromptRoleUser.value
        elif role == "assistant" or role == "ai":
            role = PangeaRoles.PromptRoleLlm.value
        elif role == "system":
            role = PangeaRoles.PromptRoleSystem.value

        messages = []
        if isinstance(content, str):
            messages.append(
                PangeaMessage(
                    role=role,
                    content=f"{content}",
                )
            )
            self._mappings.append(FieldMapping(InputPath=f"{prefix_path}", PangeaPath=self._get_target_json_path(msg_count)))
            msg_count+=1
        elif isinstance(content, list):
            for idx, item in enumerate(content):
                messages.append(
                    PangeaMessage(
                        role=role,
                        content=item.get("text"),
                    )
                )
                self._mappings.append(FieldMapping(InputPath=f"{prefix_path}[{idx}].text", PangeaPath=self._get_target_json_path(msg_count)))
                msg_count+=1
        else:
            messages.append(
                PangeaMessage(
                    role=role,
                    content=f"{content}",
                )
            )
            self._mappings.append(FieldMapping(InputPath=f"{prefix_path}", PangeaPath=self._get_target_json_path(msg_count)))
            msg_count+=1
        return messages

    def get_pangea_messages(self) -> PangeaAiInput:
        """Returns a PangeaAiInput struct containing translated input fields

        {"inputText": "\n\nHuman: story of two dogs\n\nAssistant:"}
        OR
        System prompt as
        [
            {
                "text": "You are an app that .."
            }
        ]
        OR
        user/assistant as
        {
            "role": "user | assistant",
            "content": [
                {
                    "text": "string"
                }
            ]
        }
        """
        pangea_prompt = PangeaAiInput()
        prefix_path = "$"
        msg_count = 0
        # Case 1: If the input is an object with a 'prompt' key
        # Example:  {"inputText": "\n\nHuman: story of two dogs\n\nAssistant:"}
        if isinstance(self._input, dict) and "inputText" in self._input:
            messages = self._get_prompt_msg(self._input["inputText"], f"{prefix_path}.inputText", msg_count)
            if messages:
                msg_count+=len(messages)
                pangea_prompt.messages.extend(messages)

        # Case 2: If the input contains system messages
        if isinstance(self._input, dict) and "system" in self._input:
            system_message = self._input.get("system")
            if isinstance(system_message, list):
                for idx, item in enumerate(system_message):
                    pangea_prompt.messages.append(
                        PangeaMessage(
                            role=PangeaRoles.PromptRoleSystem.value,
                            content=item.get("text"),
                        )
                    )
                    self._mappings.append(FieldMapping(InputPath=f"{prefix_path}.system[{idx}].text",
                                                       PangeaPath=self._get_target_json_path(msg_count)))
                    msg_count+=1
            else:
                # Single system message
                pangea_prompt.messages.append(
                    PangeaMessage(
                        role=PangeaRoles.PromptRoleSystem.value,
                        content=system_message,
                    )
                )
                self._mappings.append(FieldMapping(InputPath=f"{prefix_path}.system.text",
                                                   PangeaPath=self._get_target_json_path(msg_count)))
                msg_count+=1

        # Case 3: Handle messages
        messages = self._input
        if isinstance(self._input, dict) and "messages" in self._input:
            prefix_path = f"{prefix_path}.messages"
            messages = self._input.get("messages")

        if isinstance(messages, list):
            for idx, item in enumerate(messages):
                if isinstance(item, dict) and "role" in item and "content" in item:
                    prompt_messages = self._parse_content(
                        item.get("role"), item.get("content"), f"{prefix_path}[{idx}].content", msg_count=msg_count
                    )
                elif isinstance(item, dict) and "text" in item:
                    prompt_messages = self._parse_content(
                        "user", item.get("text"), f"{prefix_path}[{idx}].text", msg_count=msg_count
                    )
                else:
                    # Catch all
                    prompt_messages = self._parse_content(
                        "user", item, f"{prefix_path}[{idx}]",msg_count=msg_count
                    )
                msg_count+=len(prompt_messages)
                pangea_prompt.messages.extend(prompt_messages)
        # Case 4: message is dict
        elif isinstance(messages, dict) and "role" in messages and "content" in messages:
            role = messages.get("role", "").lower()
            content = messages.get("content", "")
            prompt_messages = self._parse_content(role, content, f"{prefix_path}.content",msg_count=msg_count)
            pangea_prompt.messages.extend(prompt_messages)

        return pangea_prompt
