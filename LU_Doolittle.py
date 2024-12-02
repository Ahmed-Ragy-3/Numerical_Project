import numpy as np
from forwardSubstitution import forward_substitution
from backwardSubstitution import backward_substitution
from forwardElimination import pivot
import commonfunctions

class Doolittle:
   def __init__(self, A, b, sig_figs=20):
      self.A = A
      self.b = b
      self.sig_figs = sig_figs
      self.L = None
      self.U = None
      self.result = np.zeros(self.A.shape[0], dtype=float)
      
   def setB(self, b):
      self.b = b

   def decompose(self):
      # print(self.A)
      
      rows = self.A.shape[0]
      self.L = np.eye(rows, dtype=float)  # Initialize L as identity matrix
      self.U = np.zeros((rows, rows), dtype=float)  # Initialize U as zero matrix
      
      order = np.arange(len(self.b))
      for r in range(rows):
         pivot(self.A, self.b, rows_order=order, row=r)
      
      
      for i in range(rows):
         
         for j in range(i, rows):
            # Calculate elements of U
            self.U[i][j] = self.A[i][j] - np.dot(self.L[i, :i], self.U[:i, j])
         
         for j in range(i + 1, rows):
            # Calculate elements of L
            if self.U[i][i] == 0:
               raise ValueError("Matrix is singular, unable to perform LU decomposition.")
            self.L[j][i] = (self.A[j][i] - np.dot(self.L[j, :i], self.U[:i, i])) / self.U[i][i]

   def solve(self):
      if self.L is None or self.U is None:
         self.decompose()

      y = forward_substitution(self.L, self.b, self.sig_figs)
      
      return self.L, self.U, backward_substitution(self.U, y, self.sig_figs)

   def getMatrixL(self):
      return self.L

   def getMatrixU(self):
      return self.U
