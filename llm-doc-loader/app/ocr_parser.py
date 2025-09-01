import pytesseract
from PIL import Image
import re

def extract_text_with_ocr(image: Image.Image) -> str:
    # Converti in grayscale per migliorare OCR
    image = image.convert("L")
    return pytesseract.image_to_string(image, lang="ita")

def parse_invoice_fields(ocr_text: str) -> dict:
    lines = ocr_text.splitlines()
    invoice = {
        "cliente": None,
        "indirizzo": None,
        "p_iva": None,
        "data": None,
        "numero_fattura": None,
        "totale": None,
        "iva": None,
        "righe": []
    }

    # Regex per campi comuni
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if "cliente" in line.lower() or "spett.le" in line.lower():
            invoice["cliente"] = line
        elif "indirizzo" in line.lower():
            invoice["indirizzo"] = line
        elif "p.iva" in line.lower() or "partita iva" in line.lower():
            invoice["p_iva"] = re.findall(r"[\d\.]+", line)
        elif "data" in line.lower():
            invoice["data"] = re.findall(r"\d{2}/\d{2}/\d{4}", line)
        elif "totale" in line.lower():
            invoice["totale"] = re.findall(r"[\d,\.]+", line)
        elif "iva" in line.lower():
            invoice["iva"] = re.findall(r"[\d,\.]+", line)

    return invoice