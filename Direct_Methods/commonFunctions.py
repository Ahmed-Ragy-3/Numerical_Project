import math
import numpy as np

significant_digits = 4

subscripts = {0: '₀', 1: '₁', 2: '₂', 3: '₃', 4: '₄', 5: '₅', 6: '₆', 7: '₇', 8: '₈', 9: '₉'}

def printMatrix(matrix):
   for row in matrix:
      print(" ".join(f"{val:.2f}" for val in row))
   print()

def print_matrix_vector(u, b):
    # Print the matrix u with proper formatting
    print("Matrix u:")
    for row in u:
        print(f"[{', '.join([f'{num:.1f}' if isinstance(num, float)
              and num == int(num) else str(num) for num in row])}]")

    # Print the vector b with proper formatting
    print("\nVector b:")
    print(f"[{', '.join([f'{num:.1f}' if isinstance(num, float)
          and num == int(num) else str(num) for num in b])}]")

def subscript(num):
   ret = ""
   
   if num == 0:
      return subscripts[0]  # Handle zero case
   
   while num != 0:
      ret += subscripts[num % 10]
      num //= 10
   return ''.join(reversed(ret))

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