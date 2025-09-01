import logging
import os
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
from io import BytesIO
from app.ocr_layer import extract_text_and_boxes
from app.document_ai_layer import classify_layout
from app.llm_layer import extract_invoice_fields_with_llm

# Setup logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/process-document/")
async def process_document(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File non valido. Carica un'immagine.")

    try:
        image_pil = Image.open(BytesIO(await file.read())).convert("RGB")
        image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        logger.info("Immagine caricata correttamente.")
    except Exception as e:
        logger.error(f"Errore nell'aprire l'immagine: {e}")
        raise HTTPException(status_code=400, detail="Immagine non valida.")

    try:
        # Layer 1: OCR
        words, boxes = extract_text_and_boxes(image_cv)
        logger.info(f"OCR completato: {len(words)} parole estratte.")

        # Layer 2: Document AI
        labels = classify_layout(image_pil, words, boxes)
        logger.info(f"Layout classificato: {len(labels)} etichette.")

        # Layer 3: LLM reale
        invoice = extract_invoice_fields_with_llm(words, labels)
        logger.info(f"Campi estratti con LLM: {invoice}")

        return {
            "document_type": "Fattura (multilayer + LLM)",
            "extracted_data": invoice
        }
    except Exception as e:
        logger.error(f"Errore durante il processamento: {e}")
        raise HTTPException(status_code=500, detail="Errore durante l'elaborazione del documento.")

@app.get("/")
def read_root():
    return {"message": "LLM Document Loader API. Usa /process-document/ per analisi."}