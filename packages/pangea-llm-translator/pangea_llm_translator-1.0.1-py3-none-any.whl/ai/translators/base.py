# Copyright 2021 Pangea Cyber Corporation
# Author: Pangea Cyber Corporation
import logging
import typing as t
from abc import ABC, abstractmethod

from jsonpath_ng import parse

from ai.model.model import FieldMapping, PangeaAiInput

logger = logging.getLogger(__name__)

class Translator(ABC):
    """Interface to translate input JSON to known LLM fields"""

    def __init__(self, input: t.Any):
        self._input = input
        self._is_text = False
        self._mappings: t.List[FieldMapping] = []

    @abstractmethod
    def get_model_and_version(self) -> t.Tuple[str, str]:
        """
        Return model name and version
        :return: tuple of model name and version tuple
        """
        ...

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """LLM model name"""
        ...

    @classmethod
    @abstractmethod
    def schema(cls) -> dict:
        """The JSON schema for the translator
        """
        ...

    @abstractmethod
    def get_pangea_messages(self) -> PangeaAiInput:
        """Returns a PangeaAiInput struct containing translated input fields

        """
        ...

    def original_input(self) -> t.Any:
        """Returns the original input as-is"""
        return self._input

    def _get_target_json_path(self, idx, prefix="$", content_field='content'):
        """
        supporting function to return pangea messages json path
        :param idx: message index
        :param prefix: path prefix
        :param content_field: content field
        :return:
        """
        return f"{prefix}[{idx}].{content_field}"

    def _transformed_original_input(self, messages: list = None) -> t.Any:
        """
        supporting function to transform original input
        :param messages: response messages from the sdk
        :return:
        """
        logger.debug(f"Translating original input: {messages}, mappings: {self._mappings}")
        for idx, fieldMap in enumerate(self._mappings):
            # Assumption that pangea message map mapped with only one value
            matches = [match.value for match in parse(fieldMap.PangeaPath).find(messages)]
            if len(matches) != 1:
                raise ValueError(
                    f"Could not extract a single value; either no value was found or multiple values were extracted,"
                    f" preventing transformation. Match count={len(matches)}, path={fieldMap.PangeaPath}")
            jsonpath_expr = parse(fieldMap.InputPath)
            if not jsonpath_expr:
                raise ValueError(f"No matching input found for path: {fieldMap.InputPath}")
            jsonpath_expr.update(self._input, matches[0])
        return self._input

    def transformed_original_input(self, messages: list = None, text: str = None) -> t.Any:
        """
        Returns the original input after replacing original with passed message or text
        :param messages: response prompt messages from the apis
        :param text: response prompt text from the apis
        """
        if messages is None and text is None:
            return self._input

        # for text based translator
        if self._is_text:
            if text:
                return text
            if messages is not None and len(messages) > 0 and 'content' in messages[0]:
                return messages[0]['content']

        # for non-text,
        # if mapping is not defined due to any reason, then return _input without any transformation
        if len(self._mappings) == 0:
            if messages is not None:
                # Can't perform transformation, return original input itself
                return self._input
            else:
                return text
        else:
            if messages is not None:
                return self._transformed_original_input(messages)
            else:
                return text

    def is_text(self) -> bool:
        """Is the original input text/str"""
        return self._is_text
