import copy
import math

significant_digits = 10

subscripts = {0: '₀', 1: '₁', 2: '₂', 3: '₃', 4: '₄', 5: '₅', 6: '₆', 7: '₇', 8: '₈', 9: '₉'}

def printMatrix(matrix):
   for row in matrix:
      print(row)
   print("\n")
    
def printVector(vector):
   for z in vector:
      print(f"[{z}]")
   print("\n")

def subscript(num):
   ret = ""
   if num == 0:
      return subscripts[0]  # Handle zero case
   while num != 0:
      ret += subscripts[num % 10]
      num //= 10
   return ''.join(reversed(ret))

def roundBy(num):
   if num == 0:
      return 0
   return round(num, significant_digits - int(math.floor(math.log10(abs(num)))) - 1)

def forwardElimination(matrixA, vectorB):
   matrixClone = copy.deepcopy(matrixA)
   vectorBClone = copy.deepcopy(vectorB)
   multipliers = []
   rows_order = list(range(len(matrixClone)))
   rows = len(matrixClone)
    
   for r in range(rows - 1):
        
      pivot_forward(r, matrixClone, rows_order, vectorBClone)
 
      for i in range(r + 1, rows):

         if matrixClone[i][r] == 0.0:
            multipliers.append(0.0)
            continue
 
         multiplier = matrixClone[i][r]/matrixClone[r][r]
         multiplier = roundBy(multiplier)
         multipliers.append(multiplier)
 
         for j in range(r + 1, rows):
            matrixClone[i][j] -= matrixClone[r][j] * multiplier
            matrixClone[i][j] = roundBy(matrixClone[i][j])
            
         vectorBClone[i] -= vectorBClone[r] * multiplier
         vectorBClone[i] = roundBy(vectorBClone[i])

         matrixClone[i][r] = 0.0

   return matrixClone, vectorBClone, multipliers, rows_order

def backwardElimination(u, b):
   n = len(u)
   for i in range(n-1, -1, -1):
      j = i
      while j < n and u[i][j] == 0:
         j += 1
      if (j == n or u[i][j] == 0):
         continue
      pivot = u[i][j]

      u[i][j] = 1

      """ u[i] = u[i]/pivot
      b[i] = b[i]/pivot without sig fig"""

      for k in range(j+1, n):
         u[i][k] = roundBy(u[i][k] / pivot)

      b[i] = roundBy(b[i] / pivot)

      for r in range(i-1, -1, -1):
         mult = roundBy(u[r][j]/u[i][j])
         if (mult == 0):
               continue
         b[r] = roundBy(b[r]-mult*b[i])
         for c in range(j, n):
               if (c == j):
                  u[r][c] = 0
                  continue
               u[r][c] = roundBy(u[r][c]-mult*u[r][c])

      """ without sig fig for r in range (i-1,-1,-1):
         mult = u[r][j]/u[i][j]
         b[r] = b[r]-mult*b[i]
         u[r] = u[r]-mult*u[i] """
   return u, b

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

def backwardSubstitution():
   pass

def pivot_forward(row, matrixA, row_order, vectorB):
   n = len(matrixA)
   max_row = row
    
   for i in range(row + 1, n):
      if abs(matrixA[i][row]) > abs(matrixA[max_row][row]):
         max_row = i

   if max_row != row:
      matrixA[row], matrixA[max_row] = matrixA[max_row], matrixA[row]
      vectorB[row], vectorB[max_row] = vectorB[max_row], vectorB[row]
        
      row_order[row], row_order[max_row] = row_order[max_row], row_order[row]
      # Uncomment to see swap details
      # print(f"Swapped row {row + 1} with row {max_row + 1}")