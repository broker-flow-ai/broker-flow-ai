import torch
from transformers import AutoProcessor, AutoModelForTokenClassification
from PIL import Image

MODEL_NAME = "microsoft/layoutlmv3-base"
processor = AutoProcessor.from_pretrained(MODEL_NAME, apply_ocr=False)
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)

def normalize_box(bbox, width, height):
    return [
        int(1000 * (bbox[0] / width)),
        int(1000 * (bbox[1] / height)),
        int(1000 * (bbox[2] / width)),
        int(1000 * (bbox[3] / height)),
    ]

def classify_layout(image: Image.Image, words: list, boxes: list):
    width, height = image.size
    normalized_boxes = [normalize_box(box, width, height) for box in boxes]
    encoding = processor(image, words, boxes=normalized_boxes, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**encoding)
        predictions = torch.argmax(outputs.logits, dim=2)

    labels = [model.config.id2label[p.item()] for p in predictions[0]]
    return labels