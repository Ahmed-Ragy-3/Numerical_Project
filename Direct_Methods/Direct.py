import numpy as np

from commonFunctions import *

def backwardElimination(u, b): # must be done after forward elimination
   n = len(u)
   for i in range(n-1, -1, -1):
      j = i
      while j < n and u[i][j] == 0:
         j += 1
      if (j == n or u[i][j] == 0):
         continue
      pivot = u[i][j]

      u[i][j] = 1

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
   return u, b

def forwardElimination(matrixA, vectorB):
    multipliers = []
    rows_order = np.arange(len(matrixA))
    rows = matrixA.shape[0]

    for r in range(rows - 1):
        
        pivot_forward(r, matrixA, rows_order, vectorB)

        for i in range(r + 1, rows):
            
            if matrixA[i, r] == 0.0:
                multipliers.append(0.0)
                continue

            multiplier = matrixA[i, r] / matrixA[r, r]
            multiplier = roundBy(multiplier)
            multipliers.append(multiplier)
            
            # Using numpy slicing for row operations
            matrixA[i, r+1:] -= matrixA[r, r+1:] * multiplier
            matrixA[i, r+1:] = np.vectorize(roundBy)(matrixA[i, r+1:])

            vectorB[i] -= vectorB[r] * multiplier
            vectorB[i] = roundBy(vectorB[i])

            matrixA[i, r] = 0.0

    return matrixA, vectorB, multipliers, rows_order

def pivot_forward(row, matrixA, row_order, vectorB):
    n = matrixA.shape[0]
    max_row = row
    
    for i in range(row + 1, n):
        if abs(matrixA[i, row]) > abs(matrixA[max_row, row]):
            max_row = i

    if max_row != row:
        # Swap rows in the matrix
        matrixA[[row, max_row], :] = matrixA[[max_row, row], :]
        
        # Swap elements in the vector
        vectorB[[row, max_row]] = vectorB[[max_row, row]]
        
        # Swap row order
        row_order[[row, max_row]] = row_order[[max_row, row]]
        
        # Uncomment to see swap details
        # print(f"Swapped row {row + 1} with row {max_row + 1}")

def forwardSubstitution(matrix, b): # could be called substitution
    answer = []  # Will hold the results
    rows = len(matrix)
    
    for i in range(rows):
        if(matrix[i][i] == 0):
            answer.append(f"x{subscript(i)}")
        else:
            answer.append(0)

    for i in range(rows):

        if matrix[i][i] == 0:  # Check for zero pivot
            if b[i] != 0:  #(no solution)
                return None
            else:  # Infinite solutions case
                for j in range(rows):
                    if(j == i):
                        continue
                    else:
                        if(matrix[i][j] == 0):
                            continue
                        else:
                            if(isinstance(answer[j], str)):
                                answer[i] = f"{answer[i]} - " + f"({matrix[i][j]})" + f"x{subscript(j)}"
        else:
            answer[i] = b[i]
            for j in range(rows):
                if(j == i):
                    continue
                else:
                    if(matrix[i][j] == 0):
                        continue
                    else:
                        if(isinstance(answer[j], str)):
                            answer[i] = f"{answer[i]} - " + f"({matrix[i][j]})" + f"x{subscript(j)}"
                            
    for i in range(rows):
        if(matrix[i][i] != 0):
            if(isinstance(answer[i], str)):
                answer[i] = f"({answer[i]}) / {matrix[i][i]}" 
            else:
                answer[i] /= matrix[i][i]
    return answer
 
def backwardSubstitution():
   pass
