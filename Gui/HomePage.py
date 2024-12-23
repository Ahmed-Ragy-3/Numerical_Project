
from PyQt6 import QtWidgets, uic
import sys
from LinearSolver import LinearSolverPage
from RootFinder import RootFinderPage
from Home import Home


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the Home UI (it is a QMainWindow)
        uic.loadUi("HomePage.ui", self)


        # Set up the stacked widget
        self.stackedWidget = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
        self.setCentralWidget(self.stackedWidget)

        # Load pages
        self.linearSolverPage = LinearSolverPage()
        self.rootFinderPage = RootFinderPage()
        self.homePage =Home()

        # Add pages to the stacked widget
        self.stackedWidget.addWidget(self.linearSolverPage)
        self.stackedWidget.addWidget(self.rootFinderPage)
        self.stackedWidget.addWidget(self.homePage)
        self.stackedWidget.setCurrentWidget(self.homePage)


        # Access buttons from Home page
        self.homeButtonLinearSolver = self.findChild(QtWidgets.QPushButton, "linearsolver")
        self.homeButtonRootFinder = self.findChild(QtWidgets.QPushButton, "rootfinder")

        # Set up button click events
        self.homeButtonLinearSolver.clicked.connect(self.showLinearSolver)
        self.homeButtonRootFinder.clicked.connect(self.showRootFinder)

        # Add back buttons to linear solver and root finder pages
        self.linearSolverPage.findChild(QtWidgets.QPushButton, "backButton").clicked.connect(self.showHomePage)
        self.rootFinderPage.findChild(QtWidgets.QPushButton, "backButton").clicked.connect(self.showHomePage)

    def showLinearSolver(self):
        """Switch to Linear Solver page."""
        self.stackedWidget.setCurrentWidget(self.linearSolverPage)

    def showRootFinder(self):
        """Switch to Root Finder page."""
        self.stackedWidget.setCurrentWidget(self.rootFinderPage)

    def showHomePage(self):
        """Switch back to the Home page."""
        self.stackedWidget.setCurrentWidget(self.homePage)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainApp()
    mainWindow.show()
    sys.exit(app.exec())

