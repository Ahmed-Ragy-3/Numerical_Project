import numpy as np
import commonfunctions
from commonfunctions import round_to_sig_figs




def convert_to_diagonally_dominant(input_matrix,input_B):

    n = len(input_matrix)  # Size of the matrix
    matrix = np.array(input_matrix, dtype=float)  # Ensure matrix is a NumPy array for easier manipulation
    B = np.array(input_B, dtype=float)
    for col in range(n):
        # Find a row with a sufficiently large diagonal element
        for row in range(col, n):
            diagonal_element = abs(matrix[row][col])
            other_elements_sum = sum(abs(matrix[row][k]) for k in range(n) if k != col)

            if diagonal_element >= other_elements_sum:
                # Swap the rows in the matrix directly
                matrix[[col, row]] = matrix[[row, col]]
                B[[col, row]] = B [[row, col]]
                break
        else:
            # Could not find a suitable row for this column
            return False, np.array(input_matrix),np.array(input_B)

    # Verify the result is diagonally dominant
    for row in range(n):
        diagonal_element = abs(matrix[row][row])
        other_elements_sum = sum(abs(matrix[row][k]) for k in range(n) if k != row)
        if diagonal_element < other_elements_sum:
            return False, np.array(input_matrix),np.array(input_B)

    return True, matrix,B


def iterative_solver(A, b, sig_figs=15, initial_guess=None, tolerance=0, max_iterations=100, isJacobi=False):
    # method = "Jacobi" if isJacobi else "Gauss-Seidel"
    # print(A, b, sig_figs, initial_guess, tolerance, max_iterations, isJacobi)
    n = len(b)
    x = np.zeros_like(b, dtype=np.float64) if initial_guess is None else initial_guess.copy()
    isDiagonalyDom , A, b = convert_to_diagonally_dominant(A,b)
    
    
    k = 0
    for k in range(max_iterations):
        x_old = x.copy()

        for i in range(n):
            sum = 0
            for j in range(n):
                if j == i:
                    continue
                if isJacobi:
                    sum += A[i][j] * x_old[j]
                else:
                    sum += A[i][j] * x[j]

            x[i] = round_to_sig_figs((b[i] - sum) / A[i, i], sig_figs)

        j = 1
        commonfunctions.output += f"Iteration {k + 1}:\n"
        for ans in x:
            commonfunctions.output += f"𝑥{commonfunctions.subscript(j)} = "
            commonfunctions.output += str(commonfunctions.round_to_sig_figs(ans, sig_figs))
            j += 1
            commonfunctions.output += "\n"
        
        commonfunctions.output += "\n"
        # Calculate relative error with a small constant to avoid division by zero
        matrix_error = np.abs((x - x_old) / (x + 1e-10))
        error = np.max(matrix_error)

        if error < tolerance:
            return x,k+1

    return x, k+1
