from pivoting import Pivoting

class ForwardElimination:
    def __init__(self, matrix):
        self.matrix = matrix
        self.row_order = list(range(len(matrix)))  # Initialize row_order
        self.pivoting = Pivoting(self.matrix, self.row_order)
        self.factors = []

    def forwardElimination(self):
        rows = len(self.matrix)
        for i in range(rows):
            # Pivoting
            self.pivoting.apply_pivoting(i)
            # Forward elimination
            for j in range(i + 1, rows):
                if self.matrix[i][i] == 0:
                    continue
                factor = self.matrix[j][i] / self.matrix[i][i]
                # Eliminate the element
                for k in range(i, len(self.matrix[j])):
                    self.matrix[j][k] -= factor * self.matrix[i][k]
                    
                self.matrix[j][i] = 0
                
                for row in self.matrix:
                    print(row)
                print("\n")
                # Store the factor
                self.factors.append(float(factor))

        return self.matrix, self.factors