import numpy as np
from commonfunctions import round_to_sig_figs

def forward_substitution(matrix, b, sig_figs, reduced=False):
   """
   Solves the system of linear equations Lx = b using forward substitution.
   
   Parameters:
      matrix (2D array): Lower triangular matrix L.
      b (1D array): Right-hand side vector b.
   
   Returns:
      x (1D array): Solution vector x.
   """
   # if reduced:
   #    return infinite_substitution(matrix, b)
   
   n = len(b)
   answer = np.zeros_like(b, dtype=np.float64)
   
   # Iterate over each row to solve for x[i]
   for i in range(n):
      if matrix[i, i] == 0:
         raise ValueError("In forward substitution: Matrix is singular or near-singular.")
      
      # Compute x[i]
      answer[i] = (b[i] - np.dot(matrix[i, :i], answer[:i])) / matrix[i, i]
      answer[i] = round_to_sig_figs(answer[i], sig_figs)
   
   return answer