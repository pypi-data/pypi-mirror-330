import os
from typing import Any, Optional, Type
import instructor


def extract_entities(
    text_document: str,
    response_model: Type[Any],
    llm_provider: str = "openai",
    llm_name: str = "gpt-4o",
    retries: int = 5,
) -> Optional[Any]:
    """Uses Instructor to extract structured details from a large document."""
    try:
        # Initialize the LLM client based on the provider
        if llm_provider == "openai":
            from openai import OpenAI

            client = instructor.from_openai(
                OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            )
        elif llm_provider == "anthropic":
            from anthropic import Anthropic

            client = instructor.from_anthropic(
                Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")

        # Extract structured data from the text document using the chosen model
        instructor_result = client.chat.completions.create(
            model=llm_name,
            response_model=response_model,
            messages=[{"role": "user", "content": text_document}],
        )
        return instructor_result

    except Exception as e:
        print(f"Error during entity extraction: {e}")
        if retries > 0:
            return extract_entities(
                text_document=text_document,
                response_model=response_model,
                llm_provider=llm_provider,
                llm_name=llm_name,
                retries=retries - 1,
            )
        return None
