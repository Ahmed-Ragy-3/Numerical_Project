import sys
# from crypt import methods

from PyQt6 import QtWidgets, uic,QtCore
from PyQt6.QtGui import QIntValidator, QBrush, QColor
from numpy.core.defchararray import upper
from soupsieve.util import lower

from Solver2 import Solver

from SolutionWindow import SolutionWindow

subscripts = {0: '₀', 1: '₁', 2: '₂', 3: '₃', 4: '₄', 5: '₅', 6: '₆', 7: '₇', 8: '₈', 9: '₉'}


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

class RootFinderPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("RootFinder.ui", self)  # Load the UI
        self.method = None
        self.solve.clicked.connect(self.handleSolve)
        self.plot.clicked.connect(self.handlePlot)
        self.solve.setEnabled(False)
        self.plot.setEnabled(False)
        self.setMinimumHeight(600)
        self.setMinimumWidth(900)
        self.Equation.textChanged.connect(self.setSolve)
        self.significantFiguresNumber.setValidator(QIntValidator(1,20))
        self.iterationsNumber.setValidator(QIntValidator(1,999))
        self.param1.setVisible(False)
        self.param2.setVisible(False)
        self.comboBox.currentTextChanged.connect(
            lambda text: self.handle_method_selection(text)
        )

    def handle_method_selection(self, text):
        if text == "Method":
            self.method = None
            self.param1.setVisible(False)
            self.param2.setVisible(False)
        elif text == "Bisection":
            self.method = "Bisection"
            self.param1.setVisible(True)
            self.param2.setVisible(True)
            self.param1.setPlaceholderText("Lower")
            self.param2.setPlaceholderText("Upper")
        elif text == "False-Position":
            self.method = "False-Position"
            self.param1.setVisible(True)
            self.param2.setVisible(True)
            self.param1.setPlaceholderText("Lower")
            self.param2.setPlaceholderText("Upper")
        elif text == "Fixed-Point":
            self.method = "Fixed-Point"
            self.param2.setVisible(True)
            self.param1.setVisible(False)
            self.param2.setPlaceholderText("Initial Guess")
        elif text == "Original Newton-Raphson":
            self.method = "Original Newton-Raphson"
            self.param2.setVisible(True)
            self.param1.setVisible(False)
            self.param2.setPlaceholderText("Initial Guess")
        elif text == "Modifed Newton-Raphson":
            self.method = "Modifed Newton-Raphson"
            self.param2.setVisible(True)
            self.param1.setVisible(False)
            self.param2.setPlaceholderText("Initial Guess")
        elif text == "Secant":
            self.method = "Secant"
            self.param1.setVisible(True)
            self.param2.setVisible(True)
            self.param1.setPlaceholderText("Lower")
            self.param2.setPlaceholderText("Upper")
        self.setSolve()
    def setSolve(self):
        if self.method != None and self.Equation.text() != "":
            self.solve.setEnabled(True)
            self.plot.setEnabled(True)
        else :
            self.solve.setEnabled(False)
            self.plot.setEnabled(False)



    def handlePlot(self):

        eqn = self.Equation.text()
        try:
            solver = Solver(eqn)
            solver.setApproach(self.method)
            solver.plot()
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Input Error"," Invalid Function")
            return
        print(eqn)

    def handleSolve(self):
        eqn = self.Equation.text()
        print(eqn)

        try:
            solver = Solver(eqn)
            solver.setApproach(self.method)
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Input Error"," : Invalid Function")
            return


    # if bi or false l->p1 , u->p2
        # else inital->p2
        sigFigs = self.significantFiguresNumber.text()
        tolrence = self.toleranceNumber.text()
        itertations = self.iterationsNumber.text()
        lower = self.param1.text()
        upper = self.param2.text()
        # print(sigFigs)
        # print(tolrence)
        # print(itertations)
        # print(lower)
        # print(upper)
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

        if (self.method == "secant" or self.method == "Bisection" or self.method == "False-Position"):

            if(not isFloat(lower) or not isFloat(upper)):
                QtWidgets.QMessageBox.warning(self, "Input Error ","should state initial guess")
                return
            solver.set_initial_guess_1(lower)
            solver.set_initial_guess_2(upper)
            try:
                self.openSolutionWindow(solver.solve())
            except ValueError as e:
                QtWidgets.QMessageBox.warning(self, "Input Error", " : Solve error")
                return
        else:
            if(not isFloat(upper)):
                QtWidgets.QMessageBox.warning(self, "Input Error","should state initial guess")
                return
            solver.set_initial_guess_1(upper)
            try:
                self.openSolutionWindow(solver.solve())
            except ValueError as e:
                QtWidgets.QMessageBox.warning(self, "Input Error", " : Solve error")
                return



    def openSolutionWindow(self, solutionString):
        self.solutionWindow = SolutionWindow()
        self.solutionWindow.solutionString.setText(solutionString)
        self.solutionWindow.findChild(QtWidgets.QPushButton, "backButton").clicked.connect(self.showRoot)
        mainWindow = self.parent()
        mainWindow.addWidget(self.solutionWindow)
        mainWindow.setCurrentWidget(self.solutionWindow)  # Switch to the solution page

    def showRoot(self):
        self.parent().setCurrentWidget(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RootFinderPage()
    window.show()
    sys.exit(app.exec())