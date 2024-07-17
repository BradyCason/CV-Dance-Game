import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from normal_mode import NormalMode
from home_screen import HomeScreen
from credits_screen import CreditsScreen

class Application_Controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Just Prance")

        # Set up Stacked Widget
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Set up Normal Mode Widget
        self.normal_screen = NormalMode()
        self.stacked_widget.addWidget(self.normal_screen)
        self.normal_screen.pause_button.clicked.connect(self.show_home_screen)

        # Set up Home Screen Widget
        self.home_screen = HomeScreen()
        self.stacked_widget.addWidget(self.home_screen)
        self.home_screen.normal_button.clicked.connect(self.show_normal_screen)
        self.home_screen.credits_button.clicked.connect(self.show_credits_screen)

        # Set up Credits Screen Widget
        self.credits_screen = CreditsScreen()
        self.stacked_widget.addWidget(self.credits_screen)
        self.credits_screen.back_button.clicked.connect(self.show_home_screen)

        self.show_home_screen()

    def show_normal_screen(self):
        self.stacked_widget.setCurrentWidget(self.normal_screen)
        self.normal_screen.open_window()

    def show_home_screen(self):
        self.stacked_widget.setCurrentWidget(self.home_screen)

    def show_credits_screen(self):
        self.stacked_widget.setCurrentWidget(self.credits_screen)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ac = Application_Controller()
    ac.show()
    sys.exit(app.exec_())