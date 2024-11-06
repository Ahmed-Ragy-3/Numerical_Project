#                                                      بسم الله الرحمن الرحيم

from Direct_Methods.Direct import forwardElimination 
from Direct_Methods.Direct import pivot 

# Example Usage
matrix = [
    [2, 3, 1, 9],
    [4, 6, 2, 18],
    [1, 1, 1, 6],
]

factors = []
row_order = list(range(len(matrix)))

# Run forward elimination
result, factors, row_order = forwardElimination(matrix, factors, row_order)

print("After elimination:")
for row in result:
    print(row)

print("\nFactors used in forward elimination:")
print(factors)

print("\nRow order after pivoting:")
print([r + 1 for r in row_order])  # Adding 1 to match the 1-based row indices
