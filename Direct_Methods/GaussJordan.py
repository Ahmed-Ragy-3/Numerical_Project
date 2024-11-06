from ..Approach import Approach
from .Direct import forwardElimination, backwardElimination, forwardSubstitution

class GaussJordan(Approach):
   def __init__(self, matrix, b):
      self.matrix = matrix
      self.b = b
   
   def solve(self):
      matrix = forwardElimination(self.matrix)
      matrix = backwardElimination(matrix)
      return forwardSubstitution(matrix), matrix