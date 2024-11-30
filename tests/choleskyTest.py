import numpy as np

from LU_Cholesky import Cholesky


A = np.array([[6, 15, 55], [15, 55, 225], [55, 225, 979]], dtype=float)
b = np.array([1, 2, 3], dtype=float)


chelesky = Cholesky(A,b,4)

chelesky.solve()
print(chelesky.getMatrixL())
print(chelesky.getMatrixU())