import numpy as np
from LU_Crout import Crout
from LU_Cholesky import Cholesky

A = np.array([[4, -2, 1], [-2, 4, -2], [1, -2, 3]], dtype=float)
b = np.array([1, 2, 3], dtype=float)

crout = Crout(A, b)

solution = crout.solve()
print(crout.getMatrixL())
print(crout.getMatrixU())
# Print the solution
print("Solution:", solution)
# In this case, let's use numpy's linear algebra solver to check the result:
expected_solution = np.linalg.solve(A, b)
print("Expected Solution:", expected_solution)
#check if both are equal
if np.allclose(solution, expected_solution, atol=1e-10):
    print("Crout's method passed the test!")
else:
    print("Crout's method failed the test.")
