from paddleocr import PaddleOCR
import cv2
import numpy as np

ocr = PaddleOCR(use_angle_cls=True, lang="it")

def extract_text_and_boxes(image: np.ndarray):
    result = ocr.ocr(image, cls=True)
    words = []
    boxes = []
    for line in result:
        for box in line:
            txt = box[1][0]
            coords = box[0]
            x_coords = [p[0] for p in coords]
            y_coords = [p[1] for p in coords]
            x_min, x_max = int(min(x_coords)), int(max(x_coords))
            y_min, y_max = int(min(y_coords)), int(max(y_coords))
            words.append(txt)
            boxes.append([x_min, y_min, x_max, y_max])
    return words, boxes