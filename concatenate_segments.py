# concatenate_segments.py

import os
import subprocess
import logging

def concatenate_segments(output_dir, final_output, audio_path):
    """
    Concatenates cropped video segments and reapplies the original audio.

    Args:
        output_dir (str): Directory containing cropped video segments.
        final_output (str): Path to save the final concatenated video.
        audio_path (str): Path to the extracted audio file.

    Returns:
        str: Path to the final video with audio.
    """
    list_file = os.path.join(output_dir, 'segments.txt')
    segment_files = sorted([
        f for f in os.listdir(output_dir)
        if f.startswith('segment_') and f.endswith('.mp4')
    ])

    logging.info("Creating segments.txt for FFmpeg concatenation.")

    with open(list_file, 'w') as f:
        for segment in segment_files:
            # Use absolute paths to ensure FFmpeg can locate the files
            segment_path = os.path.abspath(os.path.join(output_dir, segment))
            f.write(f"file '{segment_path}'\n")
            logging.debug(f"Added to segments.txt: {segment_path}")

    logging.info("Concatenating video segments.")

    # Concatenate video segments
    concat_cmd = [
        'ffmpeg',
        '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', list_file,
        '-c', 'copy',
        os.path.join(output_dir, 'concatenated_video.mp4'),
        '-loglevel', 'error'
    ]
    try:
        result = subprocess.run(concat_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.info("Video segments concatenated successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error concatenating video segments: {e.stderr}")
        raise

    # Reapply audio
    final_with_audio = final_output
    reapply_audio_cmd = [
        'ffmpeg',
        '-y',
        '-i', os.path.join(output_dir, 'concatenated_video.mp4'),
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-map', '0:v:0',
        '-map', '1:a:0',
        final_with_audio,
        '-loglevel', 'error'
    ]
    try:
        result = subprocess.run(reapply_audio_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.info(f"Final video with audio saved as {final_with_audio}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error reapplying audio: {e.stderr}")
        raise

    return final_with_audio
