from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import logging
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import replicate


app = Flask(__name__)
load_dotenv()
logging.basicConfig(level=logging.INFO)

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# # Configure Replicate
# replicate_api_token = os.getenv('REPLICATE_API_TOKEN')
# if not replicate_api_token:
#     raise ValueError("REPLICATE_API_TOKEN not found in environment variables")
# os.environ['REPLICATE_API_TOKEN'] = replicate_api_token


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

@app.route('/segment_video', methods=['POST'])
def segment_video():
    video_url = request.json.get('video_url')

    input = {
        "image": "https://replicate.delivery/pbxt/LMbGi83qiV3QXR9fqDIzTl0P23ZWU560z1nVDtgl0paCcyYs/cars.jpg"
    }

    output = replicate.run(
        "meta/sam-2:fe97b453a6455861e3bac769b441ca1f1086110da7466dbb65cf1eecfd60dc83",
        input=input
    )
    print(output)
    #=> {"combined_mask":"https://replicate.delivery/pbxt/PhfVJub...


@app.route('/edit_video/<path:video_url>')
def edit_video(video_url):
    if not video_url:
        return 'No video URL provided', 400
    return render_template('editor.html', video_url=video_url)

if __name__ == '__main__':
    app.run(debug=True)
