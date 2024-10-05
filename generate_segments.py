# generate_segments.py

import json
import logging

def generate_segments(smoothed_crops, frame_rate):
    """
    Generates video segments based on smoothed crop positions.

    Args:
        smoothed_crops (list): Smoothed list of crop_x positions.
        frame_rate (float): Frame rate of the video.

    Returns:
        list: List of segment dictionaries containing start_time, end_time, and crop_x.
    """
    segments = []
    start_frame = 0
    current_crop = smoothed_crops[0]

    for i, crop in enumerate(smoothed_crops):
        if crop != current_crop:
            end_frame = i
            segments.append({
                'start_time': start_frame / frame_rate,
                'end_time': end_frame / frame_rate,
                'crop_x': current_crop
            })
            logging.debug(f"Segment added: Start={start_frame/frame_rate}s, End={end_frame/frame_rate}s, Crop_x={current_crop}")
            start_frame = i
            current_crop = crop

    # Append the last segment
    segments.append({
        'start_time': start_frame / frame_rate,
        'end_time': len(smoothed_crops) / frame_rate,
        'crop_x': current_crop
    })
    logging.debug(f"Final segment added: Start={start_frame/frame_rate}s, End={len(smoothed_crops)/frame_rate}s, Crop_x={current_crop}")

    # Save to JSON
    with open('crop_segments.json', 'w') as f:
        json.dump(segments, f, indent=4)
    logging.info(f"Generated {len(segments)} segments and saved to crop_segments.json.")
    return segments
