from PyQt5 import QtCore, QtGui, QtWidgets, uic

class HomeScreen(QtWidgets.QWidget):
   def __init__(self):
      super(HomeScreen, self).__init__()
      uic.loadUi("home_screen.ui", self)