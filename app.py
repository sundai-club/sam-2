from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import logging
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import replicate
import uuid


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
    guid = str(uuid.uuid4())
    logging.info(f"Generated GUID for video upload: {guid}")
    if 'video' not in request.files:
        raise ValueError('No file part')
    file = request.files['video']
    if file.filename == '':
        raise ValueError('No selected file')
    if file:
        try:
            # Create a working directory
            working_dir = f'/tmp/{guid}/'
            os.makedirs(working_dir, exist_ok=True)
            # Save the uploaded file
            file_path = os.path.join(working_dir, 'video.mp4')
            file.save(file_path)
            logging.info(f"File saved locally at: {file_path}")
            # Create a manifest file
            manifest_path = os.path.join(working_dir, f'{guid}.manifest')
            
            file.seek(0)
            upload_result = cloudinary.uploader.upload(file,
                                                       resource_type="video",
                                                       folder="uploaded_videos")
            logging.info(f"File uploaded to Cloudinary. URL: {upload_result['url']}")
            video_url = upload_result['url']
            with open(os.path.join(working_dir, 'video_url.txt'), 'w') as f:
                f.write(video_url)
            open(manifest_path, 'w').close()  # Create an empty file
            encoded_url = url_for('edit_video', video_id=guid,)
            
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


@app.route('/edit_video/<video_id>')
def edit_video(video_id):
    if not video_id:
        return 'No video URL provided', 400
    video_url_path = f'/tmp/{video_id}/video_url.txt'
    with open(video_url_path, 'r') as f:
        video_url = f.read()
    return render_template('editor.html', video_url=video_url)

if __name__ == '__main__':
    app.run(debug=True)
