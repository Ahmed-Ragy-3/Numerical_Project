import numpy as np
import copy
from DirectMethods import Gauss, GaussJordan, LU_Crout, LU_Doolittle, LU_Cholesky
from IterativeMethods import Jacobi, GaussSeidel

from Helpers.forwardElimination import forward_elimination

class Solver:
   def __init__(self):
      self.matrix = np.array()
      self.b = np.array()
      self.answer = []
      self.approach = None
      self.significant_digits = 12
      self.max_iterations = 50
      self.tolerance = 1e-5
      self.initial_guess = None
      self.solvability = None
      
   def setMatrix(self, matrix):
      self.matrix = copy.deepcopy(matrix)
      return self
   
   def setB(self, b):
      self.B = copy.deepcopy(b)
      return self
      
   
   def setSignificantDigits(self, significant_digits):
      self.significant_digits = significant_digits
      return self
      
    
   # For Iterative methods
   def setMaxIterations(self, max_iterations):
      self.max_iterations = max_iterations
      return self
      
   
   def setTolerance(self, tolerance):
      self.tolerance = tolerance
      return self
      
   
   def setInitialGuess(self, initial_guess):
      self.initial_guess = copy.deepcopy(initial_guess)
      return self
      
   
   
   def setAll(self, matrix, b, significant_digits):
      self.matrix = copy.deepcopy(matrix)
      self.b = copy.deepcopy(b)
      self.significant_digits = significant_digits
   
   def check_solvability(self):
      matrixChecker = copy.deepcopy(self.matrix)
      vectorChecker = copy.deepcopy(self.b)
      forward_elimination(matrixChecker, vectorChecker)
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
   
   def setSolvingStrategy(self, approach : str) -> None:
      match approach:
         case "Gauss":
            self.approach = Gauss(self.matrix, self.b, self.significant_digits)
         case "Gauss Jordan":
            self.approach = GaussJordan(self.matrix, self.b, self.significant_digits)
         case "LU_Doolittle":
            self.approach = LU_Doolittle(self.matrix, self.b, self.significant_digits)
         case "Cholesky":
            self.approach = LU_Cholesky(self.matrix, self.b, self.significant_digits)
         case "LU_Crout":
            self.approach = LU_Crout(self.matrix, self.b, self.significant_digits)
         case "Jacobi":
            self.approach = Jacobi(self.matrix, self.b, self.significant_digits,
                                   self.max_iterations, self.tolerance, self.initial_guess)
         case "Gauss Seidel":
            self.approach = GaussSeidel(self.matrix, self.b, self.significant_digits,
                                    self.max_iterations, self.tolerance, self.initial_guess)
         case _:
            raise ValueError(f"Invalid solving strategy: {approach}")
   
   def solve(self):
      if self.approach is None:
         return "Method is not selected yet"
      self.check_solvability()
      if self.solvability == "None":
         return "No Solution"
      return self.approach.solve()
   
   

A = np.array([[2, -1, -2],
              [-4, 6, 3],
              [-4, -2, 8]], dtype=float)
b = np.array([-3, 9, 2], dtype=float)

def main():

   solver = Solver()
   solver.setSolvingStrategy("Gauss")
   solver.setMatrix(A).setB(b)
   solver.check_solvability()

   print(solver.solvability)
   solver.solve()
   
if __name__ == "__main__":
   main()