import os
from typing import Union, List, Dict
from llama_parse import LlamaParse
from dotenv import load_dotenv
import nest_asyncio

from sarthakai.splitting.chunking import chunk_text
from sarthakai.entity_extraction.tables import extract_tables_from_markdown_text
from sarthakai.genai.tasks import describe_table
from sarthakai.models import Chunk

# Apply nested asyncio and load environment variables
nest_asyncio.apply()
load_dotenv()


def llamaparse_file_to_md(
    file_path: str, additional_parsing_instructions: str = "", by_page: bool = False
) -> Union[str, List[Dict[str, Union[str, int]]]]:
    """Uses LlamaParse to parse a local document into markdown."""
    llamaparse_api_key: str = os.getenv("LLAMA_CLOUD_API_KEY", "")

    parser = LlamaParse(
        api_key=llamaparse_api_key,
        parsing_instruction=additional_parsing_instructions,
        result_type="markdown",  # Options: "markdown" or "text"
    )

    documents = parser.load_data(file_path)

    if by_page:
        return [
            {"text": document.text, "page_no": i + 1}
            for i, document in enumerate(documents)
        ]

    return "".join(document.text for document in documents)


def parse_document_with_tables(
    document_file_path: str, document_filename: str
) -> List[Chunk]:
    """Parses a document, extracting tables and splitting remaining text into chunks."""
    all_documents_chunks: List[Chunk] = []
    additional_parsing_instructions: str = (
        "Parse the tables in a markdown format carefully so that no columns are empty and no headers are empty."
    )

    parsed_md_document: Union[str, List[Dict[str, Union[str, int]]]] = (
        llamaparse_file_to_md(
            file_path=document_file_path,
            additional_parsing_instructions=additional_parsing_instructions,
        )
    )

    tables: List[str]
    remaining_parsed_md_document: str
    tables, remaining_parsed_md_document = extract_tables_from_markdown_text(
        md_document=parsed_md_document, reformat_tables_with_llm=True
    )

    print(f"{len(tables)} tables detected.")

    for table in tables:
        table_description: str = describe_table(table)
        table_chunk = Chunk(
            text=table_description,
            non_vectorised_addendum_text=table,
            file_source=document_filename,
        )
        all_documents_chunks.append(table_chunk)

    chunks: List[Chunk] = chunk_text(
        document_text=remaining_parsed_md_document, file_source=document_filename
    )

    all_documents_chunks.extend(chunks)
    return all_documents_chunks
