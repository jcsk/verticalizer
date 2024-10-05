# face_detection.py

import cv2
import os
import dlib

def detect_faces(frames_dir, total_frames, frame_rate, video_width, video_height):
    detector = dlib.get_frontal_face_detector()
    crop_positions = []
    
    for i in range(total_frames):
        frame_path = os.path.join(frames_dir, f"frame_{i:06d}.jpg")
        img = cv2.imread(frame_path)
        if img is None:
            print(f"Warning: Frame {i} could not be read.")
            crop_positions.append(video_width // 2)
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        if faces:
            # Find the largest face
            largest_face = max(faces, key=lambda rect: rect.width() * rect.height())
            center_x = largest_face.left() + largest_face.width() // 2
        else:
            # Fallback to centered crop
            center_x = video_width // 2

        # Calculate crop boundaries
        target_width = int(video_height * 9 / 16)
        half_width = target_width // 2
        crop_x = max(0, min(center_x - half_width, video_width - target_width))
        crop_positions.append(crop_x)
        
        if i % 100 == 0:
            print(f"Processed {i}/{total_frames} frames for face detection.")
    
    print("Face detection completed.")
    return crop_positions
