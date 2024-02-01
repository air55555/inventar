import cv2
import onnxruntime
import easyocr
import numpy as np
# Load the OCR model


def ocr_init():
    ocr_reader = easyocr.Reader('ru')


def ocr_jpg_image(ocr_reader,image_path):

    text = ocr_reader.readtext(image_path)
    return text

