class Pivoting:
    def __init__(self, matrix, row_order):
        self.matrix = matrix
        self.row_order = row_order

    def apply_pivoting(self, row):
        # Find the index of the row with the largest element in column `row`
        n = len(self.matrix)
        max_row = row
        for i in range(row + 1, n):
            if abs(self.matrix[i][row]) > abs(self.matrix[max_row][row]):
                max_row = i
        
        if max_row != row:
            # Swap the rows in the matrix
            self.matrix[row], self.matrix[max_row] = self.matrix[max_row], self.matrix[row]
            # Also update the row_order array to reflect the swap
            self.row_order[row], self.row_order[max_row] = self.row_order[max_row], self.row_order[row]
            # print(f"Swapped row {row + 1} with row {max_row + 1}")
        
        return self.matrix