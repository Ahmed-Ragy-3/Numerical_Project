import numpy as np
from backElimination import backwardElimination
from backElimiationTest import print_matrix_vector
u = np.array([[1.5, -0.5, 0.25],
             [0, 2.3, -0.7],
             [0, 0, 3.9]], dtype=np.float64)

b = np.array([1.25, 2.5, 3.75], dtype=np.float64)

backwardElimination(u, b, 10)

print("original matrix U and vector B\n")
print_matrix_vector(u, b)
print()
print("After Backward Elimination\n")
print_matrix_vector(u, b)
print("-"*50)
