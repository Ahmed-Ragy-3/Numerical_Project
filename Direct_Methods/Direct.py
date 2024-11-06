import copy
import math

significant_figures = 4

def roundBy(num):
   return round(num, significant_figures - int(math.floor(math.log10(abs(num)))) - 1)

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


def forwardSubstitution():
   pass


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
