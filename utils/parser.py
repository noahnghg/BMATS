import pdfplumber
from typing import Union, BinaryIO

def extract_text_from_pdf(pdf_file: Union[str, BinaryIO]) -> str:
    """
    Extracts text from a given PDF file path or file-like object.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""
    
    return text.strip()
