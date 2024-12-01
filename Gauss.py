from forwardElimination import forward_elimination
from backwardSubstitution import backward_substitution

class Gauss:
   def __init__(self, matrix, b, sig_figs=20):
      self.A = matrix
      self.b = b
      self.sig_figs = sig_figs

   def solve(self):
      forward_elimination(self.A, self.b, self.sig_figs)
      return backward_substitution(self.A, self.b, self.sig_figs)