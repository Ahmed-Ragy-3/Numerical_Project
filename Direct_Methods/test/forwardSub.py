import numpy as np
from commonFunctions import *

# def forwardSubstitution(matrix, b):
#    # backward elimination is necessary
#    # b = np.array(b, dtype=float)
#    answer = []
#    rows = len(matrix)
   
#    for i in range(rows):
#       ans = b[i]
      
#       if matrix[i][i] == 0:
#          if b[i] != 0:
#             return None
#          else:
#             answer.append(f"x{subscript(i + 1)}")
#       else: 
#          for j in range(0, i):
#             ans -= matrix[i][j] * answer[j]
         
#          answer[i] = ans / matrix[i][i]

#    return answer


subscripts = {0: '₀', 1: '₁', 2: '₂', 3: '₃', 4: '₄', 5: '₅', 6: '₆', 7: '₇', 8: '₈', 9: '₉'}

def forwardSubstitution(matrix, b):# backward elimination is necessary
    answer = []  # Will hold the results
    rows = len(matrix)

    for i in range(rows):
        ans = b[i]

        if matrix[i][i] == 0:  # Check for zero pivot
            if b[i] != 0:  # Contradiction in the system
                return None
            else:  # Infinite solutions case
                answer.append(f"x{subscript(i + 1)}")
                continue
        else:
            expression = f"{b[i]}"
            for j in range(i):
                if isinstance(answer[j], str):  # Symbolic expression
                    expression += f" - ({matrix[i][j]} * {answer[j]})"
                else:
                    expression += f" - {matrix[i][j] * answer[j]}"
            
            # Store as expression or computed value
            if any(isinstance(el, str) for el in answer[:i]):
                answer.append(f"({expression}) / {matrix[i][i]}")
            else:
                answer.append(eval(expression) / matrix[i][i])

    return answer

# Test the function
m = [
    [1.0, 3.0, 0.0],
    [0.0, 4.0, 0.0],
    [4.0, -1.0, 2.0],
]

b = [
    1.0,
    2.0,
    2.0
]

result = forwardSubstitution(m, b)
if result is None:
    print("No solution exists.")
else:
    for z in result:
        print(z)

