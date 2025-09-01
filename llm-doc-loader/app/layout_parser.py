import torch
from transformers import AutoProcessor, AutoModelForTokenClassification
from PIL import Image
import pytesseract
import logging

logger = logging.getLogger(__name__)

MODEL_NAME = "nielsr/layoutlmv3-finetuned-funsd"
logger.info(f"Caricamento modello: {MODEL_NAME}")
processor = AutoProcessor.from_pretrained(MODEL_NAME, apply_ocr=False)
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)

def normalize_box(bbox, width, height):
    return [
        int(1000 * (bbox[0] / width)),
        int(1000 * (bbox[1] / height)),
        int(1000 * (bbox[2] / width)),
        int(1000 * (bbox[3] / height)),
    ]

def extract_invoice_fields_with_layoutlm(image: Image.Image) -> dict:
    logger.info("Inizio estrazione con LayoutLMv3...")
    # Dimensioni immagine
    width, height = image.size

    # OCR con Tesseract
    ocr_result = pytesseract.image_to_data(image, lang="ita", output_type=pytesseract.Output.DICT)
    words = []
    boxes = []

    for i in range(len(ocr_result["text"])):
        word = ocr_result["text"][i].strip()
        if word:
            x = ocr_result["left"][i]
            y = ocr_result["top"][i]
            w = ocr_result["width"][i]
            h = ocr_result["height"][i]
            bbox = [x, y, x + w, y + h]
            normalized_bbox = normalize_box(bbox, width, height)
            words.append(word)
            boxes.append(normalized_bbox)

    # Prepara input per LayoutLMv3
    encoding = processor(image, words, boxes=boxes, return_tensors="pt")

    # Predici
    with torch.no_grad():
        outputs = model(**encoding)
        predictions = torch.argmax(outputs.logits, dim=2)

    # Decodifica etichette
    labels = [model.config.id2label[p.item()] for p in predictions[0]]
    tokens = processor.tokenizer.convert_ids_to_tokens(encoding.input_ids[0])

    # Estrai campi
    invoice = {
        "cliente": None,
        "p_iva": None,
        "data": None,
        "totale": None,
        "iva": None,
        "righe": []
    }

    for label, token in zip(labels, tokens):
        if label.startswith("B-") or label.startswith("I-"):
            field = label.split("-")[1].lower()
            if field in invoice and invoice[field] is None:
                invoice[field] = token

    logger.info(f"Campi estratti: {invoice}")
    return invoice