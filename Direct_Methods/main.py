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
    [1.5, -0.5, 0.25],
    [0, 2.3, -0.7],
    [0, 0, 3.9]
]

b = [1.25, 2.5, 3.75]

A, B, multipliers, order = forwardElimination(m, b)
A, B = backwardElimination(A, B)
printMatrix(A)
printVector(B)
print(multipliers)
print(order)
