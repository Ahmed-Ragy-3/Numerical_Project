import numpy as np

from commonFunctions import *

def forwardElimination(matrixA, vectorB):
    matrixClone = np.copy(matrixA)
    vectorBClone = np.copy(vectorB)
    multipliers = []
    rows_order = np.arange(len(matrixClone))
    rows = matrixClone.shape[0]

    for r in range(rows - 1):
        
        pivot_forward(r, matrixClone, rows_order, vectorBClone)

        for i in range(r + 1, rows):
            
            if matrixClone[i, r] == 0.0:
                multipliers.append(0.0)
                continue

            multiplier = matrixClone[i, r] / matrixClone[r, r]
            multiplier = roundBy(multiplier)
            multipliers.append(multiplier)
            
            # Using numpy slicing for row operations
            matrixClone[i, r+1:] -= matrixClone[r, r+1:] * multiplier
            matrixClone[i, r+1:] = np.vectorize(roundBy)(matrixClone[i, r+1:])

            vectorBClone[i] -= vectorBClone[r] * multiplier
            vectorBClone[i] = roundBy(vectorBClone[i])

            matrixClone[i, r] = 0.0

    return matrixClone, vectorBClone, multipliers, rows_order

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

m = [
    [2.0, 1.0, 4.0],
    [1.0, 2.0, 3.0],
    [4.0, -1.0, 2.0],
]

b = [
    1.0,
    1.5,
    2.0
]

A, B, multipliers, order = forwardElimination(m, b)
printMatrix(A)
printVector(B)
printVector(multipliers)
print(order)
