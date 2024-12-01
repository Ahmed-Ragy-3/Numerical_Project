# import numpy as np
# from commonfunctions import round_to_sig_figs


# def find_pivot_row(matrix, rows, row):
#     """
#     Finds the pivot row for a given row during elimination.
#     """
#     if row + 1 >= rows:
#         return row

#     for i in range(row, rows):
#         if matrix[i, row + 1] != 0:
#             return i

#     return row


# def pivot(matrix, b, rows_order, row):
#     """
#     Performs pivoting by swapping rows to place the largest element in the pivot position.
#     """
#     rows = matrix.shape[0]
#     max_row = row

#     for i in range(row + 1, rows):
#         if abs(matrix[i, row]) > abs(matrix[max_row, row]):
#             max_row = i

#     if max_row != row:
#         matrix[[row, max_row], :] = matrix[[max_row, row], :]
#         if b is not None:
#             b[[row, max_row]] = b[[max_row, row]]
#         rows_order[[row, max_row]] = rows_order[[max_row, row]]


# def eliminate_for_gauss(matrix, b, sig_figs):
#     """
#     Performs forward elimination for Gaussian elimination.
#     """
#     # matrix = np.copy(matrix)
#     # b = np.copy(b)
#     rows = matrix.shape[0]

#     for i in range(rows):
#         rows_order = np.arange(rows)
#         pivot(matrix, b, rows_order, i)

#         pivot_value = matrix[i, i]
#         if pivot_value == 0:
#             continue

#         matrix[i, i:] /= pivot_value
#         b[i] /= pivot_value

#         if sig_figs:
#             matrix[i, i:] = np.vectorize(round_to_sig_figs)(matrix[i, i:], sig_figs)
#             b[i] = round_to_sig_figs(b[i], sig_figs)

#         for j in range(i + 1, rows):
#             multiplier = matrix[j, i]
#             matrix[j, i:] -= multiplier * matrix[i, i:]
#             b[j] -= multiplier * b[i]
#             matrix[j, i] = 0

#             if sig_figs:
#                 matrix[j, i:] = np.vectorize(round_to_sig_figs)(matrix[j, i:], sig_figs)
#                 b[j] = round_to_sig_figs(b[j], sig_figs)

#     return matrix, b


# def eliminate_for_lu(matrix, b, sig_figs):
#     """
#     Performs forward elimination for LU decomposition.
#     """
#     # matrix = np.copy(matrix)
#     # b = np.copy(b)
#     rows = matrix.shape[0]
#     multipliers = []

#     for r in range(rows - 1):
#         rows_order = np.arange(rows)
#         pivot(matrix, b, rows_order, r)

#         for i in range(r + 1, rows):
#             if matrix[i, r] == 0.0:
#                 multipliers.append(0.0)
#                 continue

#             multiplier = matrix[i, r] / matrix[r, r]
#             multiplier = round_to_sig_figs(multiplier, sig_figs)
#             multipliers.append(multiplier)

#             matrix[i, r + 1:] -= matrix[r, r + 1:] * multiplier
#             b[i] -= b[r] * multiplier

#             if sig_figs:
#                 matrix[i, r + 1:] = np.vectorize(round_to_sig_figs)(matrix[i, r + 1:], sig_figs)
#                 b[i] = round_to_sig_figs(b[i], sig_figs)

#             matrix[i, r] = 0.0

#     return matrix, b, np.array(multipliers, dtype=float)


# def forward_elimination(matrix, b, sig_figs=20, method="gauss"):
#     """
#     Wrapper for forward elimination using Gaussian elimination or LU decomposition.
#     """
#     if method == "gauss":
#         print("wfwffw")
#         return eliminate_for_gauss(matrix, b, sig_figs)
#     elif method == "lu":
#         return eliminate_for_lu(matrix, b, sig_figs)
#     else:
#         raise ValueError("Invalid method. Use 'gauss' or 'lu'.")



# if __name__ == "__main__":
#     A = np.array([[2, -1, -2], [-4, 6, 3], [-4, -2, 8]], dtype=float)
#     b = np.array([-3, 9, 2], dtype=float)

#     print("Gaussian Elimination:")
#     matrix_gauss, b_gauss = forward_elimination(A, b, method="gauss", sig_figs=4)
#     print("Matrix after elimination:")
#     print(matrix_gauss)
#     print("Vector b after elimination:")
#     print(b_gauss)

#     print("\nLU Decomposition:")
#     matrix_lu, b_lu, multipliers = forward_elimination(A, b, method="lu", sig_figs=4)

# #     print("Matrix after elimination:")
# #     print(matrix_lu)
# #     print("Vector b after elimination:")
# #     print(b_lu)
# #     print("Multipliers:")
# #     print(multipliers)



import numpy as np
from commonfunctions import round_to_sig_figs


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


def pivot(matrix, b, rows_order, row):
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


def forward_elimination(matrixA, vectorB, sig_figs=None):
    """
    Performs Gaussian forward elimination with significant figures rounding.
    """
    multipliers = []
    rows_order = np.arange(len(matrixA))
    rows = matrixA.shape[0]

    for r in range(rows - 1):
        pivot(matrixA, vectorB, rows_order, r)

        for i in range(r + 1, rows):
            if matrixA[i, r] == 0.0:
                multipliers.append(0.0)
                continue

            multiplier = matrixA[i, r] / matrixA[r, r]
            if sig_figs:
                multiplier = round_to_sig_figs(multiplier, sig_figs)
            multipliers.append(multiplier)

            matrixA[i, r + 1:] -= matrixA[r, r + 1:] * multiplier
            if sig_figs:
                matrixA[i, r + 1:] = np.vectorize(round_to_sig_figs)(matrixA[i, r + 1:], sig_figs)

            vectorB[i] -= vectorB[r] * multiplier
            if sig_figs:
                vectorB[i] = round_to_sig_figs(vectorB[i], sig_figs)

            matrixA[i, r] = 0.0

    multipliers = np.array(multipliers, dtype=float)
    rows_order = np.array(rows_order, dtype=int)

    return matrixA, vectorB


def eliminate_for_gauss(matrix, b, sig_figs=None):
    """
    Performs forward elimination for Gaussian elimination.
    """
    rows = matrix.shape[0]

    for i in range(rows):
        rows_order = np.arange(rows)
        pivot(matrix, b, rows_order, i)

        pivot_value = matrix[i, i]
        if pivot_value == 0:
            print(f"Warning: Zero pivot encountered at row {i}.")
            continue

        matrix[i, i:] /= pivot_value
        b[i] /= pivot_value

        if sig_figs:
            matrix[i, i:] = np.vectorize(round_to_sig_figs)(matrix[i, i:], sig_figs)
            b[i] = round_to_sig_figs(b[i], sig_figs)

        for j in range(i + 1, rows):
            multiplier = matrix[j, i]
            matrix[j, i:] -= multiplier * matrix[i, i:]
            b[j] -= multiplier * b[i]
            matrix[j, i] = 0

            if sig_figs:
                matrix[j, i:] = np.vectorize(round_to_sig_figs)(matrix[j, i:], sig_figs)
                b[j] = round_to_sig_figs(b[j], sig_figs)

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
