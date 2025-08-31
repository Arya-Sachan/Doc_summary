\
"""
Text extraction utilities for PDF and Image files.
"""
from io import BytesIO
from typing import Optional
from PIL import Image
import pytesseract

def extract_text_from_pdf(file) -> str:
    """
    Extract text from a PDF using PyPDF2.
    Note: This will not OCR scanned PDFs in this minimal version.
    """
    try:
        import PyPDF2
    except ImportError as e:
        raise RuntimeError("PyPDF2 is required to read PDFs. Please install it.") from e

    reader = PyPDF2.PdfReader(file)
    texts = []
    for page in reader.pages:
        try:
            t = page.extract_text() or ""
        except Exception:
            t = ""
        if t:
            texts.append(t)
    return "\n".join(texts)

def extract_text_from_image(file) -> str:
    """
    OCR text extraction for images using pytesseract.
    """
    image = Image.open(file)
    # Convert to RGB to avoid mode issues
    if image.mode != "RGB":
        image = image.convert("RGB")
    text = pytesseract.image_to_string(image)
    return text or ""
