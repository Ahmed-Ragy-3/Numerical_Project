from ..Approach import Approach
from .Direct import forwardElimination, backwardElimination, forwardSubstitution

class GaussJordan(Approach):
   def __init__(self, matrix, b):
      self.matrix = matrix
      self.b = b
   
   def solve(self):
      matrixA, vectorB = forwardElimination(self.matrix, self.b)
      matrixA, vectorB = backwardElimination(matrixA, vectorB)
      return forwardSubstitution(matrixA, vectorB), matrixA