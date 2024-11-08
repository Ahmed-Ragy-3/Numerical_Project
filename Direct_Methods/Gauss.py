from ..Iterative_Methods.Approach import Approach
from .Direct import forwardElimination, backwardSubstitution

class Gauss(Approach):
   def __init__(self):
      pass
   
   def solve(self):
      # pass
      matrix = []
      forwardElimination(matrix)
      return backwardSubstitution(matrix)