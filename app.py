from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import logging
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
logging.basicConfig(level=logging.INFO)

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        raise ValueError('No file part')
    file = request.files['video']
    if file.filename == '':
        raise ValueError('No selected file')
    if file:
        try:
            upload_result = cloudinary.uploader.upload(file,
                                                       resource_type="video",
                                                       folder="uploaded_videos")
            logging.info(f"File uploaded to Cloudinary. URL: {upload_result['url']}")
            video_url = upload_result['url']
            encoded_url = url_for('edit_video', video_url=video_url, _external=True)
            return redirect(encoded_url)
        except Exception as e:
            logging.exception(f"Error uploading to Cloudinary: {str(e)}")
            return 'Error uploading file'

@app.route('/edit_video/<path:video_url>')
def edit_video(video_url):
    if not video_url:
        return 'No video URL provided', 400
    return render_template('editor.html', video_url=video_url)

if __name__ == '__main__':
    app.run(debug=True)
