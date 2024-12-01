import Approach
import numpy as np
from LU import LU
from forwardeli import forwardElimination

class Doolittle(Approach, LU):
   def __init__(self, A, b, sig_figs=20):
      self.A = np.array(A, dtype=float)
      self.b = np.array(b, dtype=float)
      self.sig_figs = sig_figs
      self.L = None
      self.U = None
   
   def solve(self):
      rows = self.A.shape[0]
      U, multipliers = forwardElimination(self)
      index = 0
      L = np.eye(rows, rows)
      for row in range (1, rows):
         for column in range (row):
            L[row][column] = multipliers[index]
            index += 1
      return L, U
   
# print("test")