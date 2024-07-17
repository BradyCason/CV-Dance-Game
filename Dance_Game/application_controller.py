import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from dance_game import DanceGame
from home_screen import HomeScreen

class Application_Controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Just Prance")

        # Set up Stacked Widget
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Set up Normal Mode Widget
        self.dance_game = DanceGame()
        self.stacked_widget.addWidget(self.dance_game)
        self.dance_game.pause_button.clicked.connect(self.show_home_screen)

        # Set up Home Screen Widget
        self.home_screen = HomeScreen()
        self.stacked_widget.addWidget(self.home_screen)
        self.home_screen.normal_button.clicked.connect(self.show_game_screen)

        self.show_home_screen()

    def show_game_screen(self):
        self.stacked_widget.setCurrentWidget(self.dance_game)

    def show_home_screen(self):
        self.stacked_widget.setCurrentWidget(self.home_screen)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ac = Application_Controller()
    ac.show()
    sys.exit(app.exec_())