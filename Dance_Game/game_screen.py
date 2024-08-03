import sys
import os
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtMultimedia
import pandas
import random
from pop_up_windows import *
from pause_menu import PauseMenu
import numpy as np
import requests
from dotenv import load_dotenv

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from Human_Tracker import human_tracker

os.chdir(os.path.dirname(__file__))

class GameScreen(QtWidgets.QWidget):
   def __init__(self):
      super(GameScreen, self).__init__()
      uic.loadUi("game_screen.ui", self)

      # Get pose data from csv file
      self.pose_data = pandas.read_csv("poses.csv")

      # Initialize game variables
      self.pose_time = 2000
      self.success_phrases = ["Perfect!", "Good!", "You Got It!", "Nice!", "Well Done!"]
      self.failure_phrases = ["Miss!", "Whoops!", "Incorrect", "Fail"]

      # Initialize human tracker
      self.tracker = human_tracker.HumanTracker()
      self.image_tracker = human_tracker.HumanTracker()

      # Initialize video capture
      self.video_capture = cv2.VideoCapture(0)

      # Initialize music player
      self.music_player = QtMultimedia.QMediaPlayer()
      self.music_position = 0

      # Initialize dialog boxes
      self.pause_menu = PauseMenu(self)
      self.pause_menu.resume_button.clicked.connect(self.resume)
      self.pause_menu.restart_button.clicked.connect(self.restart)
      self.pause_menu.rules_button.clicked.connect(self.open_rules)
      self.pause_menu.quit_button.clicked.connect(self.close_window)
      self.normal_rules_window = NormalRules(self)
      self.endless_rules_window = EndlessRules(self)
      self.death_screen_window = DeathScreen(self.close_window, self.restart, self)

      # Initialize Timers
      self.game_timer = QtCore.QTimer()
      self.game_timer.timeout.connect(self.game_timer_loop)
      self.pose_timer = QtCore.QTimer()
      self.pose_timer.timeout.connect(self.pose_timer_loop)
      self.pose_timer_remaining_time = 0

      # Setup buttons
      self.pause_button.clicked.connect(self.pause)

      self.target_images = []
      load_dotenv()
      self.client_id = os.getenv('UNSPLASH_ACCESS_KEY')

   def open_rules(self):
      if self.mode == "Normal":
         self.normal_rules_window.exec_()
      else:
         self.endless_rules_window.exec_()

   def start_normal_mode(self):
      # Start timers
      self.game_timer.start(30)
      self.pose_timer.start(self.pose_time)

      # Initialize variables
      self.lives = 3
      self.score = 0

      # Initialize the pose and the target image
      self.choose_new_pose()

      # Play music
      self.play_song("song1.mp3")

      self.display_score()
      
   def start_endless_mode(self):
      # Start timers
      self.game_timer.start(30)
      self.pose_timer.start(self.pose_time)

      # Initialize variables
      self.score = 0
      self.lives = 0

      # Initialize the pose and the target image
      self.choose_new_pose()

      # Play music
      self.play_song("song1.mp3")

      self.display_endless_score()

   def close_window(self):
      self.game_timer.stop()
      self.pose_timer.stop()
      self.stop_music()

   def open_window(self):
      self.open_rules()

      if self.mode == "Normal":
         self.start_normal_mode()
      else:
         self.start_endless_mode()

   def game_timer_loop(self):
       self.update_player_frame()
       self.update_time_bar()

   def update_player_frame(self):
      ret, frame = self.video_capture.read()
      if ret:
            # Find the human in the frame
            self.tracker.find_human(frame)
            # Draw the pose on the frame
            self.tracker.draw_pose(frame)

            # Flip frame
            frame = cv2.flip(frame, 1)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width
            q_img = QtGui.QImage(frame.data, width, height, step, QtGui.QImage.Format_RGB888)
            self.player_img.setPixmap(QtGui.QPixmap.fromImage(q_img))

   def set_target_frame(self, img_name):
      # Load the image
      self.image_path = os.path.join("Human_Poses", img_name)
      frame = cv2.imread(self.image_path)
      if frame is None:
         print("Error: Could not read image.")
         return

      # Extract pose from the image
      self.image_tracker.find_human(frame)

      # Create a black background
      height, width, channels = frame.shape
      black_background = np.zeros((height, width, channels), dtype=np.uint8)

      #Draw pose on it
      self.image_tracker.draw_pose(black_background)

      # Convert the black background with pose to QImage
      black_background = cv2.cvtColor(black_background, cv2.COLOR_BGR2RGB)
      height, width, channel = black_background.shape
      step = channel * width
      q_img = QtGui.QImage(black_background.data, width, height, step, QtGui.QImage.Format_RGB888)

      # Display the black background with pose on the target_img label
      
      self.target_img.setPixmap(QtGui.QPixmap.fromImage(q_img))
      self.target_img.update()

   def update_time_bar(self):
      self.time_bar.setProperty("value", self.pose_timer.remainingTime() / self.pose_time * 100)

   def display_score(self):
      self.score_label.setText(f"Score: {self.score}    Lives: {self.lives} ")
      
   def display_endless_score(self):
      self.score_label.setText(f"Score: {self.score}    Lives: \u221E ")

   def pose_timer_loop(self):
      if self.check_pose():
         self.move_status.setText(random.choice(self.success_phrases))
         self.move_status.setStyleSheet("QLabel {background-color: green;}")
         self.score += 1
      else:
         self.move_status.setText(random.choice(self.failure_phrases))
         self.move_status.setStyleSheet("QLabel {background-color: red;}")
         self.lives -= 1
      self.choose_new_pose()
      self.pose_timer.setInterval(self.pose_time)
      if self.mode == "Normal":
         self.display_score()
         if self.lives < 1:
            self.stop_game()
            self.death_screen_window.exec_()
      else:
         self.display_endless_score()
         

   def check_pose(self):  
      camera_info = self.extract_pose_from_camera()
      if self.image_tracker.processed_pose.pose_landmarks and self.tracker.processed_pose.pose_landmarks:
         return self.tracker.check_if_matches_pose(self.image_pose_info, camera_info)
      return False
   
   def has_all_body_parts(self, pose_landmarks, required_parts):
      # Check if the body is in an upright position
      if not (pose_landmarks["left_shoulder"][1] > pose_landmarks["nose"][1] and 
            pose_landmarks["right_shoulder"][1] > pose_landmarks["nose"][1]):
         return False
      
      if not (pose_landmarks["left_hip"][1] > pose_landmarks["left_shoulder"][1] and
            pose_landmarks["right_hip"][1] > pose_landmarks["right_shoulder"][1]):
         return False
      
      if not (pose_landmarks["left_knee"][1] > pose_landmarks["left_hip"][1] and
            pose_landmarks["right_knee"][1] > pose_landmarks["right_hip"][1]):
         return False

      # Check the pose has all of the given required parts (and they are visible)
      for part in required_parts:
         if part not in pose_landmarks or pose_landmarks[part][2] < 0.6:
            return False
         
      return True

   def choose_new_pose(self):
      # Original code
      # self.current_pose = random.randrange(self.pose_data.shape[0])
      # self.set_target_frame(self.pose_data["ImageName"][self.current_pose])
      # self.dance_name.setText(self.pose_data["Name"][self.current_pose])
      # Get the next image frame
      fixed_height = 500
      frame = self.get_next_image()

      if frame is not None:
         self.image_pose_info = self.extract_pose_from_image(frame)
         #Check image has landmarks, and has all of the required body parts
         if self.image_tracker.processed_pose.pose_landmarks:
            required_landmarks = [
               "nose", "left_eye", "right_eye",
               "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
               "left_wrist", "right_wrist", "left_hip", "right_hip",
               "left_knee", "right_knee"
            ]
            if self.has_all_body_parts(self.image_pose_info, required_landmarks):
            
               # Calculate the new width to maintain the aspect ratio
               height, width, channels = frame.shape
               aspect_ratio = width / height
               new_width = int(fixed_height * aspect_ratio)
               
               # Resize the frame to the new dimensions
               resized_frame = cv2.resize(frame, (new_width, fixed_height))
               
               # Draw the pose on the original picture
               self.image_tracker.draw_pose(resized_frame)
               
               # Convert the image with pose to QImage
               flipped_image = cv2.flip(resized_frame, 1)
               flipped_image = cv2.cvtColor(flipped_image, cv2.COLOR_BGR2RGB)
               height, width, channel = resized_frame.shape
               step = channel * width
               q_img = QtGui.QImage(flipped_image.data, width, height, step, QtGui.QImage.Format_RGB888)
               

               # Display the image with pose on the target_img label
               self.target_img.setPixmap(QtGui.QPixmap.fromImage(q_img))
               self.target_img.update()
               return
      # If no frame is returned or no pose was found, retry fetching the next image
      print("CHECKING")
      self.get_next_image()
      self.choose_new_pose()

   def get_new_images(self):
      search_url = "https://api.unsplash.com/photos/random"

      params = {
      'query': 'dancer+pose',   # Search term
      'client_id': self.client_id,  # Your access key
      'count': 50
      }

      response = requests.get(search_url, params=params)
      if response.status_code == 200:
         data = response.json()
         self.target_images = [image['urls']['small'] for image in data]

   def get_next_image(self):
      if len(self.target_images) > 0:
         image_response = requests.get(self.target_images.pop())
         if image_response.status_code == 200:
            image_array = np.asarray(bytearray(image_response.content), dtype="uint8")
      
            # Decode the image to an OpenCV format
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image
         return None
      else:
         self.get_new_images()
         return self.get_next_image()
   
   def set_new_pose_timer(self, new_time):
      self.pose_timer.start(new_time)

   def play_song(self, file_name):
      media_content = QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file_name))
      self.music_player.setMedia(media_content)
      self.music_player.play()

   def stop_music(self):
      self.music_position = self.music_player.position()
      self.music_player.stop()

   def resume_music(self):
      self.music_player.setPosition(self.music_position)
      self.music_player.play()

   def pause(self):
      self.stop_game()
      
      if not self.pause_menu.exec_():
         self.resume()
   
   def stop_game(self):
      self.stop_music()
      self.game_timer.stop()
      self.pose_timer_remaining_time = self.pose_timer.remainingTime()
      self.pose_timer.stop()
      

   def resume(self):
      self.resume_music()
      self.game_timer.start()
      self.pose_timer.start(self.pose_timer_remaining_time)

   def restart(self):
      if self.mode == "Normal":
         self.start_normal_mode()
      else:
         self.start_endless_mode()
         
   def extract_pose_from_image(self, frame):
      #Get the pose information from image frame
      if frame is None:
         print("Error: Could not read image.")
         return None

      # Find the human in the frame
      self.image_tracker.find_human(frame)

      # Extract pose information
      pose_info = self.image_tracker.get_pose_info()

      return pose_info

   def extract_pose_from_camera(self):
      if not self.video_capture.isOpened():
         print("Error: Video capture not opened.")
         return None

      ret, frame = self.video_capture.read()
      if not ret:
         print("Error: Could not read frame.")
         return None

      # Find the human in the frame
      self.tracker.find_human(frame)

      # Extract pose information
      pose_info = self.tracker.get_pose_info()

      return pose_info


if __name__ == '__main__':
   # app = QtWidgets.QApplication(sys.argv)
   # MainWindow = GameScreen()
   # MainWindow.show()
   # sys.exit(app.exec_())
   app = QtWidgets.QApplication(sys.argv)
   gs = GameScreen()
   print(gs.get_next_image())