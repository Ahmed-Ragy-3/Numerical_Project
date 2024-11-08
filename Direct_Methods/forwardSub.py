import copy
import numpy as np
from Direct_Methods.commonFunctions import *

def forwardSubstitution(matrix, b):
   # backward elimination is necessary
   # b = np.array(b, dtype=float)
   answer = np.array(dtype=float)
   rows = len(matrix)
   
   for i in range(rows):
      ans = b[i]
      
      if matrix[i][i] == 0:
         if b[i] != 0:
            return None
         else:
            answer.append(f"x{subscript(i + 1)}")
      else: 
         for j in range(0, i):
            ans -= matrix[i][j] * answer[j]
         
         answer[i] = ans / matrix[i][i]

   return answer