import os
import time
from typing import List
import cohere
from cohere.types.rerank_response import RerankResponse


def cohere_reranker(
    query: str, documents: List[str], top_n: int = 4, retries: int = 3
) -> List[str]:
    """
    Rerank documents based on relevance to the given query using Cohere's reranking model.
    """
    try:
        cohere_api_key: str = os.environ.get("COHERE_API_KEY", "")
        if not cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is not set.")

        cohere_client: cohere.Client = cohere.Client(cohere_api_key)
        reranked_response: RerankResponse = cohere_client.rerank(
            query=query, documents=documents, top_n=top_n, model="rerank-v3.5"
        )

        # Extract document indices from rerank results
        reranked_results = reranked_response.results
        reranked_documents: List[str] = [
            documents[result.index] for result in reranked_results
        ]

        return reranked_documents
    except Exception as e:
        print(f"Error during reranking: {e}")

        # Retry logic with exponential backoff
        if retries > 0:
            time.sleep(10)
            return cohere_reranker(
                query=query, documents=documents, top_n=top_n, retries=retries - 1
            )

        return []
