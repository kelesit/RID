from typing import Callable, List, Tuple, Dict
import os
import pdfplumber
import re


def merge_hyphenated_words(text: str) -> str:
    """
    Merges hyphenated words that were split across lines.

    :param text: The text to clean.
    :return: The cleaned text.
    """
    return re.sub(r"(\w)-\n(\w)", r"\1\2", text)


def fix_newlines(text: str) -> str:
    """
    Fixes newlines that were split across lines.

    :param text: The text to clean.
    :return: The cleaned text.
    """
    return re.sub(r"(?<!\n)\n(?!\n)", " ", text)


def remove_multiple_newlines(text: str) -> str:
    """
    Removes multiple newlines.

    :param text: The text to clean.
    :return: The cleaned text.
    """
    return re.sub(r"\n{2,}", "\n", text)


def extract_pages_from_pdf(file_path: str):
    """
    Extracts the pages the PDF.

    :param file_path: The path to the PDF file.
    :return: A list of tuples containing the page number and the extracted text.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    cleaning_functions = [
        merge_hyphenated_words,
        fix_newlines,
        remove_multiple_newlines,
    ]
    with pdfplumber.open(file_path) as pdf:
        pages = []
        for page_num, page in enumerate(pdf.pages):
            raw_text = page.dedupe_chars(tolerance=1).extract_text()
            for cleaning_function in cleaning_functions:
                text = cleaning_function(raw_text).replace("\n", " ")
            if text.strip():  # Check if extracted text is not empty
                pages.append((page_num + 1, text))
        pdf.close()
    return pages


if __name__ == "__main__":
    file = "data/april-2023.pdf"
    pages = extract_pages_from_pdf(file)
    print(pages)
