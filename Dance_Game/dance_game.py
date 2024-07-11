import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from game_screen1 import Ui_MainWindow

import os
os.chdir(os.path.dirname(__file__))

class DanceGame:
   def __init__(self):
      # Setup Video Capture
      self.video_capture = cv2.VideoCapture(0)

      # Setup UI
      app = QtWidgets.QApplication(sys.argv)
      MainWindow = QtWidgets.QMainWindow()
      self.ui = Ui_MainWindow()
      self.ui.setupUi(MainWindow)

      # Setup timer for player video
      self.timer = QtCore.QTimer()
      self.timer.timeout.connect(self.update_player_frame)
      self.timer.start(30)

      # Initialize the target image
      self.set_target_frame("gottem.png")

      MainWindow.show()
      sys.exit(app.exec_())

   def update_player_frame(self):
      ret, frame = self.video_capture.read()
      if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width
            q_img = QtGui.QImage(frame.data, width, height, step, QtGui.QImage.Format_RGB888)
            self.ui.player_img.setPixmap(QtGui.QPixmap.fromImage(q_img))

   def set_target_frame(self, img_name):
       self.ui.target_img.setPixmap(QtGui.QPixmap("Target_Poses/" + img_name))

if __name__ == '__main__':
   dance_game = DanceGame()