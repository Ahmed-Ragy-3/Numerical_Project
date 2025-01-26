import numpy as np
import commonfunctions

def backward_substitution(matrix, b, sig_figs):
   """
   Solves the system of linear equations Ax = b using backward substitution.
   
   Parameters:
      matrix (2D array): Upper triangular matrix A.
      b (1D array): Right-hand side vector b.
   
   Returns:
      x (1D array): Solution vector x.
   """
   n = len(b)
   answer = np.zeros_like(b, dtype=np.float64)
   
   # Start from the last row and move upwards
   for i in range(n - 1, -1, -1):
      if matrix[i, i] == 0:
         raise ValueError("In back substitution: Matrix is singular or near-singular.")
      
      # Calculate the value of x[i]
      answer[i] = (b[i] - np.dot(matrix[i, i + 1:], answer[i + 1:])) / matrix[i, i]
      answer[i] = commonfunctions.round_to_sig_figs(answer[i], sig_figs)
   
   return answer