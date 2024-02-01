import numpy as np
import cv2
from utils import ocr_jpg_image, ocr_init

ocr_reader, onnx_session = ocr_init()
text=ocr_jpg_image(ocr_reader, onnx_session, "imgs/30_2.png")
print(text)