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
        self.processed_pose = self.pose.process(image_rgb)

    def draw_pose(self, frame):
        #Draw the pose on the image
        if self.processed_pose.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame,
                self.processed_pose.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )

    def check_hands_up(self):
        if self.processed_pose.pose_landmarks:
            landmarks = self.processed_pose.pose_landmarks.landmark
            left_wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST]
            left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]

            if left_wrist.y < left_shoulder.y and right_wrist.y < right_shoulder.y:
                return True
        return False
    
    def check_left_leg_90(self):
        #Check if the left leg is about parallel with the person's hip
        if self.processed_pose.pose_landmarks:
            landmarks = self.processed_pose.pose_landmarks.landmark
            left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP]
            left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE]
            left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE]
            
            return abs(left_hip.y - left_ankle.y) < 0.1 and abs(left_knee.y - left_ankle.y) < 0.1
        return False
    
    def check_right_leg_90(self):
        #Check if the right leg is about parallel with the person's hip
        if self.processed_pose.pose_landmarks:
            landmarks = self.processed_pose.pose_landmarks.landmark
            right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP]
            right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE]
            right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE]
            
            return abs(right_hip.y - right_ankle.y) < 0.1 and abs(right_knee.y - right_ankle.y) < 0.1
        return False