import numpy as np

from Approach import Approach
from commonFunctions import forwardElimination, backwardSubstitution

class Gauss(Approach):
   def __init__(self,A, b, sig_figs=20):
      self.A = np.array(A,dtype=float)
      self.b = np.array(b,dtype=float)
      self.sig_figs = sig_figs

   
   def solve(self):
      # pass and handle A
      matrix = []
      forwardElimination(matrix)
      return backwardSubstitution(matrix)