import cv2
import os
import easyocr
import numpy as np
import sqlite3
import uuid
from datetime import datetime
from flask import  jsonify
DATABASE_INV_NUM = 'db/imgs.db'
UPLOAD_FOLDER = 'uploads/'

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


DATABASE = 'imgs.db'


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
# def search_by_inv_num(inv_to_search):
#     conn = sqlite3.connect(DATABASE_INV_NUM)
#     cursor = conn.cursor()
#
#     # Search for records with the given inv
#     cursor.execute("SELECT * FROM records WHERE inv = ?", (inv_to_search,))
#     records = cursor.fetchall()
#
#     conn.close()
#
#     if not records:
#         return jsonify({"message": "No records found for the provided inv"}), 404
#
#     # Convert records to a list of dictionaries for better serialization
#     records_dict = [{"uuid": record[0], "timestamp": record[1], "inv": record[2], "desc": record[3]} for record in
#                     records]
#
#     return jsonify(records_dict)


# def parse_inv_num(text):
#     """
#     parse inv_num from dusty text. Return exact, clear inv_num
#
#     """
#     numbers = []
#     current_number = ""
#     started_number = False
#
#     for char in text:
#         if char.isdigit():
#             started_number = True
#             current_number += char
#         elif started_number:
#             if current_number.startswith("013") \
#                     or current_number.startswith("72")\
#                     or current_number.startswith("71"):
#                 numbers.append(int(current_number))
#             current_number = ""
#             started_number = False
#
#     # Check for the last number in the string
#     if started_number and (current_number.startswith("013")
#                            or current_number.startswith("72")
#                             or current_number.startswith("71")):
#         numbers.append(int(current_number))
#
#     return numbers


def upload_file(image):

    # # Check if the request contains the file
    # if 'file' not in request.files:
    #     return jsonify({"error": "No file part"}), 400
    #
    # file = request.files['file']
    #
    # # Check if the file is empty
    # if file.filename == '':
    #     return jsonify({"error": "No selected file"}), 400

    # Generate a unique ID for the file
    file_uuid = str(uuid.uuid4())

    # Save the file with the unique ID as the filename
    file_path = os.path.join(UPLOAD_FOLDER, f"{file_uuid}.jpg")
    cv2.imwrite(file_path, image)

    # Record the file information in the database
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    inv = "111"#request.form.get('inv')  # Assuming inv is provided in the form
    desc = "good apparat"#request.form.get('desc')  # Assuming desc is provided in the form

    conn = sqlite3.connect(DATABASE_INV_NUM)
    cursor = conn.cursor()

    # Insert the record into the database
    cursor.execute("INSERT INTO uploads (uuid, timestamp, inv_num, desc) VALUES (?, ?, ?, ?)",
                   (file_uuid, timestamp, inv, desc))

    conn.commit()
    conn.close()

    return file_path
        #jsonify({"uuid": file_uuid, "status": "File uploaded successfully"}), 201

def search_by_inv_num(inv_to_search, database_path=DATABASE_INV_NUM):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Search for records with the given inv
    cursor.execute("SELECT * FROM records WHERE inv_num = ?", (inv_to_search,))
    records = cursor.fetchall()
    records_dict = [
        {"uuid": record[0], "timestamp": record[1], "inv": record[2], "desc": record[3]}
        for record in records
    ]


    if not records:
          # No records found for the provided inv

        #return "test" record if not founnd for testing cyrillic in db, etc
        #cursor.execute("SELECT * FROM records WHERE inv_num = ?", ('test',))
        #records = cursor.fetchall()

        records_dict = [
            {"uuid": "No", "timestamp":"No", "inv": inv_to_search, "desc": "----NO INVENTAR NUM---"}]


    conn.close()
    # Convert records to a list of dictionaries for better serialization


    # return string
    return (str(records_dict))

        #.encode('utf-8').decode('unicode_escape')

def extract_inv_strings(text):
    """
    Extract strings from the text that start with "013", "72", or "71" and consider leading zeroes.

    """
    extracted_strings = []

    current_string = ""
    started_string = False

    for char in text:
        if char.isdigit() or char.isalpha():
            current_string += char
            started_string = True
        elif started_string:
            if current_string.startswith(("013", "72", "71")):
                extracted_strings.append(current_string)
            current_string = ""
            started_string = False

    # Check for the last string in the text
    if started_string and current_string.startswith(("013", "72", "71")):
        extracted_strings.append(current_string)

    return extracted_strings

