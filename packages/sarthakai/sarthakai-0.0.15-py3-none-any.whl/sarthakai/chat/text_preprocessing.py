from typing import List, Dict, Any


def trim_llm_messages_history(
    messages: List[Dict[str, Any]], max_length: int = 4096
) -> List[Dict[str, Any]]:
    """Recursively trims the message history until its combined content length is within the max limit."""
    content_length = sum(len(str(message["content"])) for message in messages)
    if content_length > max_length:
        return trim_llm_messages_history(messages[1:], max_length)
    return messages
