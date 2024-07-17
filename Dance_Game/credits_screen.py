from PyQt5 import QtCore, QtGui, QtWidgets, uic

class CreditsScreen(QtWidgets.QWidget):
   def __init__(self):
      super(CreditsScreen, self).__init__()
      uic.loadUi("credits_screen.ui", self)