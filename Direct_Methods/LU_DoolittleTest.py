import numpy as np
from LU_Doolittle import Doolittle

A = np.array([[25, 5, 1],
             [64, 8, 1],
             [144, 12, 1]], dtype=np.float64)

b = np.array([106.8, 177.2, 279.2], dtype=np.float64)

print("original matrix A and vector B\n")
print("Original Matrix A:")
print(A)
print()
print("Original Vector B:")
print(b)
print()

p = Doolittle()
L, U, b = p.solve(A = A, b = b, sig_figs = 10)

print("After Decomposition\n")
print("Lower Matrix:\n")
print(L)
print()
print("Upper Matrix:\n")
print(U)
print()
print("Vector B:\n")
print(b)
print()
print("-"*50)