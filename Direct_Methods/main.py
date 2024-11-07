#                                                      بسم الله الرحمن الرحيم

# Example Usage
from Direct import *


# matrix = [
#     [2, 0, 0],
#     [0, 0, 0],
#     [0, 0, 4],
# ]
# b = [4, 0, 4]

# result = forwardSubstitution(matrix, b)


m = [
    [1.0, 1.0, -1.0],
    [1.0, -1.0, 2.0],
    [2.0, 1.0, 1.0],
]

b = [
    7.0,
    3.0,
    9.0
]

A, B, multipliers, order = forwardElimination(m, b)
printMatrix(A)
printVector(B)
print(multipliers)
print(order)
