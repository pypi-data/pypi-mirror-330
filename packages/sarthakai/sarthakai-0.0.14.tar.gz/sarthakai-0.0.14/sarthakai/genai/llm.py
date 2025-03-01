import os
import requests
import json
import tiktoken
from litellm import completion, acompletion
from openai import OpenAI
from typing import List, Dict, Union, Optional

# Constants
MILLION: int = 1_000_000
SONNET_MODEL_NAME: str = "claude-3-5-sonnet-20240620"
DEFAULT_LLM: str = "gpt-4o-mini"

# Pricing details in USD per token
pricing_usd: Dict[str, Dict[str, float]] = {
    "gpt-3.5-turbo": {"input": 0.50 / MILLION, "output": 1.50 / MILLION},
    "gpt-4o": {"input": 5 / MILLION, "output": 15 / MILLION},
    "gpt-4o-mini": {"input": 0.15 / MILLION, "output": 0.60 / MILLION},
}


def llm_call(messages: List[Dict[str, str]], model: str = DEFAULT_LLM) -> str:
    """
    Calls a language model to generate a response.
    """
    response = completion(model=model, messages=messages)
    return response.choices[0].message.content


async def async_llm_call(
    messages: List[Dict[str, str]], model: str = DEFAULT_LLM
) -> str:
    """
    Asynchronously calls a language model to generate a response.
    """
    response = await acompletion(model=model, messages=messages)
    return response.choices[0].message.content


def num_tokens_from_messages(
    messages: List[Dict[str, str]], model: str = DEFAULT_LLM
) -> int:
    """
    Calculates the number of tokens used by a list of messages.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4
        tokens_per_name = -1
    elif "gpt-3.5-turbo" in model:
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model or "omni" in model:
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"num_tokens_from_messages() is not implemented for model {model}."
        )

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name

    num_tokens += 3  # Account for assistant's primed reply
    return num_tokens
