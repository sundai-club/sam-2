from gradio_client import Client, handle_file
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('GRADIO_API_KEY')

if not api_key:
    raise ValueError("GRADIO_API_KEY not found in environment variables")

# # Create client with authentication
# # client = Client("SkalskiP/florence-sam")
# # client = Client("nathanfdunn/florence-sam-attempt2")
# client = Client("nathanfdunn/florence-sam-attempt2", hf_token=api_key)
# # https://huggingface.co/spaces/nathanfdunn/florence-sam-attempt2

# result = client.predict(
# 		video_input={"video":handle_file('https://res.cloudinary.com/hkzbfes0n/video/upload/v1727031665/uploaded_videos/aojcuh3degxpxntslds4.mp4')},
# 		text_input="Bikes",
# 		api_name="/process_video"
# )
# print(result)

client = Client("nathanfdunn/florence-sam-attempt3")#, hf_token=api_key)
result = client.predict(
		mode_dropdown="open vocabulary detection + image masks",
		image_input=handle_file('https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),
		text_input="Hello!!",
		api_name="/process_image"
)
print(result)