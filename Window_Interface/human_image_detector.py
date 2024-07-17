import sys
import os
import cv2
import numpy as np

# Assuming 'Human_Tracker' is in the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from Human_Tracker import human_tracker

def process_image(image_path):
    # Read the image
    frame = cv2.imread(image_path)
    if frame is None:
        print("Error: Could not read image.")
        return
    
    # Create a blank image with the same dimensions as the original frame
    blank_image = np.zeros_like(frame)
    
    # Find the human in the frame
    tracker.find_human(frame)
    
    # Get all of the information
    tracker.update_body_parts()
    # Use this information for angles
    tracker.calculate_angle(tracker.left_hip, tracker.left_ankle)

    # Draw the pose on the frame
    tracker.draw_pose(blank_image)
    
    
    # Display the image
    cv2.imshow('Pose Tracking', blank_image)
    
    # Wait until a key is pressed
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def extract_pose_from_image(tracker, image_path):
    frame = cv2.imread(image_path)
    if frame is None:
        print("Error: Could not read image.")
        return None

    # Find the human in the frame
    tracker.find_human(frame)

    # Extract pose information
    pose_info = tracker.get_pose_info()

    return pose_info

def extract_pose_from_camera(tracker):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        cap.release()
        return None

    # Find the human in the frame
    tracker.find_human(frame)

    # Extract pose information
    pose_info = tracker.get_pose_info()

    # Release the camera
    cap.release()
    return pose_info

if __name__ == "__main__":
    tracker = human_tracker.HumanTracker()
    image_path = 'Window_Interface\human_pose_pictures\pose1.png'

    # Extract pose from the image
    image_pose = extract_pose_from_image(tracker, image_path)

    # Extract pose from the camera
    camera_pose = extract_pose_from_camera(tracker)

    # Check if poses match
    matches = tracker.check_if_matches(image_pose, camera_pose)
    print("Poses match:", matches)
"""
if __name__ == "__main__":
    tracker = human_tracker.HumanTracker()
    image_path = "Window_Interface\human_pose_pictures\pose1.png"
    process_image(image_path)"""