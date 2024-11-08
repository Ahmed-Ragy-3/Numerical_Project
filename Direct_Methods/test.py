import numpy as np

from Direct import *

m = np.array([
    [1, 2, 3, 4, 5],
    [2, 4, 6, 8, 10],
    [2, 6, 9, 12, 15],
    [4, 8, 12, 16, 20],
    [5, 10, 15, 20, 25]
], dtype=np.float64)

b = np.array([10, 20, 30, 40, 50], dtype=np.float64)

m, b, ml, r = forwardElimination(m, b)
print_matrix_vector(m,b)

backwardElimination(m, b)
print_matrix_vector(m,b)

result = forwardSubstitution(m,b)

if result == None:
    print("no solution")
else:
    printVector(result)



