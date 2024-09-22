import cv2
import os

# Function to extract frames
def extract_frames(video_path, output_folder):
    # Check if output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Open the video file
    video = cv2.VideoCapture(video_path)
    frame_count = 0

    while True:
        # Read frame-by-frame
        ret, frame = video.read()

        if not ret:  # If the frame is not successfully captured
            break

        # Save frame as an image file
        frame_filename = os.path.join(output_folder, f"{frame_count:05d}.jpg")
        cv2.imwrite(frame_filename, frame)
        
        frame_count += 1

    # Release the video object
    video.release()
    print(f"Extracted {frame_count} frames to {output_folder}")

# Path to your video file
video_path = 'bike-race-5-sec.mp4'

# Folder to save extracted frames
output_folder = 'frames'

# Extract frames
extract_frames(video_path, output_folder)
