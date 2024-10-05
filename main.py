# main.py

import os
import subprocess
import logging
from extract_frames import extract_frames
from face_detection import detect_faces
from smooth_crops import smooth_crops
from generate_segments import generate_segments
from ffmpeg_processing import create_ffmpeg_commands, execute_commands
from concatenate_segments import concatenate_segments
from utils import cleanup_temp_files, get_video_metadata
from config import (
    VIDEO_PATH,
    FRAMES_DIR,
    OUTPUT_DIR,
    FINAL_OUTPUT,
    MIN_DURATION_SEC
)

def setup_logging():
    """
    Configures the logging settings.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("video_analysis.log"),
            logging.StreamHandler()
        ]
    )

def check_file_exists(file_path):
    """
    Checks if a file exists at the given path.

    Args:
        file_path (str): Path to the file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.isfile(file_path):
        logging.critical(f"Input video file not found: {file_path}")
        raise FileNotFoundError(f"Input video file not found: {file_path}")

def extract_audio(video_path, audio_output_path):
    """
    Extracts audio from the video using FFmpeg.

    Args:
        video_path (str): Path to the input video.
        audio_output_path (str): Path to save the extracted audio.
    """
    cmd = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-vn',
        '-acodec', 'aac',
        audio_output_path,
        '-loglevel', 'error'
    ]
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.info(f"Audio extracted to {audio_output_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error extracting audio: {e.stderr}")
        raise

def main():
    try:
        # Step 0: Setup Logging
        setup_logging()
        logging.info("Video analysis process started.")
        
        # Step 1: Check if input video exists
        check_file_exists(VIDEO_PATH)
        
        # Step 2: Extract audio
        audio_output_path = 'extracted_audio.aac'
        extract_audio(VIDEO_PATH, audio_output_path)
        
        # Step 3: Extract frames
        total_frames = extract_frames(VIDEO_PATH, FRAMES_DIR)
        
        # Step 4: Get video properties using ffprobe
        metadata = get_video_metadata(VIDEO_PATH)
        frame_rate = metadata['frame_rate']
        video_width = metadata['width']
        video_height = metadata['height']
        
        logging.info(f"Video Width: {video_width}, Video Height: {video_height}, Frame Rate: {frame_rate}")
        
        # Step 5: Detect faces and determine crop positions
        crop_positions = detect_faces(FRAMES_DIR, total_frames, frame_rate, video_width, video_height)
        
        # Step 6: Smooth crop positions
        smoothed_crops = smooth_crops(crop_positions, frame_rate, min_duration_sec=MIN_DURATION_SEC)
        
        # Step 7: Generate segments
        segments = generate_segments(smoothed_crops, frame_rate)
        
        # Step 8: Create FFmpeg commands
        commands = create_ffmpeg_commands(VIDEO_PATH, segments, OUTPUT_DIR, video_height=video_height)
        
        # Step 9: Execute FFmpeg commands
        execute_commands(commands)
        
        # Step 10: Concatenate segments and reapply audio
        final_video = concatenate_segments(OUTPUT_DIR, FINAL_OUTPUT, audio_output_path)
        
        # Optional: Cleanup temporary files
        cleanup_temp_files(FRAMES_DIR, OUTPUT_DIR, audio_output_path)
        
        logging.info(f"Processing complete. Final video saved as {final_video}")
    
    except FileNotFoundError as fnf_error:
        logging.critical(fnf_error)
        print("An error occurred during processing. Check the log file for details.")
    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}", exc_info=True)
        print("An error occurred during processing. Check the log file for details.")

if __name__ == "__main__":
    main()
