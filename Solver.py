import numpy as np
import copy
from Approach import Approach
from Direct_Methods import Gauss, GaussJordan, LU_Crout, LU_Doolittle, LU_Cholesky
from Iterative_Methods import Jacobi, GaussSeidel

from Direct_Methods.forwardeli import forwardElimination

class Solver:
   def __init__(self):
      self.matrix = np.array()
      self.b = np.array()
      self.answer = []
      self.approach = Approach()
      self.significant_digits = 0
      self.max_iterations = 50
      self.tolerance = 1e-5
      self.initial_guess = None
      self.solvability = None
      
   def setMatrix(self, matrix):
      self.matrix = copy.deepcopy(matrix)
   
   def setB(self, b):
      self.B = copy.deepcopy(b)
   
   def setSignificantDigits(self, significant_digits):
      self.significant_digits = significant_digits
    
   # For Iterative methods   
   def setMaxIterations(self, max_iterations):
      self.max_iterations = max_iterations
   
   def setTolerance(self, tolerance):
      self.significant_digits = tolerance
   
   def setInitialGuess(self, initial):
      self.initial_guess = copy.deepcopy(initial)
   
   
   def setAll(self, matrix, b, significant_digits):
      self.matrix = copy.deepcopy(matrix)
      self.b = copy.deepcopy(b)
      self.significant_digits = significant_digits
   
   def check_solvability(self):
      matrixChecker = copy.deepcopy(self.matrix)
      vectorChecker = copy.deepcopy(self.b)
      forwardElimination(matrixChecker, vectorChecker)
      rows = self.matrix.shape[0]
      zeroRows = []
      
      for i in rows:
         zeroRow = True
         for j in rows:
            if matrixChecker[i][j] != 0:
               zeroRow = False
               break
         if zeroRow:
            zeroRows.append(i)
      
      if len(zeroRows) == 0:
         self.solvability = "Unique"
         return
      else:
         for i in zeroRows:
            if vectorChecker[i] != 0:
               self.solvability = "None"
               return
      
      self.solvability = "Infinite"
   
   def setSolvingStrategy(self, approach) -> None:
      match approach:
         case "Gauss":
            self.approach = Gauss()
         case "Gauss Jordan":
            self.approach = GaussJordan()
         case "LU_Doolittle":
            self.approach = LU_Doolittle()
         case "Cholesky":
            self.approach = LU_Cholesky()
         case "LU_Crout":
            self.approach = LU_Crout()
         case "Jacobi":
            self.approach = Jacobi(self.matrix, self.b, self.significant_digits,
                                   self.max_iterations, self.tolerance, self.initial_guess)
         case "Gauss Seidel":
            self.approach = GaussSeidel(self.matrix, self.b, self.significant_digits,
                                        self.max_iterations, self.tolerance, self.initial_guess)
         case _:
            raise ValueError(f"Invalid solving strategy: {approach}")
   
   def solve(self):
      return self.approach.solve()
      
      
   # def printArray() -> str:
   #    pass

   m = np.array([ [5, -1, 1],
                  [2, 8, -1],
                  [-1, 1, 4]],
               dtype=np.float64)
   
   b = np.array([10, 11, 3], dtype=np.float64)
   print(check_solvability(m, b))