def forwardElimination(matrix, factors, row_order):
   rows = len(matrix)
   for i in range(rows):

      # Pivoting
      pivot(i, matrix, row_order)

      # Forward elimination
      for j in range(i + 1, rows):
         if matrix[i][i] == 0:
            continue
         factor = matrix[j][i] / matrix[i][i]

         # Eliminate the element
         for k in range(i, len(matrix[j])):
            matrix[j][k] -= factor * matrix[i][k]
            
         matrix[j][i] = 0 # set to zero even after elimination
         
         # for debuging
         for row in matrix:
            print(row)
         print("\n")

         # Store the factor
         factors.append(float(factor))

   return matrix, factors, row_order


def backwardElimination():
   pass


def forwardSubstitution():
   pass


def backwardSubstitution():
   pass


def pivot(row, matrix, row_order):
   # Find index of row with the largest absolute value
   n = len(matrix)
   max_row = row
   for i in range(row + 1, n):
      if abs(matrix[i][row]) > abs(matrix[max_row][row]):
            max_row = i
   
   if max_row != row:
      # Swap rows
      matrix[row], matrix[max_row] = matrix[max_row], matrix[row]
      # update row_order array
      row_order[row], row_order[max_row] = row_order[max_row], row_order[row]
      # print(f"Swapped row {row + 1} with row {max_row + 1}")
