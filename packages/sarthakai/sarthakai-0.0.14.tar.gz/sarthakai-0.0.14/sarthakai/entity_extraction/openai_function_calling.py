import json
from openai import OpenAI
from typing import Dict, Any

# Initialize the OpenAI client
openai_client = OpenAI()


def extract_entities(
    text_document: str, response_model: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Extracts entities from a text document using an OpenAI model.
    """
    # Define the tool specifications for the model
    function_definitions = [
        {
            "type": "function",
            "function": {
                "name": "extract_info",
                "description": "Get the information from the body of the input text",
                "parameters": {"type": "object", "properties": response_model},
            },
        }
    ]

    # Prepare the user message for the model
    messages = [{"role": "user", "content": text_document}]

    # Make a request to the OpenAI chat completion endpoint
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=function_definitions
    )

    try:
        # Parse the tool call arguments from the response
        arguments = response.choices[0].message.tool_calls[0].function.arguments
        return json.loads(arguments)
    except (IndexError, AttributeError, json.JSONDecodeError) as e:
        # Handle any errors and log the response for debugging
        print(f"Error parsing response: {e}\nResponse: {response}")
        return {}
