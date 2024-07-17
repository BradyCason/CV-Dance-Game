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