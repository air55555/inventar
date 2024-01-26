from flask import Flask, render_template, request
import subprocess, os
import numpy as np
from PIL import Image
import cv2

app = Flask(__name__)
#https://forums.developer.nvidia.com/t/help-needed-handling-images-in-python/107504

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/inv_num',methods =['POST'] )
def inv_num_save():
    if request.method=='POST':
        r=request
        nparr = np.fromstring(r.data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
               # save the image to disk
        cv2.imwrite("inv" + '.jpg', image)
        im = Image.fromarray(nparr)
        im.save("your_file.jpeg")
        # decode image
        #img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        #file = request.data
        #files['file']
        #img=file.read()
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'inv.jpg'))



@app.route('/upload.php')
def phpexample():
    command = "c:/php/php.exe /php"
    out = subprocess.run(command, stdout=subprocess.PIPE)
    return out.stdout

@app.route('/run_php_script')
def run_php_script():
    try:
        # Execute the PHP script using subprocess
        result = subprocess.check_output(['php', "php/upload.php"], stderr=subprocess.STDOUT, universal_newlines=True)
        return f"PHP Script Execution Result: {result}"
    except subprocess.CalledProcessError as e:
        return f"Error executing PHP script: {e.output}"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=80)