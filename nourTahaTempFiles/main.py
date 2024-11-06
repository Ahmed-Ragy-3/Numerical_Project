from forward_elimination import ForwardElimination

# Example Usage
matrix = [
    [2, 3, 1, 9],
    [4, 6, 2, 18],
    [1, 1, 1, 6],
    
]

fe = ForwardElimination(matrix)
result, factors = fe.forwardElimination()

print("after elimination:")
for row in result:
    print(row)

print("\nFactors used in forward elimination:")
print(factors)

print("\nRow order after pivoting:")
print([r + 1 for r in fe.pivoting.row_order])  # Adding 1 to match the 1-based row indices
