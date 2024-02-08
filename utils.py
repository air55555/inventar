import cv2

import easyocr
import numpy as np
import sqlite3
import uuid
from datetime import datetime


def ocr_init():
    # Load the OCR model

    ocr_reader = easyocr.Reader(["ru"])
    return ocr_reader

def ocr_jpg_image(ocr_reader,image_path):

    text = ocr_reader.readtext(image_path)
    return text

def combine_texts(data):
    # Extract text from each tuple
    texts = [item[1] for item in data]

    # Combine texts into a multiline string
    multiline_text = '\n'.join(texts)

    return multiline_text


DATABASE = 'inventar_data.db'


# Helper function to create the table
def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            uuid TEXT PRIMARY KEY,
            timestamp TEXT,
            inv_num TEXT,
            desc TEXT
        )
    ''')

    conn.commit()
    conn.close()


# Create the table when the application starts


