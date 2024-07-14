import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from dance_game import DanceGame

class Application_Controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Just Prance")

        # Set up Stacked Widget
        self.stacked_widget = QtWidgets.QStackedWidget()

        self.dance_game = DanceGame()

        self.stacked_widget.addWidget(self.dance_game)

        self.setCentralWidget(self.stacked_widget)

    def show_game_screen(self):
        self.stacked_widget.setCurrentWidget(self.dance_game)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ac = Application_Controller()
    ac.show()
    sys.exit(app.exec_())