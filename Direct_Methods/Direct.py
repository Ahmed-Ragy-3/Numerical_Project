import copy
import math

significant_digits = 4

subscripts = {0: '₀', 1: '₁', 2: '₂', 3: '₃', 4: '₄', 5: '₅', 6: '₆', 7: '₇', 8: '₈', 9: '₉'}

def subscript(num):
   ret = ""
   if num == 0:
      return subscripts[0]  # Handle zero case
   while num != 0:
      ret += subscripts[num % 10]
      num //= 10
   return ''.join(reversed(ret))

def roundBy(num):
   return round(num, significant_digits - int(math.floor(math.log10(abs(num)))) - 1)

def forwardElimination(matrix):
   matrixClone = copy.deepcopy(matrix)
   factors = []
   row_order = list(range(len(matrixClone)))
   rows = len(matrixClone)
   for i in range(rows - 1):
      
      # Pivoting
      pivot(i, matrixClone, row_order)

      # Forward elimination
      for j in range(i + 1, rows):
         if matrixClone[j][i] == 0.0:
            factors.append(0.0)
            continue
         factor = matrixClone[j][i] / matrixClone[i][i]
         factor = roundBy(factor)

         # Eliminate the element
         for k in range(i+1, len(matrixClone[j])):
            matrixClone[j][k] -= factor * matrixClone[i][k]
         
         matrixClone[j][i] = 0 # set to zero even after elimination
         
         # for debuging
         for row in matrixClone:
            print(row)
         print("\n")

         # Store the factor
         factors.append(factor)

   return matrixClone, factors, row_order


def backwardElimination():
   pass

# ragy
def forwardSubstitution(matrix, b):
   matrix_copy = copy.deepcopy(matrix)
   answer = []
   for i in range(0, len(matrix)):
      if matrix[i][i] == 0:
         if b[i] != 0:
            return None
         else:
            answer.append(f"x{subscript(i + 1)}")
      else:
         answer.append(roundBy(b[i] / matrix[i][i]))
   
   return answer


def backwardSubstitution():
   pass


def pivot(row, matrix, row_order):
   # Find index of row with the largest absolute value
   n = len(matrix)
   max_row = row
   for i in range(row + 1, n):
      if abs(matrix[i][row]) > abs(matrix[max_row][row]):
            max_row = i
   
   if max_row != row:
      # Swap rows
      matrix[row], matrix[max_row] = matrix[max_row], matrix[row]
      # update row_order array
      row_order[row], row_order[max_row] = row_order[max_row], row_order[row]
      # print(f"Swapped row {row + 1} with row {max_row + 1}")
