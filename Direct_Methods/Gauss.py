# from ..Approach import Approach/
import numpy as np
from forwardeli import forwardElimination
from commonFunctions import backward_substitution

class Gauss():
   def __init__(self, matrix, b, sig_figs=20):
      self.A = np.array(matrix, dtype=float)
      self.b = np.array(b, dtype=float)
      self.sig_figs = sig_figs

   def solve(self):
      forwardElimination(self.A, self.b, self.sig_figs)
      return backward_substitution(self.A, self.b, self.sig_figs)