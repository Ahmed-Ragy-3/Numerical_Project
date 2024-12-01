import numpy as np
from backwardSubstitution import backward_substitution
from forwardSubstitution import forward_substitution

class Crout:
   def __init__(self, A, b, sig_figs=20):
      self.b = b
      self.A = A
      self.n = self.A.shape[0]
      self.L = None
      self.U = None
      self.sig_figs = sig_figs
   
   def setB(self, b):
      self.b = b
      
   def decompose(self):
      # Crout's decomposition process
      self.L = np.zeros((self.n, self.n), dtype=float)
      self.U = np.eye(self.n, dtype=float)
      
      for j in range(self.n):
         for i in range(j, self.n):
            self.L[i, j] = self.A[i, j] - np.dot(self.L[i, :j], self.U[:j, j])
         
         for k in range(j + 1, self.n):
            self.U[j, k] = (self.A[j, k] - np.dot(self.L[j, :j], self.U[:j, k])) / self.L[j, j]

   def solve(self):
      if self.L == None or self.U == None:
         self.decompose()
      # AX = B
      # LU X = B
      # Ly = B
      # UX = y
      y = forward_substitution(self.L, self.b, self.sig_figs)
      return self.L, self.U, backward_substitution(self.U, y, self.sig_figs)

   def getMatrixL(self):
      return self.L

   def getMatrixU(self):
      return self.U