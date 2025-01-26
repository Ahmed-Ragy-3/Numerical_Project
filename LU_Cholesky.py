import numpy as np
from forwardSubstitution import forward_substitution
from backwardSubstitution import backward_substitution
from commonfunctions import round_to_sig_figs
class Cholesky:
    def __init__(self, A, b, sig_figs=20):
        self.b = b
        self.A = A
        self.n = self.A.shape[0]
        self.L = None
        self.U = None
        self.result = np.zeros(self.n, dtype=float)
        self.sig_figs = sig_figs

    def setB(self, b):
      self.b = b

    def decompose(self):
        # Check if the matrix is symmetric
        
        self.L = np.zeros((self.n, self.n), dtype=float)
        self.U = np.zeros((self.n, self.n), dtype=float)
        
        if self.checkSymmetric():
            for i in range(self.n):
                for j in range(i + 1):
                    sum_val = sum(self.L[i][k] * self.L[j][k] for k in range(j))
                    if i == j:
                        self.L[i][j] = np.sqrt(self.A[i][i] - sum_val)
                    else:
                        self.L[i][j] = (self.A[i][j] - sum_val) / self.L[j][j]
            # Set U = L.T
            applySignificantFigure = np.vectorize(lambda x: round_to_sig_figs(x, self.sig_figs))
            self.L = applySignificantFigure(self.L)
            self.U = self.L.T
        else:
            raise ValueError("Matrix is not symmetric. Cholesky decomposition requires a symmetric matrix.")

    def solve(self):
        if self.L == None or self.U == None:
            self.decompose()
            
        y = forward_substitution(self.L, self.b, self.sig_figs)
        
        return self.L, self.U, backward_substitution(self.U, y, self.sig_figs)

    def checkSymmetric(self) -> bool:
        return np.array_equal(self.A, self.A.T)

    def getMatrixL(self):
        return self.L

    def getMatrixU(self):
        return self.U