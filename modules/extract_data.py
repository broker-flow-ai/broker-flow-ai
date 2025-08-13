import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import os

def is_pdf_scanned(path):
    reader = PdfReader(path)
    for page in reader.pages:
        if '/Font' in page['/Resources']:
            return False
    return True

def extract_text_from_pdf(path):
    if is_pdf_scanned(path):
        return ocr_pdf(path)
    else:
        return extract_text_digital(path)

def extract_text_digital(path):
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])

def ocr_pdf(path):
    pages = convert_from_path(path)
    text = ""
    for image in pages:
        text += pytesseract.image_to_string(image)
    return text