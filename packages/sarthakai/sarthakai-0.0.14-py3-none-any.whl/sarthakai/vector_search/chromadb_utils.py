from typing import List, Dict, Tuple
import chromadb
from chromadb.api.models import Collection
from slugify import slugify
from sarthakai.genai.tasks import route_query
from sarthakai.models import Chunk, VectorSearchResponse
from sarthakai.common import generate_random_id
from sarthakai.vector_search.common_utils import get_embedding_batch


def list_all_chromadb_collections(
    chromadir: str, to_return: str = "collection_objects"
) -> List[str] | List[Collection]:
    chromadb_client = chromadb.PersistentClient(path=chromadir)
    collections = chromadb_client.list_collections()

    if to_return == "collection_objects":
        return collections
    elif to_return == "names":
        return [collection.name for collection in collections]

    raise ValueError(
        "Invalid value for 'to_return'. Use 'collection_objects' or 'names'."
    )


def list_all_unique_values_of_metadata_key(
    chromadir: str, collection_name: str, metadata_key: str
) -> List[str]:
    chromadb_client = chromadb.PersistentClient(path=chromadir)
    collection = chromadb_client.get_collection(collection_name)

    all_metadatas = collection.get(include=["metadatas"]).get("metadatas", [])
    return list(set(metadata.get(metadata_key, "") for metadata in all_metadatas))


def get_or_create_chromadb_collection(
    chromadir: str, collection_name: str
) -> Tuple[bool, Collection]:
    chromadb_client = chromadb.PersistentClient(path=chromadir)
    collection_name = slugify(collection_name)

    existing_collections = [c.name for c in chromadb_client.list_collections()]
    collection_already_exists = collection_name in existing_collections

    collection = chromadb_client.get_or_create_collection(name=collection_name)
    return collection_already_exists, collection


def add_chunks_to_chromadb_collection(
    chunks: List[Chunk], collection: Collection
) -> None:
    # Determine whether to generate new embeddings or use existing ones
    embeddings = (
        [chunk.embedding for chunk in chunks]
        if all(chunk.embedding for chunk in chunks)
        else get_embedding_batch([chunk.text for chunk in chunks])
    )

    collection.add(
        embeddings=embeddings,
        documents=[chunk.text for chunk in chunks],
        ids=[generate_random_id() for _ in chunks],
        metadatas=[chunk.metadata_in_chromadb_format for chunk in chunks],
    )


def route_query_to_relevant_chromadb_collection(query: str, chromadir: str) -> str:
    all_collection_names = list_all_chromadb_collections(chromadir, to_return="names")
    return route_query(query=query, routes=all_collection_names)


def search_chromadb(
    chromadir: str,
    collection_name: str,
    query: str,
    n_results: int = 4,
    distance_threshold: float = 3.0,
    metadata_constraints: Dict[str, str] | None = None,
) -> List[VectorSearchResponse]:
    client = chromadb.PersistentClient(path=chromadir)
    collection = client.get_collection(collection_name)
    query_emb = get_embedding_batch([query])

    raw_search_results = collection.query(
        query_embeddings=query_emb,
        n_results=n_results,
        where=metadata_constraints,
    )

    vector_search_responses = [
        VectorSearchResponse(document=document, distance=distance, metadata=metadata)
        for document, distance, metadata in zip(
            raw_search_results.get("documents", [[]])[0],
            raw_search_results.get("distances", [[]])[0],
            raw_search_results.get("metadatas", [[]])[0],
        )
        if distance < distance_threshold
    ]

    return vector_search_responses


def two_step_vector_search(
    query: str,
    chromadir_1: str,
    collection_name_1: str,
    chromadir_2: str,
    collection_name_2: str,
    distance_threshold_1: float = 0.25,
    distance_threshold_2: float = 0.30,
) -> List[str]:
    # First step search
    articles_vector_search_responses = search_chromadb(
        chromadir=chromadir_1,
        collection_name=collection_name_1,
        query=query,
        distance_threshold=distance_threshold_1,
    )

    # Extract context documents
    context_documents = [
        response.metadata.get("text", "")
        for response in articles_vector_search_responses
    ]

    # If first search yields no results, proceed to second step
    if not articles_vector_search_responses:
        chunks_vector_search_responses = search_chromadb(
            chromadir=chromadir_2,
            collection_name=collection_name_2,
            query=query,
            distance_threshold=distance_threshold_2,
        )
        context_documents = [
            response.document for response in chunks_vector_search_responses
        ]

    return context_documents
