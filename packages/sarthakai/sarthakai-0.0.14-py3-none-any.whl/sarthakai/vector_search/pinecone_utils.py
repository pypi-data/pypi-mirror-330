import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Union, Tuple

from sarthakai.genai.tasks import route_query
from sarthakai.models import Chunk, VectorSearchResponse

from sarthakai.common import generate_random_id
from sarthakai.vector_search.common_utils import get_embedding_batch

# Load environment variables
load_dotenv()

# Constants
CHUNK_SIZE: int = 100000
PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)


def list_all_pinecone_indexes(
    to_return: str = "index_objects",
) -> Union[List[str], List[object]]:
    """List all Pinecone indexes, either as index objects or names."""
    all_indexes = pc.list_indexes()
    if to_return == "index_objects":
        return all_indexes
    elif to_return == "names":
        return [index.name for index in all_indexes]
    else:
        raise ValueError("Invalid value for to_return. Use 'index_objects' or 'names'.")


def list_all_namespaces_in_pinecone_index(pinecone_index_name: str) -> List[str]:
    """List all namespaces within a given Pinecone index."""
    pinecone_index = pc.Index(pinecone_index_name)
    return list(pinecone_index.describe_index_stats()["namespaces"].keys())


def get_or_create_pinecone_index(
    pinecone_index_name: str, dimension: int = 1536
) -> Tuple[bool, object]:
    """Retrieve or create a Pinecone index with the specified dimension."""
    try:
        pinecone_index = pc.Index(pinecone_index_name)
        return True, pinecone_index
    except Exception:
        pc.create_index(
            name=pinecone_index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        pinecone_index = pc.Index(pinecone_index_name)
        return False, pinecone_index


def add_chunks_to_pinecone_index(
    pinecone_index_name: str, namespace_name: str, chunks: List[Chunk]
) -> None:
    """Add chunks of data to a specified namespace within a Pinecone index."""
    pinecone_index = pc.Index(pinecone_index_name)
    vectors = [
        {
            "id": generate_random_id(),
            "values": chunk.embedding,
            "metadata": chunk.metadata_in_pinecone_format,
        }
        for chunk in chunks
    ]
    pinecone_index.upsert(namespace=namespace_name, vectors=vectors)


def route_query_to_relevant_pinecone_namespace(
    query: str, pinecone_index_name: str
) -> str:
    """Route a query to the most relevant namespace within a Pinecone index."""
    all_namespace_names = list_all_namespaces_in_pinecone_index(pinecone_index_name)
    return route_query(query=query, routes=all_namespace_names)


def search_pinecone(
    pinecone_index_name: str,
    namespace_name: str,
    query: str,
    n_results: int = 4,
    distance_threshold: float = 10.0,
    embedding_model: str = "text-embedding-3-small",
) -> List[VectorSearchResponse]:
    """Search a Pinecone index for the top N results matching a query."""
    index = pc.Index(pinecone_index_name)
    query_embedding = get_embedding_batch(input_array=[query], model=embedding_model)
    raw_search_results = index.query(
        vector=query_embedding,
        namespace=namespace_name,
        top_k=n_results,
        include_metadata=True,
    )["matches"]

    vector_search_responses: List[VectorSearchResponse] = []
    for search_result in raw_search_results:
        distance = 1 - search_result["score"]  # Convert similarity score to distance
        if distance < distance_threshold:
            vector_search_response = VectorSearchResponse(
                document=search_result["metadata"]["text"],
                distance=distance,
                metadata=search_result["metadata"],
            )
            vector_search_responses.append(vector_search_response)

    return vector_search_responses


def delete_pinecone_index(pinecone_index_name: str) -> None:
    """Delete a Pinecone index by name."""
    try:
        pc.delete_index(pinecone_index_name)
    except Exception as e:
        print(f"The index {pinecone_index_name} doesn't exist.", e)
