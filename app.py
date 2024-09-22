from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import logging
import tempfile

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return 'No file part'
    file = request.files['video']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1])
        save_path = temp_file.name
        temp_file.close()
        file.save(save_path)
        logging.info(f"File saved to: {save_path}")
        return 'File successfully uploaded'


if __name__ == '__main__':
    app.run(debug=True)
