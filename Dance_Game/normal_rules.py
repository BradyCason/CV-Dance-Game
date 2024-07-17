from PyQt5 import QtCore, QtGui, QtWidgets

class NormalRules(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Normal Mode Rules")
        self.setGeometry(150, 150, 200, 100)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Rules:\nThese are the Rules bro."))
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        layout.addWidget(buttonBox)

        self.setLayout(layout)