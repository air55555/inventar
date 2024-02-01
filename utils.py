import cv2
import onnxruntime
import easyocr
import numpy as np
# Load the OCR model


def ocr_init():
    ocr_reader = easyocr.Reader(['en'])

    # Load the ONNX model
    onnx_model_path = 'DenseNet_CTC.onnx'
    onnx_session = onnxruntime.InferenceSession(onnx_model_path)
    return ocr_reader, onnx_session

def ocr_jpg_image(ocr_reader,onnx_session,image_path):
    # Read the image using OpenCV
    img = cv2.imread(image_path)

    # Preprocess the image (you might need to adjust this based on your model)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (128, 32))  # Assuming your model expects this size

    # Add batch dimension and normalize
    input_data = np.expand_dims(img.astype(np.float32) / 255.0, axis=0)

    # Run inference
    input_name = onnx_session.get_inputs()[0].name
    output_name = onnx_session.get_outputs()[0].name
    result = onnx_session.run([output_name], {input_name: input_data})

    # Post-process the output (you might need to adjust this based on your model)
    output = result[0].squeeze().argmax(axis=1)
    text = ocr_reader.recognize(img)

    return text


# Example usage
# image_path = 'path/to/your/image.jpg'
# result = ocr_jpg_image(image_path)
# print("OCR Result:", result)