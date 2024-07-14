import sys
import os
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets, uic
#from game_screen2 import Ui_MainWindow
import pandas
import random

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from Human_Tracker import human_tracker

os.chdir(os.path.dirname(__file__))

class DanceGame(QtWidgets.QWidget):
   def __init__(self):
      super(DanceGame, self).__init__()
      self.setWindowTitle("Just Prance")
      uic.loadUi("game_screen2.ui", self)

      # Get pose data from csv file
      self.pose_data = pandas.read_csv("poses.csv")

      # Initialize game variables
      self.pose_time = 2000
      self.success_phrases = ["Perfect!", "Good!", "You Got It!", "Nice!", "Well Done!"]
      self.failure_phrases = ["Miss!", "Whoops!", "Incorrect", "Fail"]

      # Initialize human tracker
      self.tracker = human_tracker.HumanTracker()

      # Setup Video Capture
      self.video_capture = cv2.VideoCapture(0)

      # Setup timer for player video
      self.game_timer = QtCore.QTimer()
      self.game_timer.timeout.connect(self.game_timer_loop)
      self.game_timer.start(30)

      # Setup timer for pose
      self.pose_timer = QtCore.QTimer()
      self.pose_timer.timeout.connect(self.pose_timer_loop)
      self.pose_timer.start(self.pose_time)

      # Initialize the pose and the target image
      self.choose_new_pose()

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
       self.target_img.setPixmap(QtGui.QPixmap("Target_Poses/" + img_name))

   def update_time_bar(self):
       self.time_bar.setProperty("value", self.pose_timer.remainingTime() / self.pose_timer.interval() * 100)

   def pose_timer_loop(self):
      self.check_pose()
      self.choose_new_pose()

   def check_pose(self):
      print(self.pose_data)
      check_move_method = self.tracker.__getattribute__(self.pose_data["Method"][self.current_pose])
      
      if check_move_method():
         self.move_status.setText(random.choice(self.success_phrases))
         self.move_status.setStyleSheet("QLabel {background-color: green;}")
      else:
         self.move_status.setText(random.choice(self.failure_phrases))
         self.move_status.setStyleSheet("QLabel {background-color: red;}")

   def choose_new_pose(self):
      self.current_pose = random.randrange(self.pose_data.shape[0])
      self.set_target_frame(self.pose_data["ImageName"][self.current_pose])
   
   def set_new_pose_timer(self, new_time):
      self.pose_timer.start(new_time)

if __name__ == '__main__':
   app = QtWidgets.QApplication(sys.argv)
   MainWindow = DanceGame()
   MainWindow.show()
   sys.exit(app.exec_())