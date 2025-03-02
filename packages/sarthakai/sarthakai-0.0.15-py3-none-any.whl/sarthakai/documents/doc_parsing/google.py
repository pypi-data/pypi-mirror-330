import os
import google.generativeai as genai
import time
from google.ai.generativelanguage_v1beta.types.file import File


def push_file_to_google_gemini(file_path: str) -> str:
    """Uses Google Gemini to parse a local document into markdown."""
    # Upload the PDF
    file = genai.upload_file(file_path)

    # Wait for file to finish processing
    while file.state != File.State.ACTIVE:
        time.sleep(1)
        file = genai.get_file(file.name)
        print(f"File is still uploading, state: {file.state}")

    print(f"File is now active, state: {file.state}")
    return file
