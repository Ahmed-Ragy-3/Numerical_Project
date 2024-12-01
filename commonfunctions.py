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
