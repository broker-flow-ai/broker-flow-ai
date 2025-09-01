import os
import torch
import logging
from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import re

# Configurazione logging
logger = logging.getLogger(__name__)

# Modello fine-tuned per CORD (fatture/scontrini strutturati)
MODEL_NAME = "naver-clova-ix/donut-base-finetuned-cord-v2"
HF_TOKEN = os.getenv("HF_TOKEN")
HF_HOME = os.getenv("HF_HOME", "/root/.cache/huggingface")

# Imposta la cache HF
os.environ["HF_HOME"] = HF_HOME

try:
    logger.info("Caricamento modello DONUT...")
    processor = DonutProcessor.from_pretrained(MODEL_NAME, token=HF_TOKEN, use_fast=False)
    model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME, token=HF_TOKEN)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    logger.info("Modello caricato con successo.")
except Exception as e:
    logger.error(f"Errore nel caricare il modello: {e}")
    raise e

def extract_json_from_image(image: Image.Image):
    try:
        # Prompt task per parsing strutturato (CORD)
        task_prompt = "<s_cord-v2>"
        decoder_input_ids = processor.tokenizer(
            task_prompt, add_special_tokens=False, return_tensors="pt"
        ).input_ids

        pixel_values = processor(image, return_tensors="pt").pixel_values
        outputs = model.generate(
            pixel_values.to(device),
            decoder_input_ids=decoder_input_ids.to(device),
            max_length=512,
            pad_token_id=processor.tokenizer.pad_token_id,
            eos_token_id=processor.tokenizer.eos_token_id,
            use_cache=True,
            bad_words_ids=[[processor.tokenizer.unk_token_id]],
            return_dict_in_generate=True,
        )

        sequence = processor.batch_decode(outputs.sequences)[0]
        sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
        sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()

        try:
            result = processor.token2json(sequence)
        except Exception:
            result = {"raw_sequence": sequence}

        return result
    except Exception as e:
        logger.error(f"Errore durante estrazione: {e}")
        return {"error": str(e)}