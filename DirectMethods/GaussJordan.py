import numpy as np
from ..Helpers.forwardElimination import forward_elimination
from ..Helpers.backwardElimination import backward_elimination
from ..Helpers.forwardSubstitution import forward_substitution

class GaussJordan:
   
   def __init__(self, matrix, b, sig_figs):
      self.A = matrix
      self.B = b
      self.sig_figs = sig_figs
   
   def solve(self):
      forward_elimination(self.A, self.B, self.sig_figs)
      backward_elimination(self.A, self.B, sig_figs=self.sig_figs)
      return forward_substitution(self.A, self.B, sig_figs=self.sig_figs, reduced=True)