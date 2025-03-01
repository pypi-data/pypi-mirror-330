# Copyright 2021 Pangea Cyber Corporation
# Author: Pangea Cyber Corporation
import json

import jsonschema
import logging
import typing as t

import jsonschema.exceptions

from ai.translators.aws_bedrock import AWSBedrockTranslator
from ai.translators.azureai import AzureAiTranslator
from ai.translators.base import Translator
from ai.translators.claude import ClaudeTranslator
from ai.translators.cohere import CohereTranslator
from ai.translators.dbrx import DBRXTranslator
from ai.translators.langchain import LangchainTranslator
from ai.translators.mistral import MistralTranslator
from ai.translators.openai import OpenAiTranslator
from ai.translators.gemini import GeminiTranslator
from ai.translators.plaintext import PlainTextTranslator
from ai.translators.pangea import PangeaAiTranslator

logger = logging.getLogger(__name__)


def get_translator_str_input(input: t.Any) -> Translator:
    """
    return translator if it matches any string based translator
    :param input: input text
    :return:
    """
    # return plain text translator
    return PlainTextTranslator(input)


def get_translator(input: t.Any, llm_hint: t.Optional[str] = None) -> Translator:
    """Get instance of translator

    :param input: can be a plain text string, or JSON struct
    :return Translator: LLM specific translator
    :raise ValidationError: input format not supported
    """
    logger.debug(f"[get_translator] {input}, llm_hint: {llm_hint}")

    if llm_hint:
        return get_translator_with_hint(input, llm_hint)

    if isinstance(input, str):
        # plain text
        return get_translator_str_input(input)

    # try gpt
    try:
        jsonschema.validate(instance=input, schema=OpenAiTranslator.schema())
    except jsonschema.exceptions.ValidationError as e:
        # not gpt
        # logger.info(f"{e.message}")
        pass
    else:
        return OpenAiTranslator(input)

    # try gemini
    try:
        jsonschema.validate(instance=input, schema=GeminiTranslator.schema())
    except jsonschema.exceptions.ValidationError as e:
        # not gemini
        # logger.info(f"{e.message}")
        pass
    else:
        return GeminiTranslator(input)

    # try pangea
    try:
        jsonschema.validate(instance=input, schema=PangeaAiTranslator.schema())
    except jsonschema.exceptions.ValidationError as e:
        # not pangea
        # logger.info(f"{e.message}")
        pass
    else:
        return PangeaAiTranslator(input)

    # try azure
    try:
        jsonschema.validate(instance=input, schema=AzureAiTranslator.schema())
    except jsonschema.exceptions.ValidationError as e:
        # not azure
        # logger.info(f"{e.message}")
        pass
    else:
        return AzureAiTranslator(input)

    # Try AWSBedrock
    try:
        jsonschema.validate(instance=input, schema=AWSBedrockTranslator.schema())
    except jsonschema.exceptions.ValidationError as e:
        # not AWSBedrock
        # logger.info(f"{e.message}")
        pass
    else:
        return AWSBedrockTranslator(input)

    # try claude
    try:
        jsonschema.validate(instance=input, schema=ClaudeTranslator.schema())
    except jsonschema.exceptions.ValidationError as e:
        # not claude
        # logger.info(f"{e.message}")
        pass
    else:
        return ClaudeTranslator(input)

    # try cohere
    try:
        jsonschema.validate(instance=input, schema=CohereTranslator.schema())
    except jsonschema.exceptions.ValidationError as e:
        # not cohere
        # logger.info(f"{e.message}")
        pass
    else:
        return CohereTranslator(input)

    # try dbrx
    try:
        jsonschema.validate(instance=input, schema=DBRXTranslator.schema())
    except jsonschema.exceptions.ValidationError as e:
        # not dbrx
        # logger.info(f"{e.message}")
        pass
    else:
        return DBRXTranslator(input)

    # try Mistral
    try:
        jsonschema.validate(instance=input, schema=MistralTranslator.schema())
    except jsonschema.exceptions.ValidationError as e:
        # not Mistral
        # logger.info(f"{e.message}")
        pass
    else:
        return MistralTranslator(input)

    # Try Langchain
    try:
        jsonschema.validate(instance=input, schema=LangchainTranslator.schema())
    except jsonschema.exceptions.ValidationError as e:
        # not Langchain
        logger.info(f"{e.message}")
        pass
    else:
        return LangchainTranslator(input)

    # default to plain
    json_str = json.dumps(input)
    return PlainTextTranslator(json_str)


def split_llm_hint(llm_hint: str) -> t.Tuple[str, str]:
    """
    Split llm hint into a tuple (provider and model name)
    :param llm_hint: llm hint str
    :return:
    """
    provider = None
    model = None
    if llm_hint:
        info = llm_hint.split(":", 1)
        # just get the provider right now
        provider = info[0]
        if len(info) > 1:
            model = info[1]
    return provider, model


def get_translator_with_hint(input: t.Any, llm_hint: str) -> Translator:
    """Get instance of translator

    :param input: can be a plain text string, or JSON struct
    :return Translator: LLM specific translator
    :raise ValidationError: input format not supported
    """
    # just get the provider right now, ignore model for now
    provider = split_llm_hint(llm_hint)[0]

    if provider == PlainTextTranslator.name() and isinstance(input, str):
        return get_translator_str_input(input)
    elif provider == OpenAiTranslator.name():
        # try gpt
        try:
            jsonschema.validate(instance=input, schema=OpenAiTranslator.schema())
        except jsonschema.exceptions.ValidationError as e:
            # not gpt
            logger.warning(f"Not {llm_hint}: {e.message}")
            return None
        else:
            return OpenAiTranslator(input)
    elif provider == GeminiTranslator.name():
        # try gemini
        try:
            jsonschema.validate(instance=input, schema=GeminiTranslator.schema())
        except jsonschema.exceptions.ValidationError as e:
            # not gemini
            logger.warning(f"Not {llm_hint}: {e.message}")
            return None
        else:
            return GeminiTranslator(input)
    elif provider == PangeaAiTranslator.name():
        # try pangea
        try:
            jsonschema.validate(instance=input, schema=PangeaAiTranslator.schema())
        except jsonschema.exceptions.ValidationError as e:
            # not pangea
            logger.warning(f"Not {llm_hint}: {e.message}")
            return None
        else:
            return PangeaAiTranslator(input)
    elif provider == AzureAiTranslator.name():
        # try azure
        try:
            jsonschema.validate(instance=input, schema=AzureAiTranslator.schema())
        except jsonschema.exceptions.ValidationError as e:
            # not azure
            logger.warning(f"Not {llm_hint}: {e.message}")
            return None
        else:
            return AzureAiTranslator(input)
    elif provider == AWSBedrockTranslator.name():
        # Try AWSBedrock
        try:
            jsonschema.validate(instance=input, schema=AWSBedrockTranslator.schema())
        except jsonschema.exceptions.ValidationError as e:
            # not AWSBedrock
            logger.warning(f"Not: {llm_hint}: {e.message}")
            return None
        else:
            return AWSBedrockTranslator(input)
    elif provider == ClaudeTranslator.name():
        # try claude
        try:
            jsonschema.validate(instance=input, schema=ClaudeTranslator.schema())
        except jsonschema.exceptions.ValidationError as e:
            # not claude
            logger.warning(f"Not {llm_hint}: {e.message}")
            return None
        else:
            return ClaudeTranslator(input)
    elif provider == CohereTranslator.name():
        # try cohere
        try:
            jsonschema.validate(instance=input, schema=CohereTranslator.schema())
        except jsonschema.exceptions.ValidationError as e:
            # not cohere
            logger.warning(f"Not {llm_hint}: {e.message}")
            return None
        else:
            return CohereTranslator(input)
    elif provider == DBRXTranslator.name():
        # try dbrx
        try:
            jsonschema.validate(instance=input, schema=DBRXTranslator.schema())
        except jsonschema.exceptions.ValidationError as e:
            # not dbrx
            logger.warning(f"Not {llm_hint}: {e.message}")
            return None
        else:
            return DBRXTranslator(input)
    elif provider == MistralTranslator.name():
        # try Mistral
        try:
            jsonschema.validate(instance=input, schema=MistralTranslator.schema())
        except jsonschema.exceptions.ValidationError as e:
            # not Mistral
            logger.warning(f"Not {llm_hint}: {e.message}")
            return None
        else:
            return MistralTranslator(input)
    elif provider == LangchainTranslator.name():
        # Try Langchain
        try:
            jsonschema.validate(instance=input, schema=LangchainTranslator.schema())
        except jsonschema.exceptions.ValidationError as e:
            # not Langchain
            logger.warning(f"Not {llm_hint}: {e.message}")
            return None
        else:
            return LangchainTranslator(input)
    logger.warning(f"{llm_hint} not supported")
    return None
