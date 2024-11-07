import numpy as np
from LU import LU
from Direct import forwardSubstitution,backwardSubstitution
class Cholesky(LU):
    def __init__(self, A, b):
        self.b = b
        self.A = np.array(A, dtype=float)
        self.n = self.A.shape[0]
        self.L = np.zeros((self.n, self.n), dtype=float)
        self.U = np.zeros((self.n, self.n), dtype=float)
        self.result = np.zeros(self.n, dtype=float)

    def decompose(self):
        # Check if the matrix is symmetric
        if self.checkSymmetric():
            for i in range(self.n):
                for j in range(i + 1):
                    sum_val = sum(self.L[i][k] * self.L[j][k] for k in range(j))
                    if i == j:
                        self.L[i][j] = np.sqrt(self.A[i][i] - sum_val)
                    else:
                        self.L[i][j] = (self.A[i][j] - sum_val) / self.L[j][j]
            # Set U = L.T
            self.U = self.L.T
        else:
            raise ValueError("Matrix is not symmetric. Cholesky decomposition requires a symmetric matrix.")

    def solve(self):
        self.decompose()
        y = forwardSubstitution(self.L, self.b)
        print("Y",y)
       # return backwardSubstitution(self.U, y) # uncomment after implement this method

    def checkSymmetric(self) -> bool:
        return np.array_equal(self.A, self.A.T)

    def getMatrixL(self):
        return self.L

    def getMatrixU(self):
        return self.U
