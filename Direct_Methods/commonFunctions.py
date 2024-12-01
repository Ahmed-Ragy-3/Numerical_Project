import math
import numpy as np

significant_digits = 4

subscripts = {0: '₀', 1: '₁', 2: '₂', 3: '₃', 4: '₄', 5: '₅', 6: '₆', 7: '₇', 8: '₈', 9: '₉'}

def subscript(num):
   ret = ""
   
   if num == 0:
      return subscripts[0]  # Handle zero case
   
   while num != 0:
      ret += subscripts[num % 10]
      num //= 10
   return 'x'.join(reversed(ret))


def pivoting(U) :
   n = len(U)
   freeVar  = [False] * n
   pivot = np.zeros((n, 2))
   transitions = 0
   
   for i in range(n) :
      j = i
      while j < n and U[i][j] == 0:
         if i==0 or (i == n-1 and transitions == 0):
            freeVar[j] = True
         elif j - transitions > 0 and j != n-1:
            freeVar[j] = True
         j += 1
         transitions += 1
      if j == n:
         pivot[i,0] = -1
         pivot[i,1] = -1
         continue
      pivot[i, 0] = i
      pivot[i, 1] = j

   return pivot, freeVar


def printMatrix(matrix):
   for row in matrix:
      print(" ".join(f"{val:.2f}" for val in row))
   print()

def print_matrix_vector(u, b):
    # Print the matrix u with proper formatting
    print("Matrix u:")
    for row in u:
        print(f"[{', '.join([f'{num:.1f}' if isinstance(num, float) and num == int(num) else str(num) for num in row])}]")

    # Print the vector b with proper formatting
    print("\nVector b:")
    print(f"[{', '.join([f'{num:.1f}' if isinstance(num, float) and num == int(num) else str(num) for num in b])}]")


def roundBy(num):
   if num == 0:
      return 0
   return round(num, significant_digits - int(math.floor(math.log10(abs(num)))) - 1)


def round_to_sig_figs(x, sig_figs):
    if x == 0:
        return 0
    else:
        magnitude = int(np.ceil(np.log10(abs(x))))
        return round(x, sig_figs - magnitude)


def backwardElimination(u, b, sig_fig=20):
   n = len(u)
   for i in range(n-1, -1, -1):
      j = i
      while j < n and u[i][j] == 0:
         j += 1
      if (j == n or u[i][j] == 0):
         continue
      pivot = u[i][j]

      u[i][j] = 1

      for k in range(j+1, n):
         u[i][k] = round_to_sig_figs(u[i][k] / pivot, sig_fig)

      b[i] = round_to_sig_figs(b[i] / pivot, sig_fig)

      for r in range(i-1, -1, -1):
         mult = round_to_sig_figs(u[r][j]/u[i][j], sig_fig)
         if (mult == 0):
               continue
         b[r] = round_to_sig_figs(b[r]-mult*b[i], sig_fig)
         for c in range(j, n):
               if (c == j):
                  u[r][c] = 0
                  continue
               u[r][c] = round_to_sig_figs(u[r][c]-mult*u[r][c], sig_fig)
   
   return u, b


def forward_substitution(matrix, b, reduced=False):
   """
   Solves the system of linear equations Lx = b using forward substitution.
   
   Parameters:
      matrix (2D array): Lower triangular matrix L.
      b (1D array): Right-hand side vector b.
   
   Returns:
      x (1D array): Solution vector x.
   """
   # if reduced:
   #    return infinite_substitution(matrix, b)
   
   n = len(b)
   answer = np.zeros_like(b, dtype=np.float64)
   
   # Iterate over each row to solve for x[i]
   for i in range(n):
      if matrix[i, i] == 0:
         raise ValueError("In forward substitution: Matrix is singular or near-singular.")
      
      # Compute x[i]
      answer[i] = (b[i] - np.dot(matrix[i, :i], answer[:i])) / matrix[i, i]
   
   return answer


def backward_substitution(matrix, b):
   """
   Solves the system of linear equations Ax = b using backward substitution.
   
   Parameters:
      matrix (2D array): Upper triangular matrix A.
      b (1D array): Right-hand side vector b.
   
   Returns:
      x (1D array): Solution vector x.
   """
   n = len(b)
   answer = np.zeros_like(b, dtype=np.float64)
   
   # Start from the last row and move upwards
   for i in range(n - 1, -1, -1):
      if matrix[i, i] == 0:
         raise ValueError("In back substitution: Matrix is singular or near-singular.")
      
      # Calculate the value of x[i]
      answer[i] = (b[i] - np.dot(matrix[i, i + 1:], answer[i + 1:])) / matrix[i, i]
   
   return answer
