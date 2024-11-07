import copy

from Direct_Methods.commonFunctions import *

# ragy
def forwardSubstitution(matrix, b):
   matrix_copy = copy.deepcopy(matrix)
   answer = []
   for i in range(0, len(matrix)):
      if matrix[i][i] == 0:
         if b[i] != 0:
            return None
         else:
            answer.append(f"x{subscript(i + 1)}") # no need for this
      else:
         answer.append(roundBy(b[i] / matrix[i][i]))
   
   return answer