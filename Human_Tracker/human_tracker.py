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
            
    def update_body_parts(self):
        #This grabs all of the body parts and updates there information
        landmarks = self.processed_pose.pose_landmarks.landmark
        self.nose = landmarks[self.mp_pose.PoseLandmark.NOSE]
        self.left_eye_inner = landmarks[self.mp_pose.PoseLandmark.LEFT_EYE_INNER]
        self.left_eye = landmarks[self.mp_pose.PoseLandmark.LEFT_EYE]
        self.left_eye_outer = landmarks[self.mp_pose.PoseLandmark.LEFT_EYE_OUTER]
        self.right_eye_inner = landmarks[self.mp_pose.PoseLandmark.RIGHT_EYE_INNER]
        self.right_eye = landmarks[self.mp_pose.PoseLandmark.RIGHT_EYE]
        self.right_eye_outer = landmarks[self.mp_pose.PoseLandmark.RIGHT_EYE_OUTER]
        self.left_ear = landmarks[self.mp_pose.PoseLandmark.LEFT_EAR]
        self.right_ear = landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR]
        self.mouth_left = landmarks[self.mp_pose.PoseLandmark.MOUTH_LEFT]
        self.mouth_right = landmarks[self.mp_pose.PoseLandmark.MOUTH_RIGHT]
        self.left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        self.right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        self.left_elbow = landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW]
        self.right_elbow = landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
        self.left_wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST]
        self.right_wrist = landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST]
        self.left_pinky = landmarks[self.mp_pose.PoseLandmark.LEFT_PINKY]
        self.right_pinky = landmarks[self.mp_pose.PoseLandmark.RIGHT_PINKY]
        self.left_index = landmarks[self.mp_pose.PoseLandmark.LEFT_INDEX]
        self.right_index = landmarks[self.mp_pose.PoseLandmark.RIGHT_INDEX]
        self.left_thumb = landmarks[self.mp_pose.PoseLandmark.LEFT_THUMB]
        self.right_thumb = landmarks[self.mp_pose.PoseLandmark.RIGHT_THUMB]
        self.left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP]
        self.right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP]
        self.left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE]
        self.right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE]
        self.left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE]
        self.right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE]
        self.left_heel = landmarks[self.mp_pose.PoseLandmark.LEFT_HEEL]
        self.right_heel = landmarks[self.mp_pose.PoseLandmark.RIGHT_HEEL]
        self.left_foot_index = landmarks[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
        self.right_foot_index = landmarks[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]
        
    def check_hands_up(self):
        if self.processed_pose.pose_landmarks:
            self.update_body_parts()
            if self.check_left_arm_up() and self.check_right_arm_up():
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
       
    def check_left_arm_up(self):
        #Check if the left arm is straight up
        if self.processed_pose.pose_landmarks:
            self.update_body_parts()
            angle = self.calculate_angle(self.left_shoulder, self.left_wrist)
            if (250 <= angle <= 290):
                return True
        return False
    
    def check_right_arm_up(self):
        #Check if the right arm is straight up
        if self.processed_pose.pose_landmarks:
            self.update_body_parts()
            angle = self.calculate_angle(self.right_shoulder, self.right_wrist)
            if (250 <= angle <= 290):
                return True
        return False
    
    def check_left_arm_90(self):
        #Checks if the left arm is straight out at 90 degrees
        if self.processed_pose.pose_landmarks:
            self.update_body_parts()
            angle = self.calculate_angle(self.left_shoulder, self.left_wrist)
            if (angle >= 315 or angle <= 45):
                return True
        return False
    
    def check_right_arm_90(self):
        #Checks if the right arm is straight out at 90 degrees
        if self.processed_pose.pose_landmarks:
            self.update_body_parts()
            angle = self.calculate_angle(self.right_shoulder, self.right_wrist)
            if (135 <= angle <= 225):
                return True
        return False
            
    def check_left_leg_90(self):
        #Check if the left leg is about parallel with the person's hip
        if self.processed_pose.pose_landmarks:
            self.update_body_parts()
            hip_to_knee_angle = self.calculate_angle(self.left_hip, self.left_knee)
            knee_to_ankle_angle = self.calculate_angle(self.left_knee, self.left_ankle)
            if (hip_to_knee_angle <= 45 or hip_to_knee_angle >= 315) and (knee_to_ankle_angle <= 45 or knee_to_ankle_angle >= 315):
                return True
        return False
   
    def check_right_leg_90(self):
        #Check if the right leg is about parallel with the person's hip
        if self.processed_pose.pose_landmarks:
            self.update_body_parts()
            hip_to_knee_angle = self.calculate_angle(self.right_hip, self.right_ankle)
            knee_to_ankle_angle = self.calculate_angle(self.right_knee, self.right_ankle)
            if (135 <= hip_to_knee_angle <= 225) and (135 <= knee_to_ankle_angle <= 225):
                return True
        return False
   
    def check_if_dabbing(self):
        #Check if the person is dabbing
        if self.processed_pose.pose_landmarks:
            self.update_body_parts()
            #Checking the left dab first,
            # which involves checking the left wrist being in the right position in relation to the nose and left elbow first
            left_wrist_above_nose = self.left_wrist.y < self.nose.y
            left_wrist_extended = self.left_wrist.x < self.left_elbow.x
            #Then checking if right wrist is farther away than the right elbow and the angle is correct
            right_arm_check = self.right_wrist.x < self.right_elbow.x and (180 <= self.calculate_angle(self.right_elbow, self.right_wrist) <= 240)
           
            #Then check the right dab
            right_wrist_above_nose = self.right_wrist.y < self.nose.y
            right_wrist_extended = self.right_wrist.x > self.right_elbow.x
            left_arm_check = self.left_wrist.x > self.left_elbow.x and (self.calculate_angle(self.left_elbow, self.left_wrist) >= 300)
           
            #Check both sides, if dabbing on right or left, it will return True
            return (left_wrist_above_nose and left_wrist_extended and right_arm_check) or (right_wrist_above_nose and right_wrist_extended and left_arm_check)
        return False
    
    def check_right_leg_opposite90(self):
        #Check if the right leg is about 90 degrees on opposite side of body
        if self.processed_pose.pose_landmarks:
            self.update_body_parts()
            hip_to_knee_angle = self.calculate_angle(self.right_hip, self.right_ankle)
            knee_to_ankle_angle = self.calculate_angle(self.right_knee, self.right_ankle)
            if (hip_to_knee_angle <= 70 or hip_to_knee_angle >= 315) and (knee_to_ankle_angle <= 70 or knee_to_ankle_angle >= 315):
                return True
        return False
    
    def check_left_leg_opposite90(self):
        #Check if the left leg is about parallel with the person's hip on opposite side
        if self.processed_pose.pose_landmarks:
            self.update_body_parts()
            hip_to_knee_angle = self.calculate_angle(self.left_hip, self.left_knee)
            knee_to_ankle_angle = self.calculate_angle(self.left_knee, self.left_ankle)
            if (120 <= hip_to_knee_angle <= 225) and (120 <= knee_to_ankle_angle <= 225):
                return True
        return False
    
    def check_arms_parallel_out(self):
        if self.processed_pose.pose_landmarks:
            self.update_body_parts()

            if self.check_left_arm_90() and self.check_right_arm_90():
                return True
        return False
    
    def check_right_leg_bent(self):
        #Check if the right leg is about 90 degrees on other leg
        if self.processed_pose.pose_landmarks:
            self.update_body_parts()
           
            right_leg_angle = self.calculate_angle3(self.right_hip, self.right_knee, self.right_ankle)
            left_leg_angle = self.calculate_angle(self.left_hip, self.left_ankle)
            
            if (65 <= right_leg_angle <= 115) and (80 <= left_leg_angle <= 100) and (abs(self.right_ankle.y - self.left_knee.y) <= 0.2):
                return True
        return False
    
    def check_left_leg_bent(self):
        #Check if the left leg is about 90 degrees on other leg
        if self.processed_pose.pose_landmarks:
            self.update_body_parts()
           
            left_leg_angle = self.calculate_angle3(self.left_hip, self.left_knee, self.left_ankle)
            right_leg_angle = self.calculate_angle(self.right_hip, self.right_ankle)
            
            if (65 <= left_leg_angle <= 115) and (80 <= right_leg_angle <= 100) and (abs(self.left_ankle.y - self.right_knee.y) <= 0.2):
                return True
        return False
    
    def check_arms_diagonal_right_up(self):
        #Checks if arms are about diagonal from each other with right on top
        if self.processed_pose.pose_landmarks:
            self.update_body_parts()
            
            right_arm_angle = self.calculate_angle(self.right_shoulder, self.right_wrist)
            left_arm_angle = self.calculate_angle(self.left_shoulder, self.left_wrist)

            if (20 <= left_arm_angle <= 70) and (200 <= right_arm_angle <= 250):
                return True
        return False
    
    def check_arms_diagonal_left_up(self):
        #Checks if arms are about diagonal from each other with left on top
        if self.processed_pose.pose_landmarks:
            self.update_body_parts()
            
            right_arm_angle = self.calculate_angle(self.right_shoulder, self.right_wrist)
            left_arm_angle = self.calculate_angle(self.left_shoulder, self.left_wrist)

            if (290 <= left_arm_angle <= 340) and (110 <= right_arm_angle <= 160):
                return True
        return False