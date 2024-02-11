# unittests for inventar app
import os
import unittest
from flask import Flask, json
from app import app
import cv2
import sqlite3
from utils import search_by_inv_num
from utils import ocr_init, ocr_jpg_image, combine_texts

class TestYourApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        # Assuming DATABASE_INV_NUM is the path to your test database
        self.test_db_path = 'db/imgs.db'

    def tearDown(self):
        pass

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "Server OK")

    def test_upload_file(self):
        # Assuming you have an image file for testing in the same directory as your test file
        image_path = 'imgs/real_apparatus/photo_7_2024-02-10_09-35-05.jpg'
        with open(image_path, 'rb') as image_file:
            image = cv2.imread(image_path)
            _, img_encoded = cv2.imencode("imgs/rus_text_encoded.png", image)
            image_bytes = img_encoded.tobytes()

            response = self.app.post(
                '/inv_num',
                data=image_bytes
            )

        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertGreater(len(text), 0)
        self.assertIn('01301909', text)
        self.assertIn('омп', text)
        # Check if the response contains certain symbols
        #expected_symbols = ['01301909', 'омп']
        #for symbol in expected_symbols:

class TestSearchByInvNum(unittest.TestCase):
    def setUp(self):
        # Assuming you have a test database
        self.test_db_path = 'db/imgs.db'
        #self.create_test_table()

    def tearDown(self):
        # Clean up after the test
        pass
        #self.drop_test_table()


    def test_search_by_inv_num_found(self):
        inv_to_search = '01301909'
        result = search_by_inv_num(inv_to_search, self.test_db_path)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['uuid'], '555')
        self.assertEqual(result[0]['timestamp'], '55555')
        self.assertEqual(result[0]['inv'], '01301909')
        self.assertEqual(result[0]['desc'], 'комплект устройств технологических')

    def test_search_by_inv_num_not_found(self):
        inv_to_search = 'INVXYZ'
        result = search_by_inv_num(inv_to_search, self.test_db_path)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()


    # def create_test_table(self):
    #     conn = sqlite3.connect(self.test_db_path)
    #     cursor = conn.cursor()
    #     cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS records (
    #             uuid TEXT PRIMARY KEY,
    #             timestamp TEXT,
    #             inv_num TEXT,
    #             desc TEXT
    #         )
    #     ''')
    #     # Insert some sample data
    #     cursor.executemany('''
    #         INSERT INTO records (uuid, timestamp, inv_num, desc)
    #         VALUES (?, ?, ?, ?)
    #     ''', [
    #         ('1', '2022-01-01 12:00:00', 'INV001', 'Description 1'),
    #         ('2', '2022-01-02 12:00:00', 'INV002', 'Description 2'),
    #         ('3', '2022-01-03 12:00:00', 'INV003', 'Description 3'),
    #     ])
    #     conn.commit()
    #     conn.close()
    #
    # def drop_test_table(self):
    #     conn = sqlite3.connect(self.test_db_path)
    #     cursor = conn.cursor()
    #     cursor.execute('DROP TABLE IF EXISTS records')
    #     conn.commit()
    #     conn.close()\

    #     self.assertTrue(any(symbol in item[1] for item in text))
    #
    # def test_search_by_inv_num(self):
    #     # Insert some test data into the test database
    #     conn = sqlite3.connect(self.test_db_path)
    #     cursor = conn.cursor()
    #     cursor.execute("INSERT INTO records (uuid, timestamp, inv, desc) VALUES (?, ?, ?, ?)",
    #                    ('test_uuid', '2022-01-01 12:00:00', 'test_inv', 'test_desc'))
    #     conn.commit()
    #     conn.close()
    #
    #     # Perform the search with the provided inv
    #     response = self.app.get('/search_by_inv?inv=test_inv')
    #     self.assertEqual(response.status_code, 200)
    #
    #     # Verify that the response contains the expected data
    #     expected_data = [
    #         {"uuid": 'test_uuid', "timestamp": '2022-01-01 12:00:00', "inv": 'test_inv', "desc": 'test_desc'}
    #     ]
    #     self.assertEqual(response.json, expected_data)
    #
    # def test_search_by_inv(self):
    #     # Assuming you have a record with inv '111' in your test database
    #     response = self.app.get('/search_by_inv?inv=111')
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.get_data(as_text=True))
    #     # Assert whatever response you expect
    #

    # class TestOCRFunctions(unittest.TestCase):
    #     def setUp(self):
    #         self.ocr_reader = ocr_init()
    #
    #     def test_ocr_jpg_image(self):
    #         # Assuming you have an image for testing in the 'tests' directory
    #         image_path = 'tests/your_test_image.jpg'
    #         text = ocr_jpg_image(self.ocr_reader, image_path)
    #         self.assertIsInstance(text, list)
    #         self.assertGreater(len(text), 0)
    #
    #     def test_combine_texts(self):
    #         # Assuming you have some sample data
    #         sample_data = [
    #             ([[0, 0], [100, 0], [100, 50], [0, 50]], 'Text 1', 0.9),
    #             ([[0, 50], [100, 50], [100, 100], [0, 100]], 'Text 2', 0.8)
    #         ]
    #         multiline_text = combine_texts(sample_data)
    #         self.assertIsInstance(multiline_text, str)
    #         self.assertIn('Text 1', multiline_text)
    #         self.assertIn('Text 2', multiline_text)
