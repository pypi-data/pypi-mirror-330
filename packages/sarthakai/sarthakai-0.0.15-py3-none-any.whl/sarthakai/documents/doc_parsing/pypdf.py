import PyPDF2
from typing import List, Dict, Union


def pdf2chunks(
    filename: str, split_by: str = "paragraphs"
) -> List[Dict[str, Union[str, int]]]:
    """Breaks down a local PDF file into smaller chunks."""
    reader = PyPDF2.PdfReader(filename)
    chunks: List[Dict[str, Union[str, int]]] = []

    for page_number in range(len(reader.pages)):
        # Extract text from each page and remove line breaks
        page_text: str = reader.pages[page_number].extract_text().replace("\n", " ")

        if split_by == "pages":
            chunks.append(
                {"document": page_text, "location": page_number, "source": filename}
            )
        elif split_by == "paragraphs":
            docs_long: List[str] = page_text.split("\n")
            docs: List[str] = []
            substring_length: int = 1000

            # Split long paragraphs into smaller chunks
            for doc in docs_long:
                if len(doc) <= substring_length:
                    docs.append(doc)
                else:
                    docs.extend(
                        doc[i : i + substring_length]
                        for i in range(0, len(doc), substring_length)
                    )

            # Only add non-trivial chunks
            for doc in docs:
                if len(doc) > 64:
                    chunks.append(
                        {"document": doc, "location": page_number, "source": filename}
                    )

    return chunks
