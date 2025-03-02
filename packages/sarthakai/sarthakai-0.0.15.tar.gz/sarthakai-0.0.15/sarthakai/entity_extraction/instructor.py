import os
from typing import Any, Optional, Type
import instructor


def extract_entities(
    text_document: str,
    response_model: Type[Any],
    llm_provider: str = "openai",
    llm_name: str = "",
    retries: int = 5,
) -> Optional[Any]:
    """Uses Instructor to extract structured details from a large document."""
    try:
        # Initialize the LLM client based on the provider
        if llm_provider == "openai":
            from openai import OpenAI

            llm_name = llm_name or "gpt-4o"
            client = instructor.from_openai(
                OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            )
            # Extract structured data from the text document using the chosen model
            instructor_result = client.chat.completions.create(
                model=llm_name,
                response_model=response_model,
                messages=[{"role": "user", "content": text_document}],
            )
        elif llm_provider == "anthropic":
            from anthropic import Anthropic

            client = instructor.from_anthropic(
                Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
            )
            # Extract structured data from the text document using the chosen model
            instructor_result = client.chat.completions.create(
                model=llm_name,
                response_model=response_model,
                messages=[{"role": "user", "content": text_document}],
            )
        elif llm_provider == "google":
            import google.generativeai as genai

            llm_name = llm_name or "models/gemini-1.5-flash-latest"
            # Initialize the client
            client = instructor.from_gemini(
                client=genai.GenerativeModel(
                    model_name=llm_name,
                )
            )
            # Extract structured data from the text document using the chosen model
            instructor_result = client.chat.completions.create(
                response_model=response_model,
                messages=[{"role": "user", "content": text_document}],
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")

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
