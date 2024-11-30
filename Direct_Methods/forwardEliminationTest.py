import numpy as np


from commonFunctions import *

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


test_cases = [
    {
        "A": np.array([[1, 3, 1],
                       [2, 7, 3],
                       [2, 4, 1]], dtype=float),
        "b": np.array([100, 500, -100], dtype=float)
    },
    {
        "A": np.array([[1, 2, 3],
                       [0, -1, 2],
                       [4, 1, 1]], dtype=float),
        "b": np.array([10, -1, 5], dtype=float)
    },
    {
        "A": np.array([[3, -1, 2],
                       [1, 3, -2],
                       [2, 0, 1]], dtype=float),
        "b": np.array([8, 4, 3], dtype=float)
    },
    {
        "A": np.array([[0, 3, -1],
                       [1, -2, 3],
                       [0, 0, 0]], dtype=float),
        "b": np.array([7, 4, 0], dtype=float)
    }
]

for idx, case in enumerate(test_cases, 1):
    A = case["A"].copy()
    b = case["b"].copy()
    print(f"{'\033[33m'}Test Case {idx}:{'\033[0m'}")
    print("Original Matrix A:")
    print(A)
    print("Original Vector b:")
    print(b)
    
    A, b, m, o = forwardElimination(A, b)
    
    print(f"{'\033[33m'}After Forward Elimination:{'\033[0m'}")
    print(f"{'\033[33m'}Matrix A:{'\033[0m'}")
    print(np.array2string(A, separator=', '))
    print(f"{'\033[33m'}Vector b:{'\033[0m'}")
    print(np.array2string(b, separator=', '))
    print(f"{'\033[33m'}multipliers:{'\033[0m'}")
    print(np.array2string(m, separator=', '))
    print(f"{'\033[33m'}order:{'\033[0m'}")
    print(np.array2string(o, separator=', '))
    print("\n" + "-"*30 + "\n")