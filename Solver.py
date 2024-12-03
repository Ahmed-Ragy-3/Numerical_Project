import numpy as np
import copy
import pandas as pd
import Gauss, GaussJordan, LU_Crout, LU_Doolittle, LU_Cholesky
import Jacobi, GaussSeidel
import commonfunctions
import time
from forwardElimination import forward_elimination



class Solver:
   def __init__(self):
      self.matrix = None
      self.b = None
      self.answer = []
      self.approach = None
      self.significant_digits = 15
      self.max_iterations = 50
      self.tolerance = 1e-5
      self.initial_guess = None
      self.solvability = None
      self.str_approach = None
      
   def setMatrix(self, matrix):
      self.matrix = copy.deepcopy(matrix)
      if self.str_approach is not None:
         self.setSolvingStrategy(self.str_approach)
      return self

   def setB(self, b):
      self.b = copy.deepcopy(b)
      if self.str_approach is not None:
         self.setSolvingStrategy(self.str_approach)
      return self
      
   
   def setSignificantDigits(self, significant_digits):
      self.significant_digits = significant_digits
      if self.str_approach is not None:
         self.setSolvingStrategy(self.str_approach)
      return self
      
    
   # For Iterative methods
   def setMaxIterations(self, max_iterations):
      self.max_iterations = max_iterations
      self.setSolvingStrategy(self.str_approach)
      return self
      
   
   def setTolerance(self, tolerance):
      self.tolerance = tolerance
      if self.str_approach is not None:
         self.setSolvingStrategy(self.str_approach)
      return self
      
   
   def setInitialGuess(self, initial_guess):
      self.initial_guess = copy.deepcopy(initial_guess)
      if self.str_approach is not None:
         self.setSolvingStrategy(self.str_approach)
      return self
      
   
   
   def setAll(self, matrix, b, significant_digits):
      self.matrix = copy.deepcopy(matrix)
      self.b = copy.deepcopy(b)
      self.significant_digits = significant_digits
      if self.str_approach is not None:
         self.setSolvingStrategy(self.str_approach)
   
   def check_solvability(self):
      matrixChecker = copy.deepcopy(self.matrix)
      vectorChecker = copy.deepcopy(self.b)
      forward_elimination(matrixChecker, vectorChecker, self.significant_digits)
      commonfunctions.output = ""
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
            self.str_approach = "Gauss"
            self.approach = Gauss.Gauss(self.matrix, self.b, self.significant_digits)
         case "Gauss Jordan":
            self.str_approach = "Gauss Jordan"
            self.approach = GaussJordan.GaussJordan(self.matrix, self.b, self.significant_digits)
         case "Doolittle":
            self.str_approach = "Doolittle"
            self.approach = LU_Doolittle.Doolittle(self.matrix, self.b, self.significant_digits)
         case "Cholesky":
            self.str_approach = "Cholesky"
            self.approach = LU_Cholesky.Cholesky(self.matrix, self.b, self.significant_digits)
         case "Crout":
            self.str_approach = "Crout"
            self.approach = LU_Crout.Crout(self.matrix, self.b, self.significant_digits)
         case "Jacobi":
            self.str_approach = "Jacobi"
            self.approach = Jacobi.Jacobi(self.matrix, self.b, self.significant_digits,
                                   self.max_iterations, self.tolerance, self.initial_guess)
         case "Gauss Seidel":
            self.str_approach = "Gauss Seidel"
            self.approach = GaussSeidel.GaussSeidel(self.matrix, self.b, self.significant_digits,
                                    self.max_iterations, self.tolerance, self.initial_guess)
         case _:
            print("8ayro asm el method")
   
   def solve(self):
      self.check_solvability()
      if self.approach is None:
         commonfunctions.output = "Method is not selected yet"
         return commonfunctions.output
      commonfunctions.output += "The Matrix:\n"
      commonfunctions.output += commonfunctions.stringify_matrix(self.matrix, self.significant_digits)
      
      commonfunctions.output += "\n\nThe Vector:\n"
      for row in self.b.reshape(-1, 1):
         commonfunctions.output += " ".join(f" {value:.{self.significant_digits}f}" for value in row) + "\n"

      commonfunctions.output += "\n\nSolvability: "
      if self.solvability == "None":
         commonfunctions.output += "No Solution"
         return commonfunctions.output
      elif self.solvability == "Infinite":
         commonfunctions.output += "Infinite number of solutions"
         return commonfunctions.output
      
      commonfunctions.output += "Unique Solution\n\n"
      
      start_time = time.perf_counter()
      
      try:
         answer = self.approach.solve()
         commonfunctions.output = commonfunctions.output.replace("- -", "+ ")
      except Exception as e:
         print(e)
         return "Can't be solved using " + self.str_approach
      
      end_time = time.perf_counter()
      commonfunctions.output += f"\nThe Answer: (takes {(end_time - start_time) * 1000:.8f} ms)\n"
      # print(end_time - start_time)
      
      
      i = 0
      
      if self.str_approach == "Jacobi" or self.str_approach == "Gauss Seidel":
         commonfunctions.output += f"\nNumber of Iterations: {str(answer[1])}\n\n"
         for ans in answer[0]:
            commonfunctions.output += f"𝑥{commonfunctions.subscript(i + 1)} = "
            commonfunctions.output += str(commonfunctions.round_to_sig_figs(ans, self.significant_digits))
            i += 1
            commonfunctions.output += "\n"
      
         return commonfunctions.output
         
      elif self.str_approach == "Doolittle" or self.str_approach == "Cholesky" or self.str_approach == "Crout":
         L = answer[0]
         U = answer[1]
         commonfunctions.output += "\nThe Upper triangular Matrix:\n"
         for row in U:
            commonfunctions.output += " ".join(f"{value:.{self.significant_digits}f}" for value in row) + "\n"
         
         commonfunctions.output += "\n\nThe Lower triangular Matrix:\n"
         commonfunctions.output += commonfunctions.stringify_matrix(L, self.significant_digits)
         commonfunctions.output += "\n\n"
         
         for ans in answer[2]:
            commonfunctions.output += f"𝑥{commonfunctions.subscript(i + 1)} = "
            commonfunctions.output += str(commonfunctions.round_to_sig_figs(ans, self.significant_digits))
            i += 1
            commonfunctions.output += "\n"
            
         return commonfunctions.output

      
      for ans in answer:
         commonfunctions.output += f"𝑥{commonfunctions.subscript(i + 1)} = "
         commonfunctions.output += str(commonfunctions.round_to_sig_figs(answer[i], self.significant_digits))
         i += 1
         commonfunctions.output += "\n"
      
      return commonfunctions.output
   


def main():
   #test case
   A, b = get_test_case(2)
   
   solver = Solver()
   solver.setMatrix(A)
   solver.setB(b)
   solver.setSignificantDigits(2)
   
   solver.setSolvingStrategy("Jacobi")
   solver.check_solvability()

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

   elif test_case_number == 8:
      A = np.array([
         [5, 0, 0],
         [0, 3, 0],
         [0, 0, 2]
      ], dtype=float)
      b = np.array([15, 6, 7], dtype=float)
      
   else:
      raise ValueError("Invalid test case number. Please choose a number between 1 and 7.")
    
   return A, b
   
   
   
if __name__ == "__main__":
   main()
   
   
