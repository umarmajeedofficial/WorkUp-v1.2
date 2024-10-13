# functions/utils.py

import os
import tempfile
from typing import Optional
import PyPDF2
import docx
import streamlit as st
import re  # Import regex for sanitizing filenames


def extract_text_from_pdf(file) -> str:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def extract_text_from_docx(file) -> str:
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def extract_text(file) -> Optional[str]:
    try:
        if file.type == "application/pdf":
            return extract_text_from_pdf(file)
        elif file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                           "application/msword"]:
            return extract_text_from_docx(file)
        elif file.type.startswith("text/"):
            return file.getvalue().decode("utf-8")
        else:
            st.error("Unsupported file type.")
            return None
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")
        return None


def sanitize_filename(name: str) -> str:
    """
    Removes or replaces invalid characters from a filename.

    Args:
        name (str): The original filename.

    Returns:
        str: The sanitized filename.
    """
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    return re.sub(r'[^\w\-]', '_', name)
