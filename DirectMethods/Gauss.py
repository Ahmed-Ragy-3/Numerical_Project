import numpy as np
from ..Helpers.forwardElimination import forward_elimination
from ..Helpers.backwardSubstitution import backward_substitution

class Gauss():
   def __init__(self, matrix, b, sig_figs=20):
      self.A = np.array(matrix, dtype=float)
      self.b = np.array(b, dtype=float)
      self.sig_figs = sig_figs

   def solve(self):
      forward_elimination(self.A, self.b, self.sig_figs, method="gauss")
      return backward_substitution(self.A, self.b, self.sig_figs)