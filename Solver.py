import numpy as np
import copy
import Gauss, GaussJordan, LU_Crout, LU_Doolittle, LU_Cholesky
import Jacobi, GaussSeidel
import commonfunctions
from forwardElimination import forward_elimination

class Solver:
   def __init__(self):
      self.matrix = None
      self.b = None
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
      self.b = copy.deepcopy(b)
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
      
      for i in range(rows):
         zeroRow = True
         for j in range(rows):
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
            self.approach = Gauss.Gauss(self.matrix, self.b, self.significant_digits)
         case "Gauss Jordan":
            self.approach = GaussJordan.GaussJordan(self.matrix, self.b, self.significant_digits)
         case "Doolittle":
            self.approach = LU_Doolittle.Doolittle(self.matrix, self.b, self.significant_digits)
         case "Cholesky":
            self.approach = LU_Cholesky.Cholesky(self.matrix, self.b, self.significant_digits)
         case "Crout":
            self.approach = LU_Crout.Crout(self.matrix, self.b, self.significant_digits)
         case "Jacobi":
            self.approach = Jacobi.Jacobi(self.matrix, self.b, self.significant_digits,
                                   self.max_iterations, self.tolerance, self.initial_guess)
         case "Gauss Seidel":
            self.approach = GaussSeidel.GaussSeidel(self.matrix, self.b, self.significant_digits,
                                    self.max_iterations, self.tolerance, self.initial_guess)
         case _:
            raise ValueError(f"Invalid solving strategy: {approach}")
   
   def solve(self):
      output = "Unique Solution\n"
      if self.approach is None:
         output = "Method is not selected yet"
         return output
      
      self.check_solvability()
      
      if self.solvability == "None":
         output = "No Solution"
         return output
      elif self.solvability == "Infinite":
         output = "Infinite number of solutions"
         return output
      
      answer = self.approach.solve()
      i = 0
      for ans in answer:
         output += f"x{commonfunctions.subscript(i + 1)} = "
         output += str(answer[i])
         i += 1
         output += "\n"
      
      return output
   


def main():
   #test case
   A, b = get_test_case(3)
   
   solver = Solver()
   solver.setMatrix(A)
   solver.setB(b)
   solver.setSignificantDigits(20)
   solver.setSolvingStrategy("Gauss")
   solver.check_solvability()

   # print(solver.solvability)
   print(solver.solve())
   


def get_test_case(test_case_number):
   # 1- With Gauss Elimination and Gauss Jordan → Report the time taken by both methods.
   # 2- With LU decomposition Forms (Doolittle - Crout  - Cholesky ) → Report the time taken by them.
   # Note : Use precision = 4
   if test_case_number == 1:
      A = np.array([
         [2, 1, 1, 1, 1],
         [1, 2, 1, 1, 1],
         [1, 1, 2, 1, 1],
         [1, 1, 1, 2, 1],
         [1, 1, 1, 1, 2]
      ], dtype=float)
      b = np.array([4, 5, 6, 7, 8], dtype=float)

      # Solve the equations with Jacobi and Gauss Seidel → Report the convergence of both
      # and compare the time of convergence and number of iterations (if exist)
      # Default precision - max number of iteration = 100 - Absolute Relative Error = 0.00001
   elif test_case_number == 2:
      A = np.array([
         [8, 3, 2],
         [1, 5, 1],
         [2, 1, 6]
      ], dtype=float)
      b = np.array([13, 7, 9], dtype=float)

      # With Gauss Seidel - max number of iteration = 100 - default precision - relative error = 0.0005
   elif test_case_number == 3:
      A = np.array([
         [2, 3, -1, 4, -1, 5, 6],
         [1, 2, 3, -1, 4, 1, -5],
         [3, 1, -2, 3, -4, 2, -1],
         [4, 3, 1, 2, -3, 4, 5],
         [1, -2, 3, 1, 2, -3, 4],
         [2, -1, 4, 2, -1, 3, -2],
         [3, 2, 2, -3, 4, -5, 6]
      ], dtype=float)
      b = np.array([10, 5, 3, 8, -2, 6, -1], dtype=float)

      # With Gauss elimination  - default precision
   elif test_case_number == 4:
      A = np.array([
         [2, 3, -1, 4, -1],
         [1, 2, 3, -1, 4],
         [3, 1, -2, 3, -4],
         [4, 3, 1, 2, 0],
         [1, -2, 3, 1, 2]
      ], dtype=float)
      b = np.array([10, 5, 3, 8, -2], dtype=float)

      # 1- Using Gauss Elimination, Precision = 6
      # 2- Using Gauss Elimination, Precision = 3
   elif test_case_number == 5:
      A = np.array([
         [3, -0.1, -0.2],
         [0.1, 7, -0.3],
         [0.3, -0.2, 10]
      ], dtype=float)
      b = np.array([7.85, -19.3, 71.4], dtype=float)

      # Using Gauss Jordan & Doolittle Decomposition - default precision
   elif test_case_number == 6:
      A = np.array([
         [0, 2, 5],
         [2, 1, 1],
         [3, 1, 0]
      ], dtype=float)
      b = np.array([1, 1, 2], dtype=float)

      # With Jacobi and Gauss Seidel —> Report the convergence of both and 
      # compare the time of convergence and number of iterations (if exist)
      # Default precision - max number of iteration = 50 - Absolute Relative Error = 0.00001
   elif test_case_number == 7:
      A = np.array([
         [2, 1, 6],
         [8, 3, 2],
         [1, 5, 1]
      ], dtype=float)
      b = np.array([9, 13, 7], dtype=float)
   else:
      raise ValueError("Invalid test case number. Please choose a number between 1 and 7.")
    
   return A, b
   
   
   
if __name__ == "__main__":
   main()
   
   
