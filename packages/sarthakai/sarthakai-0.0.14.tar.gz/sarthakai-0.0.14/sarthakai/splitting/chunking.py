from dotenv import load_dotenv
import nest_asyncio
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

from sarthakai.models import Chunk

# Load environment variables from a .env file
load_dotenv()

# Allow asyncio to run in Jupyter notebooks or nested loops
nest_asyncio.apply()

# Define a constant for the chunk size limit
CHUNK_SIZE_LIMIT: int = 1000


def chunk_text(document: str, text_size_limit: int) -> List[Chunk]:
    """
    Splits the given document into chunks of the specified size and returns a list of Chunk objects.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=text_size_limit,
        chunk_overlap=50,  # Ensure slight overlap between chunks to maintain context
        length_function=len,
    )

    # Split the document into text chunks
    texts: List[str] = text_splitter.split_text(document)

    # Wrap each text chunk into a Chunk object
    chunks: List[Chunk] = [Chunk(text=text) for text in texts]

    return chunks
