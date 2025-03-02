from sarthakai.genai.tasks import reformat_table


def extract_tables_from_markdown_text(
    md_document: str, reformat_tables_with_llm: bool = False
) -> tuple[list[str], str]:
    lines: list[str] = md_document.splitlines()
    tables: list[str] = []
    table: list[str] = []
    non_table_text: list[str] = []
    consecutive_pipe_lines: int = 0
    min_consecutive_lines: int = (
        3  # Minimum consecutive lines with pipes to classify as a table
    )

    for line in lines:
        if (
            "|" in line
        ):  # Check if the line contains a pipe symbol, indicating a potential table row
            table.append(line)
            consecutive_pipe_lines += 1
        else:
            # If a block of table rows ends, validate and store the table
            if consecutive_pipe_lines >= min_consecutive_lines:
                tables.append("\n".join(table))
            # Reset table tracking
            table.clear()
            consecutive_pipe_lines = 0
            # Collect non-table text
            non_table_text.append(line)

    # Final check for a valid table at the end of the document
    if consecutive_pipe_lines >= min_consecutive_lines:
        tables.append("\n".join(table))

    non_table_text_str: str = "\n".join(non_table_text).strip()

    if reformat_tables_with_llm:
        tables = [reformat_table(table_to_reformat=table) for table in tables]

    return tables, non_table_text_str
