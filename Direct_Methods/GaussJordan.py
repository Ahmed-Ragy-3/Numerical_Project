from ..Approach import Approach
import numpy as np
from .Direct import forwardElimination, backwardElimination, forwardSubstitution

class GaussJordan(Approach):
   
   def __init__(self, matrix, b, ans):
      self.A = np.array(matrix, dtype=float)
      self.B = np.array(b, dtype=float)
      self.answer = np.array(ans, dtype=float)
   
   def solve(self):
      matrixA, vectorB = forwardElimination(self.A, self.B)
      matrixA, vectorB = backwardElimination(matrixA, vectorB)
      self.answer = forwardSubstitution(matrixA, vectorB)
      return self.answer