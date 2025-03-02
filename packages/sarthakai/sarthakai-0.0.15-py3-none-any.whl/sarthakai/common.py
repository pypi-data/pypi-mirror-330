import json
import re
import string
import random
from rapidfuzz import fuzz, process
from typing import List, Optional


def generate_random_id(k: int = 48) -> str:
    """
    Generate a random string of length `k` using ASCII letters.
    """
    return "".join(random.choices(string.ascii_letters, k=k))


def fuzzy_match_term_against_list_of_terms(
    term: str, ground_truths: List[str], threshold: int = 80
) -> Optional[str]:
    """
    Perform fuzzy matching of `term` against a list of `ground_truths`.
    Returns the best match if its score meets or exceeds the `threshold`.
    """
    if not ground_truths:
        raise ValueError("List `ground_truths` cannot be empty.")

    terms_and_matching_scores = process.extract(
        term.lower(),
        ground_truths,
        scorer=fuzz.partial_ratio,
        limit=2,
    )

    matches = [
        term for term, score, _ in terms_and_matching_scores if score >= threshold
    ]
    return matches[0] if matches else None


def parse_json_from_llm_response(llm_response: str) -> dict:
    """
    Parse JSON from an LLM-generated response, removing code block markers and comments.
    """
    cleaned_response = re.sub(
        r"```json|```", "", llm_response
    )  # Remove code block markers
    cleaned_response = re.sub(
        r"//.*?$|/\*.*?\*/", "", cleaned_response, flags=re.MULTILINE | re.DOTALL
    )  # Remove comments
    return json.loads(cleaned_response)
