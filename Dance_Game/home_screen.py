from PyQt5 import QtCore, QtGui, QtWidgets, uic

class HomeScreen(QtWidgets.QWidget):
   def __init__(self):
      super(HomeScreen, self).__init__()
      uic.loadUi("home_screen.ui", self)
      self.add_text_outline(self.title)

   def add_text_outline(self, label):
      effect1 = QtWidgets.QGraphicsDropShadowEffect(self)
      effect1.setOffset(0,0)
      effect1.setBlurRadius(10)
      effect1.setColor(QtGui.QColor("black"))

      label.setGraphicsEffect(effect1)
      label.setStyleSheet("color: white;")