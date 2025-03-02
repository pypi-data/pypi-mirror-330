from pydantic import BaseModel
from typing import List, Dict, Union, Optional
from datetime import datetime


class Chunk(BaseModel):
    text: str
    non_vectorised_addendum_text: str = ""
    embedding: Optional[List[float]] = None
    page_numbers: Optional[List[int]] = None
    file_source: str = ""
    article_id: str = ""
    metadata: Optional[Dict[str, Union[str, datetime]]] = None
    bounding_boxes: Optional[List[Dict[str, Union[int, float]]]] = None

    @property
    def metadata_in_chromadb_format(self) -> Dict[str, Union[str, datetime]]:
        """
        Formats metadata for ChromaDB.
        """
        metadata = self.metadata or {}
        if self.non_vectorised_addendum_text:
            metadata["non_vectorised_addendum_text"] = self.non_vectorised_addendum_text
        if self.page_numbers:
            metadata["page_numbers"] = str(self.page_numbers)
        if self.file_source:
            metadata["file_source"] = self.file_source
        if self.bounding_boxes:
            metadata["bounding_boxes"] = str(self.bounding_boxes)
        metadata["format"] = "chromadb"
        return metadata

    @property
    def metadata_in_pinecone_format(self) -> Dict[str, Union[str, datetime]]:
        """
        Formats metadata for Pinecone.
        """
        metadata = self.metadata or {}
        if self.non_vectorised_addendum_text:
            metadata["non_vectorised_addendum_text"] = self.non_vectorised_addendum_text
        if self.page_numbers:
            metadata["page_numbers"] = str(self.page_numbers)
        if self.file_source:
            metadata["file_source"] = self.file_source
        if self.bounding_boxes:
            metadata["bounding_boxes"] = str(self.bounding_boxes)
        if self.text:
            metadata["text"] = str(self.text)
        metadata["format"] = "pinecone"
        return metadata


class VectorSearchResponse(BaseModel):
    document: str
    distance: float
    metadata: Optional[Dict[str, str]] = None


class WebSearchResponse(BaseModel):
    url: str
    title: str = ""
    snippet: str = ""
