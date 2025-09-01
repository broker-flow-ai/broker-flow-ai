from transformers import AutoProcessor, AutoModelForTokenClassification

MODEL_NAME = "microsoft/layoutlmv3-base"

processor = AutoProcessor.from_pretrained(MODEL_NAME, apply_ocr=False)
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)
print("Modello caricato correttamente")
