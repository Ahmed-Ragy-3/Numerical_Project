from Approach import Approach
from Direct import forwardElimination, backwardElimination, forwardSubstitution
import numpy as np

class GaussJordan(Approach):
   def __init__(self, A, b, sig_figs=20):
      self.A = np.array(A, dtype=float)
      self.b = np.array(b, dtype=float)
      self.sig_figs = sig_figs
   
   def solve(self):
      # pass
      matrix = []
      forwardElimination(matrix)
      backwardElimination(matrix)
      return forwardSubstitution(matrix)