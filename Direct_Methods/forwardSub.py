import copy
import numpy as np
from backSub import backwardSubstitution
from forwardeli import forwardElimination

subscripts = {0: '₀', 1: '₁', 2: '₂', 3: '₃', 4: '₄', 5: '₅', 6: '₆', 7: '₇', 8: '₈', 9: '₉'}

def reverse(arr):
    n = len(arr)
    for i in range(int(n / 2)):
        arr[i], arr[n - i - 1] = arr[n - i - 1], arr[i]
        
    return copy.copy(arr)
    

def forwardSubstitution(matrix, b, reduced=False):
    # print(reverse(matrix))
    # print(reverse(b))
    if not reduced:
        matrix , b , _ , _ = forwardElimination(matrix, b)
        
    print(matrix)
        
    answer = backwardSubstitution(matrix, b, reduced=True)
    return answer

# Test the function
m = np.array([
    [1, 0, 0],
    [0, 0, 5],
    [0, 0, 0],
], dtype=float)

b = np.array([
    1,
    8,
    0
], dtype=float)

result = forwardSubstitution(m, b, reduced=True)
if result is None:
    print("No solution exists.")
else:
    for z in result:
        print(z)

