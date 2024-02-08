import requests
import cv2
from utils import *
addr= "http://192.168.0.106"
create_table()
def test_health_endpoint():
    # Replace 'http://your-flask-app-host:your-flask-app-port/' with the actual URL of your Flask app
    response = requests.get(addr+'/health')

    if response.status_code == 200 and response.text == "Server OK":
        print("Health Check Passed!")
    else:
        print("Health Check Failed.")
def test_inv_num_endpoint(image_path):
    # Load the image
    image = cv2.imread(image_path)
    _, img_encoded = cv2.imencode("imgs/rus_text_encoded.png", image)
    image_bytes = img_encoded.tobytes()

    # Send a POST request to the Flask endpoint
    response = requests.post(addr+'/inv_num', data=image_bytes)

    # Print the response
    print(response.text)
#ocr_reader = ocr_init()
#text=ocr_jpg_image(ocr_reader,  "imgs/rus_text.png")
#print(text[0][1])
#print(text)
test_inv_num_endpoint("imgs/rus_text.png")



# Run the test
test_health_endpoint()