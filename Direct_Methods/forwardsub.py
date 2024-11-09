from commonFunctions import printVector, subscript
import numpy as np

def forwardSubstitution(matrix, b): # could be called substitution
    answer = []
    rows = len(matrix)
    free_variables = dict()     # index: x1

    #initialize
    for i in range(rows):
        answer.append(b[i])
        if matrix[i][i] == 0:
            if b[i] != 0: return None 
            free_variables[i] = f"x{subscript(i + 1)}"
    
    def build_answer(row):
        print(f"row = {row}")
        pivot = matrix[row][row]
        
        if row in free_variables:
            answer[row] = free_variables[row]
        else:
            free_str = ""
            for i in range(0, row):
                print(i)
                if isinstance(answer[i], str):
                    free_str += f"-{matrix[row][i] / pivot}{free_variables[i] if i in free_variables else answer[i]}"
                    free_str.replace("--", "+")
                else:
                    print(answer[i])
                    answer[row] -= matrix[row][i] * answer[i]
            
            answer[row] /= pivot
            if free_str != "":
                answer[row] = f"{answer[row]}{free_str}"

    for row in range(rows):
        build_answer(row)
    
    return answer


m = np.array([
    [0, 0, 0],
    [2.56, 1, 0],
    [5.76, 3.5, 1],
], dtype=float)

b = np.array([0, 177.2, 279.2], dtype=float)


result = forwardSubstitution(m.tolist(), b)

if result == None:
    print("no solution")
else:
    printVector(result)

# 106.8
# -96.21
# 0.73