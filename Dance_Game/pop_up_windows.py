from PyQt5 import QtCore, QtGui, QtWidgets

class NormalRules(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Normal Mode Rules")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("How to Play:\n-A dance move will appear in "\
                                          "the target frame on the left.\n-Match the move "\
                                          "when the time bar reaches 0 to gain a point.\n-3 "\
                                          "Strikes and you're out!"))
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

class EndlessRules(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Endless Mode Rules")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("How to Play:\n-A dance move will appear in "\
                                          "the target frame on the left.\n-Match the move "\
                                          "when the time bar reaches 0 to gain a point.\n-Keep "\
                                          "prancing until you can't, or else..."))
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        layout.addWidget(buttonBox)

        self.setLayout(layout)
        
class DeathScreen(QtWidgets.QDialog):
    def __init__(self, quit, restart, parent=None):
        super().__init__(parent)

        self.setWindowTitle("YOU LOST!")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Well, well, well... That was quite the performance.\n"
            "It seems rhythm just isn't your forte, is it?\n"
            "But don't worry, not everyone can be a dance superstar!\n"
            "Maybe you should stick to tapping your foot under the table.\n"
            "Ready to try again, or should we just call it a day?"
            ))
        # Create a QDialogButtonBox with custom buttons
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.NoButton)
        self.quit_button = buttonBox.addButton("Quit", QtWidgets.QDialogButtonBox.RejectRole)
        self.restart_button = buttonBox.addButton("Restart", QtWidgets.QDialogButtonBox.AcceptRole)

        # Connect the buttons to their respective slots
        self.quit_button.clicked.connect(quit)
        self.restart_button.clicked.connect(restart)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout.addWidget(buttonBox)
        self.setLayout(layout)