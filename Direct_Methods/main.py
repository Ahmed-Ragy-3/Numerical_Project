#                                                      بسم الله الرحمن الرحيم

# Example Usage
from Direct import forwardElimination


matrix = [
    [2, 3, 1, 9],
    [4, 6, 2, 18],
    [1, 16, 1, 66],
]

# Run forward elimination
result, factors, row_order = forwardElimination(matrix)

print("After elimination:")
for row in result:
    print(row)

print("\nFactors used in forward elimination:")
print(factors)

print("\nRow order after pivoting:")
print([r + 1 for r in row_order])  # Adding 1 to match the 1-based row indices
