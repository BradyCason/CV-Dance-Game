import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from Human_Tracker import human_tracker

import cv2

def open_window():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Find human pose
        results = humanTracker.find_human(frame)

        # Draw the pose on the frame
        humanTracker.draw_pose(frame, results)
        
        cv2.imshow('Pose Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    humanTracker = human_tracker.HumanTracker()
    open_window()