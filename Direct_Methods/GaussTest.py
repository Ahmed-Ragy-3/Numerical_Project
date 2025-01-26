import numpy as np
import Gauss
from commonFunctions import printMatrix, print_matrix_vector

A = np.array([[25, 5, 1],
             [64, 8, 1],
             [144, 12, 1]], dtype=np.float64)

b = np.array([106.8, 177.2, 279.2], dtype=np.float64)

gause = Gauss()

x = gause.s(A = A, b = b, sig_figs = 10)

print("original matrix U and vector B\n")
print_matrix_vector(A, b)
print()
print("After Gause\n")
printMatrix(x)
print("-"*50)