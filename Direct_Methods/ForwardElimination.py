import numpy as np
from commonFunctions import *

# How to use
#   create instance of ForwardElimination with matrixA and VectorB(optional)
#   then type : instance.eliminate()
#   returns in order : matrixA vectorB(if given) multipliersVector rows_orderVector
#   u can find test cases with/out vectorB at the end of the file (modify the last case if u want to test something)

class ForwardElimination:
    def __init__(self, matrixA, vectorB=None):
        self.matrixA = np.copy(matrixA)
        self.vectorB = np.copy(vectorB) if vectorB is not None else None
        self.vectorBExist = True if vectorB is not None else False
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

    def __pivot(self, row):
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
            
            if self.vectorBExist:
                self.vectorB[[row, max_row]] = self.vectorB[[max_row, row]]
            
            self.rows_order[[row, max_row]] = self.rows_order[[max_row, row]]

    def eliminate(self):

        for r in range(self.rows - 1):
            
            self.__pivot(r)

            for i in range(r + 1, self.rows):
                
                if self.matrixA[i, r] == 0.0:
                    self.multipliers.append(0.0)
                    continue

                self.multiplier = self.matrixA[i, r] / self.matrixA[r, r]
                self.multiplier = roundBy(self.multiplier)
                self.multipliers.append(self.multiplier)
                
                self.matrixA[i, r+1:] -= self.matrixA[r, r+1:] * self.multiplier
                self.matrixA[i, r+1:] = np.vectorize(roundBy)(self.matrixA[i, r+1:])

                if self.vectorBExist :
                    self.vectorB[i] -= self.vectorB[r] * self.multiplier
                    self.vectorB[i] = roundBy(self.vectorB[i])

                self.matrixA[i, r] = 0.0
        
        self.multipliers = np.array(self.multipliers, dtype=float)
        self.rows_order = np.array(self.rows_order, dtype=int)
        
        if self.vectorBExist :
            return self.matrixA, self.vectorB, self.multipliers, self.rows_order
        return self.matrixA, self.multipliers, self.rows_order
    
    
test_cases = [
    {"A": np.array([[1, 3, 1],[2, 7, 3],[2, 4, 1]], dtype=float),"b": np.array([100, 500, -100], dtype=float)},
    {"A": np.array([[1, 2, 3],[0, -1, 2],[4, 1, 1]], dtype=float),"b": np.array([10, -1, 5], dtype=float)},
    {"A": np.array([[3, -1, 2],[1, 3, -2],[2, 0, 1]], dtype=float),"b": np.array([8, 4, 3], dtype=float)},
    {"A": np.array([[0, 3, -1],
                    [1, -2, 3],
                    [0, 0, 0]], dtype=float),
        "b": np.array([7, 4, 0], dtype=float)}
]

for idx, case in enumerate(test_cases, 1):
    A = case["A"].copy()
    b = case["b"].copy()
    print(f"{'\033[33m'}Test Case {idx}:{'\033[0m'}")
    print("Original Matrix A:")
    print(A)
    print("Original Vector b:")
    print(b)
    
    fr = ForwardElimination(A, b)
    
    A, b, m, o = fr.eliminate()
    
    print(f"{'\033[33m'}After Forward Elimination:{'\033[0m'}")
    print(f"{'\033[33m'}Matrix A:{'\033[0m'}")
    print(np.array2string(A, separator=', '))
    print(f"{'\033[33m'}Vector b:{'\033[0m'}")
    print(np.array2string(b, separator=', '))
    print(f"{'\033[33m'}self.multipliers:{'\033[0m'}")
    print(np.array2string(m, separator=', '))
    print(f"{'\033[33m'}order:{'\033[0m'}")
    print(np.array2string(o, separator=', '))
    print("\n" + "-"*30 + "\n")


test_cases_with_col_shifts = [
{"A": np.array([[5, 0, 2, 3],[0, 0, 0, 0],[0, 0, 0, 1],[0, 0, 0, 0]], dtype=float)},
{"A": np.array([[0, 0, 0, 1],[0, 0, 0, 0],[0, 2, 0, 0],[0, 0, 0, 0]], dtype=float)},
{"A": np.array([[1, 2, 3, 4],[0, 0, 0, 5],[0, 0, 0, 0],[0, 0, 6, 0]], dtype=float)},
{"A": np.array([[0, 0, 0, 0],[0, 7, 0, 0],[0, 0, 0, 0],[1, 0, 0, 0]], dtype=float)},
{"A": np.array([[0, 0, 1],
                [0, 0, 0],
                [2, 0, 0]], dtype=float)},
{
        "A": np.array([[0, 5, 2,3],
                       [0,1, 2, 3],
                       [0,0,0,0],
                       [0,0,0,1]], dtype=float),
        "b": np.array([5,1,0,1], dtype=float)
    }
]



    
for idx, case in enumerate(test_cases_with_col_shifts, 1):
    A = case["A"].copy()
    print(f"{'\033[33m'}Test Case {idx}:{'\033[0m'}")
    print("Original Matrix A:")
    print(A)
    
    fr = ForwardElimination(A)
    
    A, m, o = fr.eliminate()
    
    print(f"{'\033[33m'}After Forward Elimination:{'\033[0m'}")
    print(f"{'\033[33m'}Matrix A:{'\033[0m'}")
    print(np.array2string(A, separator=', '))
    print(f"{'\033[33m'}self.multipliers:{'\033[0m'}")
    print(np.array2string(m, separator=', '))
    print(f"{'\033[33m'}order:{'\033[0m'}")
    print(np.array2string(o, separator=', '))
    print("\n" + "-"*30 + "\n")


# test_case_10x10 = {
#     "A": np.array([
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 3, 0, 0, 0],
#         [0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
#         [0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
#         [1, 0, 0, 0, 0, 0, 0, 0, 9, 0],
#         [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 6, 0, 0, 0, 0, 0, 0]
#     ], dtype=float),
#     "b": np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], dtype=float)
# }

# # Assuming ForwardElimination is defined
# A = test_case_10x10["A"]
# b = test_case_10x10["b"]

# print("Original Matrix A:")
# print(A)
# print("\nOriginal Vector b:")
# print(b)

# fr = ForwardElimination(A, b)
# A_result, b_result, multipliers, order = fr.eliminate()

# print("\nAfter Forward Elimination:")
# print("Matrix A:")
# print(A_result)
# print("Vector b:")
# print(b_result)
# print("Multipliers:")
# print(multipliers)
# print("Row Order:")
# print(order)
