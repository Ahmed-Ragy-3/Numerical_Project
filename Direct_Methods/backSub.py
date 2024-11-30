import numpy as np
from commonFunctions import subscript
from Direct import backwardElimination

def print_matrix(matrix):
    for r in matrix:
        print(r)

def stringify(coeff, free_variables):
    answer = [""] * len(coeff)
    for r in range(len(coeff)):
        if free_variables[r]:
            answer[r] = "𝑥" + subscript(r + 1)
            continue
        
        for c in range(r):
            if c == 0:
                continue
            
            answer[r] += f"{c}" + f"𝑥{subscript(r + 1)}" if r != 0 else ""
    
    return answer
    
def advanced_back_sub(matrix, b):

    n = len(matrix)
    free_variables = [False] * n     # boolean
    coefficients = []
    
    # initialize
    for i in range(n):
        coefficients.append([0] * (n - i))
        coefficients[i][0] = b[i]

        if matrix[i][i] == 0:
            if b[i] != 0:
                return None
            free_variables[i] = True
    
    print_matrix(coefficients)
    # To multiply a list or matrix by a constant, it should be numpy
    for row in range(n - 2, -1, -1):
        print("------------------")
        if free_variables[row]:
            continue
        
        for col in range(len(coefficients[row])):
            if free_variables[col] and col != 0:
                coefficients[row][col] -= matrix[row][col]
                continue
            
            for var in range(row + 1, len(coefficients[col])):
                print(f"row = {row}, col = {col}, var = {var}")
                print(f"m = {matrix[row][var]}")
                coefficients[row][col] -= matrix[row][var] * coefficients[var][col]
                
    
    #row = 1, col = 0, var =
    # coefficients[1][0] -= matrix[1][2] * coefficients[2][0] + matrix[1][3] * coefficients[3][0]
    #
    
    #  num  x2 x3 x4
    # [1.0, 0, 0, 0]
    # [2.0, 0, 0]
    # [0  , 0]
    # [3.0]
    
    #  1 1 1 0 | 1
    #  0 1 6 2 | 1
    #  0 0 0 0 | 0
    #  0 0 0 1 | 3
    
    print(free_variables)
    
    print_matrix(coefficients)
    print(free_variables)
    # print(stringify(coefficients, free_variables))
    return stringify(coefficients, free_variables)
    # pass


def backwardSubstitution(matrix, b, reduced=False):
    n = len(matrix)
    answer = [""] * n
    free_variables = dict()     # index: x1
    
    if not reduced:
        backwardElimination(matrix, b)
    
    # print_matrix(matrix)
    # print_matrix(b)
    
    # answer[2] = x3
    # answer[3] = x4
    # answer[0] = "1 - matrix[i][j]{answer[j]} - matrix[i][j]{answer[j]}"
             
    # 1 2 2 8    1
    # 0 1 4 2    0
    # 0 0 0 1    0
    # 0 0 0 0    0
    
    not_free = []
    for i in range(n):
        answer[i] = str(convert_int(b[i]))
        reach_end = True
        for j in range(i, n):
            if matrix[i][j] != 0:
                not_free.append(j)
                reach_end = False
                break
        
        if reach_end and b[i] != 0:
            return None
    
    # print(not_free)
    for i in range(n):
        if i not in not_free:
            free_variables[i] = "𝑥" + subscript(i + 1)
            answer[i] = free_variables[i]
            
    if len(free_variables) == 0:
        return b
    
    # print(free_variables)
    
    for i in range(n):
        if i in free_variables:
            continue
        for j in range(i + 1, n):
            if matrix[i][j] != 0 and answer[j] != 0:
                answer[i] += f" - {convert_int(matrix[i][j])}{answer[j]}"
                answer[i] = str.replace(answer[i], "- -","+ ")
            
    return answer

def convert_int(num):
    if abs(num - int(num)) < 1e-4:
        return int(num)
    return num

m = np.array([
    [0, 3, 1, 3],
    [0, 1, 6, 2],
    [0, 0, 0, 0],
    [0, 0, 0, 1]
], dtype=float)

b = np.array([1, 1, 0, 3], dtype=float)

result = advanced_back_sub(m, b)
print(result)

# if result == None:
#     print("no solution")
# else:
#     printVector(result)