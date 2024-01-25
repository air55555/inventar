from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

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
    app.run(debug=True)