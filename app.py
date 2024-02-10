from flask import Flask, render_template, request
import subprocess, os
import numpy as np
import cv2
from utils import ocr_jpg_image, ocr_init, combine_texts , \
    search_by_inv_num ,upload_file


app = Flask(__name__)


#https://forums.developer.nvidia.com/t/help-needed-handling-images-in-python/107504

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    return "Server OK", 200

@app.route('/inv_num',methods =['POST'] )
def inv_num_save():
    if request.method=='POST':
        r=request
        nparr = np.fromstring(r.data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
               # save the image to disk # Generate a unique ID for the file
        file_path = upload_file(image)

        text=ocr_jpg_image(ocr_reader, file_path ) #"imgs/rus_text.png"
        if len(text)>0:
            multiline = combine_texts(text)
            #print(text[0][1])
            #return text[0][1], 200
            return multiline, 200
        else:
            return "No text detected", 200
        # decode image
        #img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        #file = request.data
        #files['file']
        #img=file.read()
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'inv.jpg'))




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=80)
    ocr_reader = ocr_init()