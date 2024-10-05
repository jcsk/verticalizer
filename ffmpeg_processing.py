# ffmpeg_processing.py

import os
import subprocess
import logging

def create_ffmpeg_commands(video_path, segments, output_dir, video_height):
    """
    Creates FFmpeg commands for each video segment based on crop positions.

    Args:
        video_path (str): Path to the input video.
        segments (list): List of segment dictionaries containing start_time, end_time, and crop_x.
        output_dir (str): Directory to save cropped video segments.
        video_height (int): Height of the video in pixels.

    Returns:
        list: List of FFmpeg command lists.
    """
    os.makedirs(output_dir, exist_ok=True)
    commands = []
    target_width = int(video_height * 9 / 16)
    
    for idx, segment in enumerate(segments):
        start = segment['start_time']
        duration = segment['end_time'] - segment['start_time']
        crop_x = segment['crop_x']
        segment_filename = os.path.join(output_dir, f'segment_{idx:04d}.mp4')
        crop_filter = f"crop={target_width}:{video_height}:{crop_x}:0"
        cmd = [
            'ffmpeg',
            '-y',
            '-i', video_path,
            '-ss', f"{start}",
            '-t', f"{duration}",
            '-filter:v', crop_filter,
            '-c:a', 'copy',
            segment_filename,
            '-loglevel', 'error'
        ]
        commands.append(cmd)
        logging.debug(f"FFmpeg command created for segment {idx}: {cmd}")
    
    logging.info(f"Created FFmpeg commands for {len(segments)} segments.")
    return commands

def execute_commands(commands):
    """
    Executes a list of FFmpeg commands sequentially.

    Args:
        commands (list): List of FFmpeg command lists.
    """
    for idx, cmd in enumerate(commands):
        logging.info(f"Processing segment {idx+1}/{len(commands)}...")
        try:
            subprocess.run(cmd, check=True)
            logging.info(f"Segment {idx+1} processed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error processing segment {idx}: {e}")
            raise
    logging.info("All FFmpeg commands executed successfully.")
