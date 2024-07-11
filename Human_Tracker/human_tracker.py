import cv2
import mediapipe as mp
import math

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
    
    def calculate_angle(self, point1, point2):
        #Calculates the absolute angle between two points, follow diagram that Dylan made if needed
        dx = point2.x - point1.x
        dy = point2.y - point1.y

        angle_radians = math.atan2(dy, dx)
        angle_degrees = math.degrees(angle_radians)

        # Ensure the angle is positive
        if angle_degrees < 0:
            angle_degrees += 360

        return angle_degrees
    
    def calculate_angle3(self, point1, point2, point3):
        #Caculates the angle between three points using dot product with two vectors
        #Make the vectors
        vector1 = (point1.x - point2.x, point1.y - point2.y)
        vector2 = (point3.x - point2.x, point3.y - point2.y)

        #Dot product and magnitude calculations
        dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
        magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
        magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

        #Angle in radians and then degrees
        angle_radians = math.acos(dot_product / (magnitude1 * magnitude2))
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees
        
    
    def check_left_leg_90(self):
        #Check if the left leg is about parallel with the person's hip
        if self.processed_pose.pose_landmarks:
            landmarks = self.processed_pose.pose_landmarks.landmark
            left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP]
            left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE]
            left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE]
            
            hip_to_knee_angle = self.calculate_angle(left_hip, left_knee)
            knee_to_ankle_angle = self.calculate_angle(left_knee, left_ankle)
            if (hip_to_knee_angle <= 45 or hip_to_knee_angle >= 315) and (knee_to_ankle_angle <= 45 or knee_to_ankle_angle >= 315):
                return True
        return False
    
    def check_right_leg_90(self):
        #Check if the right leg is about parallel with the person's hip
        if self.processed_pose.pose_landmarks:
            landmarks = self.processed_pose.pose_landmarks.landmark
            right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP]
            right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE]
            right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE]
            
            hip_to_knee_angle = self.calculate_angle(right_hip, right_ankle)
            knee_to_ankle_angle = self.calculate_angle(right_knee, right_ankle)
            if (135 <= hip_to_knee_angle <= 225) and (135 <= knee_to_ankle_angle <= 225):
                return True
        return False
    
    def check_if_dabbing(self):
        #Check if the person is dabbing
        if self.processed_pose.pose_landmarks:
            landmarks = self.processed_pose.pose_landmarks.landmark
            left_wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST]
            left_elbow = landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW]
            right_elbow = landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
            nose = landmarks[self.mp_pose.PoseLandmark.NOSE]

            #Checking the left dab first, 
            # which involves checking the left wrist being in the right position in relation to the nose and left elbow first
            left_wrist_above_nose = left_wrist.y < nose.y
            left_wrist_extended = left_wrist.x < left_elbow.x
            #Then checking if right wrist is farther away than the right elbow and the angle is correct
            right_arm_check = right_wrist.x < right_elbow.x and (180 <= self.calculate_angle(right_elbow, right_wrist) <= 240)
            
            #Then check the right dab
            right_wrist_above_nose = right_wrist.y < nose.y
            right_wrist_extended = right_wrist.x > right_elbow.x
            left_arm_check = left_wrist.x > left_elbow.x and (self.calculate_angle(left_elbow, left_wrist) >= 300)
            
            #Check both sides, if dabbing on right or left, it will return True
            return (left_wrist_above_nose and left_wrist_extended and right_arm_check) or (right_wrist_above_nose and right_wrist_extended and left_arm_check)
        return False