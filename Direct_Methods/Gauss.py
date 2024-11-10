from Approach import Approach
from Direct import forwardElimination, backwardSubstitution

class Gauss(Approach):
   def __init__(self):
      pass
   
   def solve(self,A, b, sig_figs=20, initial_guess=None, tolerance=0, max_iterations=100):
      # pass
      matrix = []
      forwardElimination(matrix)
      return backwardSubstitution(matrix)