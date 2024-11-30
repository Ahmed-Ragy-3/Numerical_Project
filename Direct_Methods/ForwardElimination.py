import numpy as np
from commonFunctions import *

# How to use 
#   create instance of ForwardElimination with matrixA and VectorB
#   then type : instance.eliminateForLU() for a, b, multipliers (LU)
#   then type : instance.eliminateForGauss() for a, b  (Gauss)
#   u can find a test case at the end of the file if u want to test something

class ForwardElimination:
    def __init__(self, matrixA, vectorB=None):
        self.matrixA = np.copy(matrixA)
        self.vectorB = np.copy(vectorB) if vectorB is not None else None
        # self.vectorBExist = True if vectorB is not None else False
        self.rows_order = np.arange(len(matrixA))
        self.rows = matrixA.shape[0]
        self.multipliers = []
        
    def __findPivotRow(self, row):
        max_row = row
        allZeros = True
        
        if row + 1 >= self.rows:
            return row
        
        for i in range(row , self.rows):
            if self.matrixA[i, row + 1] != 0:
                allZeros = False
                break

        if allZeros:
            if row + 1 < self.rows:
                return self.__findPivotRow(row + 1)
            else:
                return max_row
        else:
            for i in range(row, self.rows):
                if self.matrixA[i, row + 1] != 0 :
                    return i
        
        return max_row

    def pivot(self, row):
        max_row = row
        allZeros = True
        
        for i in range(row, self.rows):
            if self.matrixA[i, row] != 0:
                allZeros = False
                break
        if allZeros :
            max_row = self.__findPivotRow(row)
        else:
            for i in range(row + 1, self.rows):
                if abs(self.matrixA[i, row]) > abs(self.matrixA[max_row, row]):
                    max_row = i

        if max_row != row :
            self.matrixA[[row, max_row], :] = self.matrixA[[max_row, row], :]
            
            # if self.vectorBExist:
            self.vectorB[[row, max_row]] = self.vectorB[[max_row, row]]
            
            self.rows_order[[row, max_row]] = self.rows_order[[max_row, row]]

    def eliminateForGauss(self):
        self.eliminateForLU()
        u = self.matrixA
        # if self.vectorBExist:
        b = self.vectorB
        n = self.rows
        for i in range(n):
            j = i
            while j < n and u[i][j] == 0:
                j += 1
            if j == n or u[i][j] == 0:
                continue
            pivot = u[i][j]

            u[i][j] = 1
            for k in range(j + 1, n):
                u[i][k] = u[i][k] / pivot
                u[i][k] = roundBy(u[i][k])
            # if self.vectorBExist:
            b[i] = b[i] / pivot
            b[i] = roundBy(b[i])

            for r in range(i + 1, n):
                mult = u[r][j] / u[i][j]
                mult = roundBy(mult)
                if mult == 0:
                    continue
                # if self.vectorBExist:
                b[r] -= mult * b[i]
                b[r] = roundBy(b[r])
                for c in range(j, n):
                    if c == j:
                        u[r][c] = 0
                        continue
                    u[r][c] -= mult * u[i][c]
                    u[r][c] = roundBy(u[r][c])
        # if self.vectorBExist : return u, b
        return u, b
    
    def eliminateForLU(self):

        for r in range(self.rows - 1):
            
            self.pivot(r)

            for i in range(r + 1, self.rows):
                
                if self.matrixA[i, r] == 0.0:
                    self.multipliers.append(0.0)
                    continue

                multiplier = self.matrixA[i, r] / self.matrixA[r, r]
                multiplier = roundBy(multiplier)
                self.multipliers.append(multiplier)
                
                self.matrixA[i, r+1:] -= self.matrixA[r, r+1:] * multiplier
                self.matrixA[i, r+1:] = np.vectorize(roundBy)(self.matrixA[i, r+1:])

                # if self.vectorBExist :
                self.vectorB[i] -= self.vectorB[r] * multiplier
                self.vectorB[i] = roundBy(self.vectorB[i])

                self.matrixA[i, r] = 0.0

        self.multipliers = np.array(self.multipliers, dtype=float)
        self.rows_order = np.array(self.rows_order, dtype=int)
        
        # if self.vectorBExist :
        # return self.matrixA, self.vectorB, self.multipliers, self.rows_order
        return self.matrixA, self.vectorB, self.multipliers
        # return self.matrixA, self.multipliers, self.rows_order
    
# A = np.array([[0, 5, 2, 3],
#               [0, 1, 2, 3],
#               [0, 0, 0, 0],
#               [0, 0, 0, 1]], dtype=float)
# b = np.array([  5 ,
#                 1 ,
#                 0 ,
#                 1 ], dtype=float)
A = np.array([[2, 1, -1],
              [3, 2, 1],
              [2, -1, 2]], dtype=float)
b = np.array([  1 ,
                10 ,
                6 ], dtype=float)

print("Original Matrix A:")
print(A)
print("Original Vector b:")
print(b)
print(f"{'\033[33m'}-------------------{'\033[0m'}")

fr = ForwardElimination(A, b)

A, b, m = fr.eliminateForLU()

print(f"{'\033[33m'}After Forward Elimination for LU:{'\033[0m'}")
print(f"Matrix A:")
print(np.array2string(A, separator=', '))
print(f"{'\033[33m'}----{'\033[0m'}")
print(f"Vector b:")
print(np.array2string(b, separator=', '))
print(f"{'\033[33m'}----{'\033[0m'}")
print(f"self.multipliers:")
print(np.array2string(m, separator=', '))
print(f"{'\033[33m'}-------------------{'\033[0m'}")
# print(f"order:")
# print(np.array2string(o, separator=', '))
# print("\n" + "-"*30 + "\n")

fr = ForwardElimination(A, b)

A, b = fr.eliminateForGauss()

print(f"{'\033[33m'}After Forward Elimination for Gauss:{'\033[0m'}")
print(f"Matrix A:")
print(np.array2string(A, separator=', '))
print(f"{'\033[33m'}----{'\033[0m'}")
print(f"Vector b:")
print(np.array2string(b, separator=', '))
