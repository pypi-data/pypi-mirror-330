from typing import Dict


def split_markdown_by_section_headers(markdown_text: str) -> Dict[str, str]:
    sections: Dict[str, str] = {}
    current_section: str | None = None
    section_texts: list[str] = []

    # Split the markdown string by newlines
    lines: list[str] = markdown_text.split("\n")

    for line in lines:
        # Identify section headers (main headings starting with '# ')
        if line.startswith("# "):
            if current_section is not None:
                sections[current_section] = "\n".join(section_texts).strip()
                section_texts.clear()  # Reset for the next section
            current_section = line.lstrip("#").strip()
        elif line.strip():  # Add non-empty lines to the current section
            section_texts.append(line.strip())

    # Add the last section if it exists
    if current_section is not None:
        sections[current_section] = "\n".join(section_texts).strip()

    return sections
