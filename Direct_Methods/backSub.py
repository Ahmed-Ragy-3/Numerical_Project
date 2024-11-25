import numpy as np
from commonFunctions import subscript
from Direct import backwardElimination

def print_matrix(matrix):

    for row in matrix:
        print(row)
    
        print("\n")
        


def backwardSubstitution(matrix, b, reduced=False):
    # don't check solvability
    n = len(matrix)
    answer = [""] * n
    free_variables = dict()     # index: x1
    
    if not reduced:
        backwardElimination(matrix, b)
    
    print_matrix(matrix)
    print_matrix(b)
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
    
    print(not_free)
    for i in range(n):
        if i not in not_free:
            free_variables[i] = "x" + subscript(i + 1)
            answer[i] = free_variables[i]
            
    if len(free_variables) == 0:
        return b
    
    print(free_variables)
    
    for i in range(n):
        if i in free_variables:
            continue
        for j in range(i + 1, n):
            if matrix[i][j] != 0:
                answer[i] += f" - {convert_int(matrix[i][j])}{answer[j]}"
                answer[i] = str.replace(answer[i], "- -","+ ")
            
    
    return answer

def convert_int(num):
    if abs(num - int(num)) < 1e-4:
        return int(num)
    return num

m = np.array([
    [1, 2, 8, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0]
], dtype=float)

b = np.array([5, 0, 4, 0], dtype=float)

result = backwardSubstitution(m, b)

print(result)

# if result == None:
#     print("no solution")
# else:
#     printVector(result)

        
# 106.8
# -96.21
# 0.73