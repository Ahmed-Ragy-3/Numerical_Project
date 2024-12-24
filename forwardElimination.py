import numpy as np
import commonfunctions


def find_pivot_row(matrix, rows, row):
    """
    Finds the pivot row for a given row during elimination.
    """
    if row + 1 >= rows:
        return row

    for i in range(row, rows):
        if matrix[i, row + 1] != 0:
            return i

    return row


def pivot(matrix, b, rows_order, row, sig_figs):
    """
    Performs pivoting by swapping rows to place the largest element in the pivot position.
    """
    rows = matrix.shape[0]
    max_row = row

    for i in range(row + 1, rows):
        if abs(matrix[i, row]) > abs(matrix[max_row, row]):
            max_row = i

    if max_row != row:
        matrix[[row, max_row], :] = matrix[[max_row, row], :]
        if b is not None:
            b[[row, max_row]] = b[[max_row, row]]
        rows_order[[row, max_row]] = rows_order[[max_row, row]]
        
        commonfunctions.output += f"\nR{row + 1} ←→ R{max_row + 1}"
        commonfunctions.output += "\n" + commonfunctions.stringify_matrix(matrix, sig_figs) + "\n\n"
        


def forward_elimination(matrixA, vectorB, sig_figs=15):
    """
    Performs Gaussian forward elimination with significant figures rounding.
    """
    commonfunctions.output += "\nForward Elimination:\n"
    multipliers = []
    rows_order = np.arange(len(matrixA))
    rows = matrixA.shape[0]

    for r in range(rows - 1):
        pivot(matrixA, vectorB, rows_order, r, sig_figs)
        # print("sig fig = ", sig_figs)

        for i in range(r + 1, rows):
            if matrixA[i, r] == 0.0:
                multipliers.append(0.0)
                continue
           
            multiplier = matrixA[i, r] / matrixA[r, r]
            
            if sig_figs:
                multiplier = commonfunctions.round_to_sig_figs(multiplier, sig_figs)
            multipliers.append(multiplier)

            matrixA[i, r + 1:] -= matrixA[r, r + 1:] * multiplier
            if sig_figs:
                matrixA[i, r + 1:] = np.vectorize(commonfunctions.round_to_sig_figs)(matrixA[i, r + 1:], sig_figs)

            vectorB[i] -= vectorB[r] * multiplier
            if sig_figs:
                vectorB[i] = commonfunctions.round_to_sig_figs(vectorB[i], sig_figs)


            temp = matrixA[i, r]
            matrixA[i, r] = 0.0
            commonfunctions.output += f"\nR{i + 1} ← R{i + 1} - ({temp} / {matrixA[r, r]}) * R{r + 1}"
            commonfunctions.output += "\n" + commonfunctions.stringify_matrix(matrixA, sig_figs) + "\n"

    multipliers = np.array(multipliers, dtype=float)
    rows_order = np.array(rows_order, dtype=int)

    return matrixA, vectorB


def eliminate_for_gauss(matrix, b, sig_figs=15):
    """
    Performs forward elimination for Gaussian elimination.
    """
    rows = matrix.shape[0]

    for i in range(rows):
        rows_order = np.arange(rows)
        pivot(matrix, b, rows_order, i, sig_figs)

        pivot_value = matrix[i, i]
        if pivot_value == 0:
            print(f"Warning: Zero pivot encountered at row {i}.")
            continue

        matrix[i, i:] /= pivot_value
        b[i] /= pivot_value

        if sig_figs:
            matrix[i, i:] = np.vectorize(commonfunctions.round_to_sig_figs)(matrix[i, i:], sig_figs)
            b[i] = commonfunctions.round_to_sig_figs(b[i], sig_figs)

        for j in range(i + 1, rows):
            multiplier = matrix[j, i]
            matrix[j, i:] -= multiplier * matrix[i, i:]
            b[j] -= multiplier * b[i]
            matrix[j, i] = 0

            if sig_figs:
                matrix[j, i:] = np.vectorize(commonfunctions.round_to_sig_figs)(matrix[j, i:], sig_figs)
                b[j] = commonfunctions.round_to_sig_figs(b[j], sig_figs)

    return matrix, b


# # Uncomment for testing
# if __name__ == "__main__":
#     A = np.array([[2, -1, -2], [-4, 6, 3], [-4, -2, 8]], dtype=float)
#     b = np.array([-3, 9, 2], dtype=float)

#     print("Gaussian Elimination:")
#     matrix_gauss, b_gauss = forward_elimination(A, b, sig_figs=4)
#     print("Matrix after elimination:")
#     print(matrix_gauss)
#     print("Vector b after elimination:")
#     print(b_gauss)
