from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic

class SolutionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("SolutionWindow.ui", self)

if __name__ == "__main__":
    app = QApplication([])
    window = SolutionWindow()
    window.show()
    app.exec()
