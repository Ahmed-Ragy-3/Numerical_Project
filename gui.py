import sys
from crypt import methods

from PyQt6 import QtWidgets, uic,QtCore
from PyQt6.QtGui import QIntValidator, QBrush, QColor
import numpy as np
from fontTools.varLib.models import nonNone
from pandas.core.methods.describe import select_describe_func

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
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("mixed.ui", self)  # Load the UI
        self.numberOfEquations.setValidator(QIntValidator(1,99))
        self.numberOfEquations.textChanged.connect(self.create_matrix)
        self.solve.clicked.connect(self.get_matrix)
        self.solve.setEnabled(False)  # Disable Solve button initially
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setFixedSize(0, 0)
        self.setMinimumHeight(600)
        self.setMinimumWidth(900)
        buttonsWidth = int(self.width() / 5)
        self.method = None # store the choosen method
        self.prevMethod = None

        self.significantFiguresNumber.setValidator(QIntValidator(1,20))
        self.significantFiguresNumber.setVisible(True)
        self.significantFiguresLabel.setVisible(True)
        self.toleranceNumber.setVisible(False)
        self.toleranceLabel.setVisible(False)
        self.iterationsNumber.setValidator(QIntValidator(1,999))
        self.iterationsNumber.setVisible(False)
        self.iterationsLabel.setVisible(False)

        self.mainLayout.setSpacing(2)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.methodButton.setCheckable(True)
        self.methodButton.setChecked(False)
        self.methodButton.setFixedWidth(buttonsWidth)

        self.methodDrawerLayout.setSpacing(2)
        self.methodDrawerLayout.setContentsMargins(0, 0, 0, 0)

        self.directButton.setCheckable(True)
        self.directButton.setMaximumWidth(buttonsWidth)

        self.directOptionsLayout.setSpacing(2)
        self.directOptionsLayout.setContentsMargins(0, 0, 0, 0)

        self.gaussButton.setMaximumWidth(buttonsWidth)

        self.gaussJordanButton.setMaximumWidth(buttonsWidth)

        self.DoolittleDecomposition.setMaximumWidth(buttonsWidth)

        self.CroutDecomposition.setMaximumWidth(buttonsWidth)

        self.CholeskyDecomposition.setMaximumWidth(buttonsWidth)

        self.directOptions.setVisible(False)

        # Iterative Section
        self.iterativeButton.setCheckable(True)
        self.iterativeButton.setMaximumWidth(buttonsWidth)
        
        #self.iterativeOptionsLayout.setSpacing(2)
        self.iterativeOptionsLayout.setContentsMargins(0, 0, 0, 0)

        self.jacobiButton.setMaximumWidth(buttonsWidth)

        self.sedielButton.setMaximumWidth(buttonsWidth)

        self.widget.setMinimumWidth(buttonsWidth)
        self.methodDrawer.setMinimumWidth(buttonsWidth)
        self.iterativeOptions.setVisible(False)

        self.methodDrawer.setVisible(False)

        self.methodButton.toggled.connect(self.toggleMethodDrawer)
        self.directButton.toggled.connect(self.toggleDirectOptions)
        self.iterativeButton.toggled.connect(self.toggleIterativeOptions)
        self.gaussButton.clicked.connect(self.toggleGaussButton)
        self.gaussJordanButton.clicked.connect(self.toggleGaussJordanButton)
        self.DoolittleDecomposition.clicked.connect(self.toggleDoolittleDecompositionButton)
        self.CroutDecomposition.clicked.connect(self.toggleCroutDecompositionButton)
        self.CholeskyDecomposition.clicked.connect(self.toggleCholeskyDecompositionButton)
        self.jacobiButton.clicked.connect(self.toggleJacobiButton)
        self.sedielButton.clicked.connect(self.toggleSedielButton)

    def create_matrix(self):

        rows = self.numberOfEquations.text()
        if not rows.isdigit() or int(rows) == 0:
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
        self.methodDrawer.setMaximumWidth(buttonsWidth)
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
            tolrence = float(itertations)
        except:
            tolrence = None
        if sigFigs.isdigit():
            solver.setSignificantDigits(int(sigFigs))
        if isFloat(tolrence):
            solver.setTolerance(int(tolrence))
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



    def toggleMethodDrawer(self, checked):
        self.methodDrawer.setVisible(checked)
        self.methodButton.setText("Method")
        self.method = None
        self.toleranceNumber.setVisible(False)
        self.toleranceLabel.setVisible(False)
        self.iterationsNumber.setVisible(False)
        self.iterationsLabel.setVisible(False)
        self.setSolve()


    def toggleDirectOptions(self, checked):
        self.directOptions.setVisible(checked)
        self.setSolve()



    def toggleIterativeOptions(self, checked):
        self.iterativeOptions.setVisible(checked)
        self.setSolve()


    def toggleGaussButton(self):
        self.methodButton.setText("Gauss")
        self.methodDrawer.setVisible(False)
        self.directOptions.setVisible(False)
        self.iterativeOptions.setVisible(False)
        self.solve.setEnabled(True)
        if (self.prevMethod == "Jacobi" or self.prevMethod == "Gauss Seidel" or self.prevMethod == None):
            self.prevMethod =  self.method = "Gauss"
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            self.create_matrix()





    def toggleGaussJordanButton(self):
        self.methodButton.setText("Gauss Jordan")
        self.methodDrawer.setVisible(False)
        self.directOptions.setVisible(False)
        self.iterativeOptions.setVisible(False)
        self.solve.setEnabled(True)
        if (self.prevMethod == "Jacobi" or self.prevMethod == "Gauss Seidel" or self.prevMethod == None):
            self.prevMethod = self.method = "Gauss Jordan"
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            self.create_matrix()






    def toggleDoolittleDecompositionButton(self):
        self.methodButton.setText("Doolittle Decomposition")
        self.methodDrawer.setVisible(False)
        self.directOptions.setVisible(False)
        self.iterativeOptions.setVisible(False)
        self.solve.setEnabled(True)
        if (self.prevMethod == "Jacobi" or self.prevMethod == "Gauss Seidel" or self.prevMethod == None):
            self.prevMethod = self.method = "Doolittle"
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            self.create_matrix()




    def toggleCroutDecompositionButton(self):
        self.methodButton.setText("Crout Decomposition")
        self.methodDrawer.setVisible(False)
        self.directOptions.setVisible(False)
        self.iterativeOptions.setVisible(False)
        self.solve.setEnabled(True)
        if (self.prevMethod == "Jacobi" or self.prevMethod == "Gauss Seidel" or self.prevMethod == None):
            self.prevMethod = self.method = "Crout"
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            self.create_matrix()




    def toggleCholeskyDecompositionButton(self):
        self.methodButton.setText("Cholesky Decomposition")
        self.methodDrawer.setVisible(False)
        self.directOptions.setVisible(False)
        self.iterativeOptions.setVisible(False)
        self.solve.setEnabled(True)
        if (self.prevMethod == "Jacobi" or self.prevMethod == "Gauss Seidel" or self.prevMethod == None):
            self.prevMethod = self.method = "Cholesky"
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            self.create_matrix()




    def toggleJacobiButton(self):
        self.methodButton.setText("Jacobi")
        self.methodDrawer.setVisible(False)
        self.directOptions.setVisible(False)
        self.iterativeOptions.setVisible(False)
        self.solve.setEnabled(True)
        if (self.prevMethod != "Gauss Seidel" or self.prevMethod == None):
            self.prevMethod = self.method = "Jacobi"
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            self.create_matrix()

        self.toleranceNumber.setVisible(True)
        self.toleranceLabel.setVisible(True)
        self.iterationsNumber.setVisible(True)
        self.iterationsLabel.setVisible(True)




    def toggleSedielButton(self):
        self.methodButton.setText("Gauss-Sediel")
        self.methodDrawer.setVisible(False)
        self.directOptions.setVisible(False)
        self.iterativeOptions.setVisible(False)
        self.solve.setEnabled(True)
        if (self.method != "Jacobi" or self.tableWidget.rowCount() == 0):
            self.prevMethod = self.method = "Gauss Seidel"
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            self.create_matrix()

        self.toleranceNumber.setVisible(True)
        self.toleranceLabel.setVisible(True)
        self.iterationsNumber.setVisible(True)
        self.iterationsLabel.setVisible(True)
        self.significantFiguresNumber.setVisible(True)
        self.significantFiguresLabel.setVisible(True)



    def openSolutionWindow(self, solutionString):
        self.solutionWindow = QtWidgets.QMainWindow()
        uic.loadUi("SolutionWindow.ui", self.solutionWindow)
        self.solutionWindow.solutionString.setText(solutionString)
        self.solutionWindow.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
