from gradio_client import Client, handle_file
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('GRADIO_API_KEY')

if not api_key:
    raise ValueError("GRADIO_API_KEY not found in environment variables")

# Create client with authentication
# client = Client("SkalskiP/florence-sam", hf_token=api_key)
client = Client("nathanfdunn/florence-sam-attempt2", hf_token=api_key)
# client = Client("nathanfdunn/florence-sam-attempt2")

result = client.predict(
		video_input={"video":handle_file('https://res.cloudinary.com/hkzbfes0n/video/upload/v1727031665/uploaded_videos/aojcuh3degxpxntslds4.mp4')},
		text_input="Bikes",
		api_name="/process_video"
)
print(result)