import sys
# from crypt import methods

from PyQt6 import QtWidgets, uic,QtCore
from PyQt6.QtGui import QIntValidator, QBrush, QColor
import numpy as np


from SolutionWindow import SolutionWindow

from Solver import Solver

subscripts = {0: '₀', 1: '₁', 2: '₂', 3: '₃', 4: '₄', 5: '₅', 6: '₆', 7: '₇', 8: '₈', 9: '₉'}

baseSize = 45

def subscript(num):
    ret = ""

    if num == 0:
        return subscripts[0]  # Handle zero case

    while num != 0:
        ret += subscripts[num % 10]
        num //= 10
    return ''.join(reversed(ret))

def isFloat(value):
    try:
        float(value)  # Try converting to a float
        return True
    except :
        return False

class LinearSolverPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("LinearSolver.ui", self)  # Load the UI
        self.numberOfEquations.setValidator(QIntValidator(1,99))
        self.numberOfEquations.textChanged.connect(self.create_matrix)
        self.solve.clicked.connect(self.get_matrix)
        self.solve.setEnabled(False)  # Disable Solve button initially
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setFixedSize(0, 0)
        self.setMinimumHeight(600)
        self.setMinimumWidth(900)
        # buttonsWidth = int(self.width() / 5)
        self.method = None
        self.prevMethod = None

        self.significantFiguresNumber.setValidator(QIntValidator(1,20))
        self.significantFiguresNumber.setVisible(True)
        self.toleranceNumber.setVisible(False)
        self.iterationsNumber.setValidator(QIntValidator(1,999))
        self.iterationsNumber.setVisible(False)

        self.comboBox.currentTextChanged.connect(
            lambda text: self.handle_method_selection(text)
        )

    def handle_method_selection(self, text):
        if text == "Method":
            self.method = None
        elif text == "Gauss":
            self.method = "Gauss"
            if (self.prevMethod == "Jacobi" or self.prevMethod == "Gauss Seidel" or self.prevMethod == None):
                self.prevMethod =  self.method = "Gauss"
                self.create_matrix()
            self.prevMethod = self.method = "Gauss"
        elif text == "Gauss-Jordan":
            self.method = "Gauss Jordan"
            if (self.prevMethod == "Jacobi" or self.prevMethod == "Gauss Seidel" or self.prevMethod == None):
                self.prevMethod = self.method = "Gauss Jordan"
                self.create_matrix()
            self.prevMethod = self.method = "Gauss Jordan"
        elif text == "Crout LU":
            self.method = "Crout"
            if (self.prevMethod == "Jacobi" or self.prevMethod == "Gauss Seidel" or self.prevMethod == None):
                self.prevMethod = self.method = "Crout"
                self.create_matrix()
            self.prevMethod = self.method = "Crout"
        elif text == "Cholesky LU":
            self.method = "Cholesky"
            if (self.prevMethod == "Jacobi" or self.prevMethod == "Gauss Seidel" or self.prevMethod == None):
                self.prevMethod = self.method = "Cholesky"
                self.create_matrix()
            self.prevMethod = self.method = "Cholesky"
        elif text == "Doolittle LU":
            self.method = "Doolittle"
            if (self.prevMethod == "Jacobi" or self.prevMethod == "Gauss Seidel" or self.prevMethod == None):
                self.prevMethod = self.method = "Doolittle"
                self.create_matrix()
            self.prevMethod = self.method = "Doolittle"
        elif text == "Jacobi":
            self.method = "Jacobi"
            if (self.prevMethod != "Gauss Seidel" or self.prevMethod == None):
                self.prevMethod = self.method = "Jacobi"
                self.create_matrix()
            self.prevMethod = self.method = "Jacobi"
        elif text == "Gauss-Seidel":
            self.method = "Gauss Seidel"
            if (self.prevMethod != "Jacobi" or self.prevMethod == None):
                self.prevMethod = self.method = "Gauss Seidel"
                self.create_matrix()
            self.prevMethod = self.method = "Gauss Seidel"

        if (self.method == "Jacobi" or self.method == "Gauss Seidel"):
            self.toleranceNumber.setVisible(True)
            self.iterationsNumber.setVisible(True)
        else :
            self.toleranceNumber.setVisible(False)
            self.iterationsNumber.setVisible(False)


        self.setSolve()

    def create_matrix(self):
        rows = self.numberOfEquations.text()
        if not rows.isdigit() or int(rows) == 0 or self.method == None:
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setFixedSize(0, 0)
            self.solve.setEnabled(False)
            return
        rows = int(rows)
        cols = rows+1
        if(self.method == "Jacobi" or self.method == "Gauss Seidel"):
            rows+=1
        self.setSolve()
        # Set up table
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(cols)
        headers = [f"x{subscript(i+1)}" for i in range(cols-1)] + ["B"]
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(baseSize)  # Adjust cell size
        self.tableWidget.verticalHeader().setDefaultSectionSize(baseSize)
        # self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        total_width = (cols) * baseSize+2
        total_height = rows * baseSize+23 # add the size of col name bar
        maxWidth = int(self.width() - self.width() / 2)
        maxHeight = int(self.height() - self.height() / 2)
        buttonsWidth = int(self.width() / 5)
        self.widget.setMaximumWidth(buttonsWidth)
        # self.methodDrawer.setMaximumWidth(buttonsWidth)
        self.tableWidget.setFixedSize(min(total_width,maxWidth), min(total_height,maxHeight))

        # Fill table with default values
        for row in range(rows):
            for col in range(cols):
                item = QtWidgets.QTableWidgetItem("0")
                if (rows == cols and col == cols-1) or (rows!=cols and col == rows ):  # If it's the last column
                    item.setBackground(QBrush(QColor("light pink")))  # Set background color
                    if((self.method == "Jacobi" or self.method == "Gauss Seidel" )and row == rows-1):
                        item.setBackground(QBrush(QColor("grey")))

                self.tableWidget.setItem(row, col, item)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def setSolve(self):
        rows = self.numberOfEquations.text()
        if self.method != None and rows.isdigit() and int(rows)!=0 :
            self.solve.setEnabled(True)
        else :
            self.solve.setEnabled(False)

    def get_matrix(self):
        rows = int(self.numberOfEquations.text())
        matrix = np.zeros((rows, rows))
        b = np.zeros(rows)

        # Retrieve matrix values
        for row in range(rows):
            for col in range(rows):
                item = self.tableWidget.item(row, col)
                if not item or item.text().strip() == "":
                    QtWidgets.QMessageBox.warning(self, "Input Error", f"Cell ({row}, {col}) is empty.")
                    return
                try:
                    matrix[row, col] = float(item.text())
                except ValueError:
                    QtWidgets.QMessageBox.warning(self, "Input Error", f"Invalid number at cell ({row}, {col}).")
                    return

        # Retrieve b vector values
        for i in range(rows):
            item = self.tableWidget.item(i, rows)
            if not item or item.text().strip() == "":
                QtWidgets.QMessageBox.warning(self, "Input Error", f"Cell ({i}, {rows}) is empty.")
                return
            try:
                b[i] = float(item.text())
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Input Error", f"Invalid number at cell ({i}, {rows}).")
                return

        solver = Solver()
        solver.setMatrix(matrix)
        solver.setB(b)
        solver.setSolvingStrategy(self.method)
        sigFigs = self.significantFiguresNumber.text()
        tolrence = self.toleranceNumber.text()
        itertations = self.iterationsNumber.text()
        try:
            tolrence = float(tolrence)
        except:
            tolrence = None
        if sigFigs.isdigit():
            solver.setSignificantDigits(int(sigFigs))
        if isFloat(tolrence):
            solver.setTolerance(float(tolrence))
        if itertations.isdigit():
            solver.setMaxIterations(int(itertations))
        if (self.method == "Jacobi" or self.method == "Gauss Seidel"):
            initialGuess = np.zeros(rows)
            for i in range (rows) :
                item = self.tableWidget.item(rows,i)
                if not item or item.text().strip() == "":
                    QtWidgets.QMessageBox.warning(self, "Input Error", f"Cell ({row}, {col}) is empty.")
                    return
                try:
                    initialGuess[i] = float(item.text())
                except ValueError:
                    QtWidgets.QMessageBox.warning(self, "Input Error", f"Invalid number at cell ({row}, {col}).")
                    return

            solver.setInitialGuess(initialGuess)
        self.openSolutionWindow(solver.solve())

    def openSolutionWindow(self, solutionString):
        self.solutionWindow = SolutionWindow()
        self.solutionWindow.solutionString.setText(solutionString)
        self.solutionWindow.findChild(QtWidgets.QPushButton, "backButton").clicked.connect(self.showLinear)
        mainWindow = self.parent()  # Assuming the parent is MainApp
        mainWindow.addWidget(self.solutionWindow)
        mainWindow.setCurrentWidget(self.solutionWindow)  # Switch to the solution page

    def showLinear(self):
        self.parent().setCurrentWidget(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LinearSolverPage()
    window.show()
    sys.exit(app.exec())
