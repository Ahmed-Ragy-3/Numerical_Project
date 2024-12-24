from forwardElimination import forward_elimination
from backwardElimination import backward_elimination
from forwardSubstitution import forward_substitution

class GaussJordan:
   
   def __init__(self, matrix, b, sig_figs):
      self.A = matrix
      self.B = b
      self.sig_figs = sig_figs
   
   def solve(self):
      forward_elimination(self.A, self.B, self.sig_figs)
      # print("After forward elimination")
      # print(self.A)
      backward_elimination(self.A, self.B, sig_fig=self.sig_figs)
      # print("After backward elimination")
      # print(self.A)
      return forward_substitution(self.A, self.B, sig_figs=self.sig_figs, reduced=True)