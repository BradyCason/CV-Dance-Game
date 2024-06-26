import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from Human_Tracker import human_tracker

import cv2

def open_window():
    cap = cv2.VideoCapture(0)

if __name__ == "__main__":
    c = human_tracker.HumanTracker()
    c.find_human()