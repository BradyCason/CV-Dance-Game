from PyQt5 import QtCore, QtGui, QtWidgets

class PauseMenu(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Pause Menu")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Game Pause!"))

        self.resume_button = QtWidgets.QPushButton("Resume")
        self.resume_button.clicked.connect(self.accept)
        layout.addWidget(self.resume_button)
        self.restart_button = QtWidgets.QPushButton("Restart")
        self.restart_button.clicked.connect(self.accept)
        layout.addWidget(self.restart_button)
        self.rules_button = QtWidgets.QPushButton("Rules")
        layout.addWidget(self.rules_button)
        self.quit_button = QtWidgets.QPushButton("Quit")
        self.quit_button.clicked.connect(self.accept)
        layout.addWidget(self.quit_button)

        self.setLayout(layout)