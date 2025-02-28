import os
from typing import Optional
import aiohttp

from openai import OpenAI


async def call_llm_openai(config, prompt: str) -> str:
    """
    Calls OpenAI's completion/chat endpoint asynchronously.

    Args:
        prompt (str): The user prompt to send to the LLM.

    Returns:
        str: The LLM response text.
    """

    messages = []
    if config.system_prompt:
        messages.append({"role": "system", "content": config.system_prompt})
    messages.append({"role": "user", "content": prompt})

    client = OpenAI(api_key=config.api_key or os.environ["OPENAI_API_KEY"])

    completion = client.chat.completions.create(
        model=config.options["model"] or "gpt-4o-mini",
        messages=messages,
        temperature=config.options["temperature"],
    )

    try:
        return completion.choices[0].message.content
    except (KeyError, IndexError):
        return str(completion)


async def call_llm_ollama(config, prompt: str, url: Optional[str] = None) -> str:
    """
    Calls Ollama's completion/chat endpoint asynchronously.

    Args:
        prompt (str): The user prompt to send to the LLM.
        url (str): The URL of the Ollama server.

    Returns:
        str: The LLM response text.
    """
    # Default URL if none is provided
    if url is None:
        url = "http://localhost:11434"

    messages = []
    if config.system_prompt:
        messages.append({"role": "system", "content": config.system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": config.options.get("model", "default-model"),
        "prompt": str(messages),
        "stream": False,
    }

    valid_options = [
        "suffix",
        "images",
        "format",
        "options",
        "system",
        "template",
        "stream",
        "raw",
        "keep_alive",
        "context",
    ]
    for option in valid_options:
        if option in config.options:
            payload[option] = config.options[option]

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{url}/api/generate", json=payload) as response:
                if response.status == 200:
                    completion = await response.json()
                    return completion["response"]
                else:
                    return f"Error: {response.status}, {await response.text()}"
        except Exception as e:
            return f"Exception: {str(e)}"


async def call_llm_gpt4all(config, prompt: str, url: Optional[str] = None) -> str:
    """
    Calls GPT4ALL's completion/chat endpoint asynchronously.

    Args:
        prompt (str): The user prompt to send to the LLM.
        url (str): The URL of the GPT4ALL server.

    Returns:
        str: The LLM response text.
    """
    # Default URL if none is provided
    if url is None:
        url = "http://localhost:4891"  # Default GPT4ALL server URL

    messages = []
    if config.system_prompt:
        messages.append({"role": "system", "content": config.system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": config.options.get("model", "default-model"),
        "messages": messages,
    }

    # TODO - Expand options for OpenAI
    valid_options = ["max_tokens", "temperature"]
    for option in valid_options:
        if option in config.options:
            payload[option] = config.options[option]

    print(payload)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{url}/v1/chat/completions", json=payload
            ) as response:
                if response.status == 200:
                    completion = await response.json()
                    return (
                        completion.get("choices", [{}])[0]
                        .get("message", {})
                        .get("content", "")
                    )
                else:
                    return f"Error: {response.status}, {await response.text()}"
        except Exception as e:
            return f"Exception: {str(e)}"
