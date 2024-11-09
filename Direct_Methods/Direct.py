from commonFunctions import *

import numpy as np

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
         
         matrixA[i, r+1:] -= matrixA[r, r+1:] * multiplier
         matrixA[i, r+1:] = np.vectorize(roundBy)(matrixA[i, r+1:])

         vectorB[i] -= vectorB[r] * multiplier
         vectorB[i] = roundBy(vectorB[i])

         matrixA[i, r] = 0.0
   
   multipliers = np.array(multipliers, dtype=float)
   rows_order = np.array(rows_order, dtype=int)

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


def round_to_sig_figs(x, sig_figs):
    if x == 0:
        return 0
    else:
        magnitude = int(np.ceil(np.log10(abs(x))))
        return round(x, sig_figs - magnitude)


def backwardElimination(u, b, sig_fig=20):
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
         u[i][k] = round_to_sig_figs(u[i][k] / pivot, sig_fig)

      b[i] = round_to_sig_figs(b[i] / pivot, sig_fig)

      for r in range(i-1, -1, -1):
         mult = round_to_sig_figs(u[r][j]/u[i][j], sig_fig)
         if (mult == 0):
               continue
         b[r] = round_to_sig_figs(b[r]-mult*b[i], sig_fig)
         for c in range(j, n):
               if (c == j):
                  u[r][c] = 0
                  continue
               u[r][c] = round_to_sig_figs(u[r][c]-mult*u[r][c], sig_fig)
   return u, b


def forwardSubstitution():
    pass


def backwardSubstitution():
    pass


def pivot():
    pass
