import os
import requests
from typing import List, Optional, Union, Dict
import json

from sarthakai.genai.tasks import describe_table
from sarthakai.models import Chunk
from sarthakai.vector_search.common_utils import get_embedding_batch


def reducto_file_to_chunks(
    document_url: str, summarise_tables: bool = True, retries: int = 5
) -> List[Chunk]:
    """
    Parses a document using the Reducto API and returns a list of Chunk objects.
    """
    url: str = "https://platform.reducto.ai/parse"
    payload: dict = {
        "document_url": document_url,
        "options": {"table_summary": {"enabled": summarise_tables}},
        "advanced_options": {"table_output_format": "md", "merge_tables": True},
    }
    headers: dict = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {os.environ['REDUCTO_API_KEY']}",
    }

    try:
        response: requests.Response = requests.post(url, json=payload, headers=headers)
        result: dict = response.json()["result"]

        # Handle URL redirection for further parsing
        if result["type"] == "url":
            response = requests.get(result["url"])
            result = response.json()

        parsed_document: List[dict] = result["chunks"]
    except Exception as e:
        print(
            "ERROR IN REDUCTO",
            e,
            response.text if "response" in locals() else "No response",
        )
        if retries > 0:
            return reducto_file_to_chunks(
                document_url=document_url,
                summarise_tables=summarise_tables,
                retries=retries - 1,
            )
        return []

    all_document_chunks: List[Chunk] = []
    print("Reducto finished parsing document. Now preparing chunks.")

    for chunk in parsed_document:
        vectorisable_chunk_content: str = ""
        unvectorisable_chunk_content: str = ""
        chunk_bounding_boxes: List[dict] = []
        page_numbers: set[int] = set()

        for block in chunk.get("blocks", []):
            current_page_number: int = block.get("bbox", {}).get("page", 0)
            page_numbers.add(current_page_number)
            chunk_bounding_boxes.append(block.get("bbox", {}))

            if block.get("type") == "Table":
                table_content: str = block.get("content", "")
                vectorisable_chunk_content += describe_table(
                    table_to_describe=table_content
                )
                unvectorisable_chunk_content += table_content
            else:
                content: str = block.get("content", "")
                vectorisable_chunk_content += content
                unvectorisable_chunk_content += content

        embedding: Optional[List[float]] = get_embedding_batch(
            [vectorisable_chunk_content]
        )
        chunk_obj = Chunk(
            text=unvectorisable_chunk_content,
            bounding_boxes=chunk_bounding_boxes,
            file_source=document_url,
            page_numbers=list(page_numbers),
            embedding=embedding[0] if embedding else [],
        )
        all_document_chunks.append(chunk_obj)

    return all_document_chunks


def chunk_local_file_reducto(
    filename: str, chunk_size: Optional[int] = None
) -> Union[Dict, None]:
    """
    Chunks a local file using the Reducto API.
    """
    url = "https://api.reducto.ai/chunk_file?llm_table_summary=false&figure_summarization=false&no_chunk=false"
    if chunk_size:
        url += f"&chunk_size={chunk_size}"

    try:
        with open(filename, "rb") as file:
            files = {"document_file": (filename, file, "application/pdf")}
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {os.environ['REDUCTO_API_KEY']}",
            }
            response = requests.post(url, files=files, headers=headers)
            return json.loads(response.text)
    except Exception as e:
        print(f"Error while chunking file: {e}")
        return None


def chunk_file_by_url_reducto(
    document_url: str, chunk_size: Optional[int] = None
) -> Union[Dict, None]:
    """
    Chunks a file by URL using the Reducto API.
    """
    url = f"https://api.reducto.ai/chunk_url?llm_table_summary=false&document_url={document_url}"
    if chunk_size:
        url += f"&chunk_size={chunk_size}"

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {os.environ['REDUCTO_API_KEY']}",
    }
    try:
        response = requests.post(url, headers=headers)
        return json.loads(response.text)
    except Exception as e:
        print(f"Error while chunking URL: {e}")
        return None
