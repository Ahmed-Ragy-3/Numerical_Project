import numpy as np
from LU import LU
from Direct import forwardSubstitution,backwardSubstitution
class Crout(LU):
    def __init__(self, A, b):
        self.b = b
        self.A = np.array(A, dtype=float)
        self.n = self.A.shape[0]
        self.L = np.zeros((self.n, self.n), dtype=float)
        self.U = np.eye(self.n, dtype=float)  # creates a matrix with ones on the main diagonal

    def decompose(self):
        # Crout's decomposition process
        for j in range(self.n):
            for i in range(j, self.n):
                self.L[i, j] = self.A[i, j] - np.dot(self.L[i, :j], self.U[:j, j])

            for k in range(j + 1, self.n):
                self.U[j, k] = (self.A[j, k] - np.dot(self.L[j, :j], self.U[:j, k])) / self.L[j, j]

    def solve(self):
        self.decompose()
        y = forwardSubstitution(self.L, self.b)
        print("Y = ",y)
      #  return backwardSubstitution(self.U, y)

    def getMatrixL(self):
        return self.L

    def getMatrixU(self):
        return self.U
