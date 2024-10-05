# utils.py

import os
import shutil
import subprocess
import json
import logging


def cleanup_temp_files(*paths):
    """
    Deletes the specified files and directories.

    Args:
        *paths: Variable length argument list of paths to delete.
    """
    for path in paths:
        if os.path.isdir(path):
            try:
                shutil.rmtree(path)
                logging.info(f"Deleted directory: {path}")
            except Exception as e:
                logging.error(f"Failed to delete directory {path}: {e}")
        elif os.path.isfile(path):
            try:
                os.remove(path)
                logging.info(f"Deleted file: {path}")
            except Exception as e:
                logging.error(f"Failed to delete file {path}: {e}")
        else:
            logging.warning(f"Path not found for cleanup: {path}")


def get_video_metadata(video_path):
    """
    Retrieves video metadata using ffprobe.

    Args:
        video_path (str): Path to the video file.

    Returns:
        dict: Dictionary containing video metadata.
    """
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,avg_frame_rate',
        '-of', 'json',
        video_path
    ]

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        metadata = json.loads(result.stdout)
        stream = metadata['streams'][0]
        width = stream['width']
        height = stream['height']
        
        # Calculate frame rate
        avg_frame_rate = stream['avg_frame_rate']
        nums = avg_frame_rate.split('/')
        if len(nums) == 2 and nums[1] != '0':
            frame_rate = float(nums[0]) / float(nums[1])
        else:
            frame_rate = 30.0  # Default fallback
        
        logging.info(f"Retrieved video metadata: Width={width}, Height={height}, Frame Rate={frame_rate}")
        
        return {
            'width': width,
            'height': height,
            'frame_rate': frame_rate
        }
    except Exception as e:
        logging.error(f"Error retrieving video metadata: {e}")
        raise

def setup_logging(log_file='video_analysis.log'):
    """
    Configures the logging settings.

    Args:
        log_file (str): Path to the log file.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='w'),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging is configured.")
