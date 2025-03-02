from openai import OpenAI
from typing import List, Tuple

from sarthakai.models import Chunk
from sarthakai.genai.llm import llm_call
from sarthakai.genai.prompts import QuestionAnsweringSystemPrompt

openai_client = OpenAI()


def get_embedding_batch(
    input_array: List[str], model: str = "text-embedding-3-large"
) -> List[List[float]]:
    """
    Generates embeddings for a batch of input strings using the specified model.
    """
    batch_size: int = 1000
    embeddings_list: List[List[float]] = []

    # Ensure no empty strings cause issues by replacing them with a space
    input_array = [" " if item == "" else item for item in input_array]

    for i in range(0, len(input_array), batch_size):
        try:
            array_subset: List[str] = input_array[i : i + batch_size]
            response = openai_client.embeddings.create(input=array_subset, model=model)
            embeddings_list.extend(i.embedding for i in response.data)
        except Exception as e:
            print(f"Error processing batch {i // batch_size}: {e}")
            break

    return embeddings_list


def answer_question(query: str, context_documents: List[str]) -> str:
    """
    Answers a question based on provided context documents using LLM.
    """
    question_answering_system_prompt = QuestionAnsweringSystemPrompt(
        context_documents=context_documents
    )
    compiled_prompt: str = question_answering_system_prompt.compile()

    messages = [
        {"role": "system", "content": compiled_prompt},
        {"role": "user", "content": query},
    ]

    llm_response: str = llm_call(messages)
    return llm_response


def filter_document_search_results_llm(
    user_prompt: str, search_results: List[Chunk]
) -> Tuple[str, List[Chunk]]:
    """
    Filters document search results using LLM to find the most relevant documents.
    """
    chunk_size: int = 100
    relevant_docs: str = ""

    for i in range(0, len(search_results), chunk_size):
        chunk: List[Chunk] = search_results[i : i + chunk_size]
        system_prompt: str = """Out of the following documents, return only those which are absolutely necessary to answer the user's question.
        Return your answer as a bulleted list in new lines. If none of the documents is relevant, return 'NONE'."""

        for doc in chunk:
            system_prompt += f"\n- {doc['document']}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        llm_response: str = llm_call(messages)

        if "NONE" in llm_response:
            break

        relevant_docs += llm_response

    return relevant_docs, search_results
