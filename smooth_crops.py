# smooth_crops.py

import logging

def smooth_crops(crop_positions, frame_rate, min_duration_sec=0.5):
    """
    Smooths crop positions to prevent jitter by enforcing a minimum duration for each crop.

    Args:
        crop_positions (list): List of crop_x positions for each frame.
        frame_rate (float): Frame rate of the video.
        min_duration_sec (float): Minimum duration (in seconds) for each crop.

    Returns:
        list: Smoothed list of crop_x positions.
    """
    min_frames = int(min_duration_sec * frame_rate)
    smoothed = []
    current_crop = crop_positions[0]
    count = 0

    for crop in crop_positions:
        if crop != current_crop:
            if count >= min_frames:
                current_crop = crop
                count = 1
                logging.debug(f"Changed crop to {current_crop} after {count} frames.")
            else:
                # Ignore the change and keep the current_crop
                count += 1
                logging.debug(f"Ignored crop change to {crop}. Keeping {current_crop}. Count: {count}")
        else:
            count += 1
        smoothed.append(current_crop)
    
    logging.info("Smoothing of crop positions completed.")
    return smoothed
