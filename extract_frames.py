# extract_frames.py

import cv2
import os
import logging

def extract_frames(video_path, frames_dir):
    """
    Extracts frames from the input video and saves them as JPEG images.

    Args:
        video_path (str): Path to the input video file.
        frames_dir (str): Directory to save the extracted frames.

    Returns:
        int: Total number of frames extracted.
    """
    os.makedirs(frames_dir, exist_ok=True)
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    while success:
        frame_filename = os.path.join(frames_dir, f"frame_{count:06d}.jpg")
        cv2.imwrite(frame_filename, image)
        success, image = vidcap.read()
        count += 1
        if count % 100 == 0:
            logging.info(f"Extracted {count} frames.")
    vidcap.release()
    logging.info(f"Finished extracting frames. Total frames extracted: {count}")
    return count  # Total number of frames
