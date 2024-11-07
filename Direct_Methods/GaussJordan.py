from ..Iterative_Methods.Approach import Approach
from .Direct import forwardElimination, backwardElimination, forwardSubstitution

class GaussJordan(Approach):
   def __init__(self):
      pass
   
   def solve(self):
      # pass
      matrix = []
      forwardElimination(matrix)
      backwardElimination(matrix)
      return forwardSubstitution(matrix)