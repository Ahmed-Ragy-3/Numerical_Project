#                                                      بسم الله الرحمن الرحيم

# Example Usage
from Direct import *


matrix = [
    [2, 0, 0],
    [0, 0, 0],
    [0, 0, 4],
]
b = [4, 0, 4]

result = forwardSubstitution(matrix, b)

# # Run forward elimination
# result, factors, row_order = forwardElimination(matrix)

# print("After elimination:")
for row in result:
    print(row)

# print("\nFactors used in forward elimination:")
# print(factors)

# print("\nRow order after pivoting:")
# print([r + 1 for r in row_order])  # Adding 1 to match the 1-based row indices


