
from PyQt6 import QtWidgets, uic
import sys

class Home(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the Home UI (it is a QMainWindow)
        uic.loadUi("Home.ui", self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Home()
    mainWindow.show()
    sys.exit(app.exec())
