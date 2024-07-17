import sys
import os
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtMultimedia
import pandas
import random
from normal_rules import NormalRules
from pause_menu import PauseMenu
import numpy as np

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

      # Initialize Timers
      self.game_timer = QtCore.QTimer()
      self.game_timer.timeout.connect(self.game_timer_loop)
      self.pose_timer = QtCore.QTimer()
      self.pose_timer.timeout.connect(self.pose_timer_loop)
      self.pose_timer_remaining_time = 0

      # Setup buttons
      self.pause_button.clicked.connect(self.pause)

   def open_rules(self):
      if self.mode == "Normal":
         self.normal_rules_window.exec_()

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

   def close_window(self):
      self.game_timer.stop()
      self.pose_timer.stop()
      self.stop_music()

   def open_window(self):
      self.open_rules()

      if self.mode == "Normal":
         self.start_normal_mode()

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
      self.tracker.find_human(frame)
      pose_info = self.tracker.get_pose_info()

      # Create a black background
      height, width, channels = frame.shape
      black_background = np.zeros((height, width, channels), dtype=np.uint8)

      #Draw pose on it
      self.tracker.draw_pose(black_background)

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
      self.display_score()

   def check_pose(self):
      check_move_method = self.tracker.__getattribute__(self.pose_data["Method"][self.current_pose])
      
      return check_move_method(self.extract_pose_from_image(self.image_path), self.extract_pose_from_camera())

   def choose_new_pose(self):
      self.current_pose = random.randrange(self.pose_data.shape[0])
      self.set_target_frame(self.pose_data["ImageName"][self.current_pose])
      self.dance_name.setText(self.pose_data["Name"][self.current_pose])
   
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
      self.stop_music()
      self.game_timer.stop()
      self.pose_timer_remaining_time = self.pose_timer.remainingTime()
      self.pose_timer.stop()
      
      if not self.pause_menu.exec_():
         self.resume()

   def resume(self):
      self.resume_music()
      self.game_timer.start()
      self.pose_timer.start(self.pose_timer_remaining_time)

   def restart(self):
      if self.mode == "Normal":
         self.start_normal_mode()
         
   def extract_pose_from_image(self, image_path):
      frame = cv2.imread(image_path)
      if frame is None:
         print("Error: Could not read image.")
         return None

      # Find the human in the frame
      self.tracker.find_human(frame)

      # Extract pose information
      pose_info = self.tracker.get_pose_info()

      return pose_info

   def extract_pose_from_camera(self):
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
      self.tracker.find_human(frame)

      # Extract pose information
      pose_info = self.tracker.get_pose_info()

      # Release the camera
      cap.release()
      return pose_info


if __name__ == '__main__':
   app = QtWidgets.QApplication(sys.argv)
   MainWindow = GameScreen()
   MainWindow.show()
   sys.exit(app.exec_())