import cv2
import mediapipe as mp

class HumanTracker:
    def __init__(self):
        #Initialize MediaPipe pose solution
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils

    def find_human(self, frame):
        #Convert the image from BGR to RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #Process the image and find the pose
        results = self.pose.process(image_rgb)
        return results

    def draw_pose(self, frame, results):
        #Draw the pose on the image
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )