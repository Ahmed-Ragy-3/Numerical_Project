import numpy as np


def round_to_sig_figs(x, sig_figs):
    if x == 0:
        return 0
    else:
        magnitude = int(np.ceil(np.log10(abs(x))))
        return round(x, sig_figs - magnitude)


def iterative_solver(A, b, sig_figs=20, initial_guess=None, tolerance=0, max_iterations=100, isJacobi=False):
    # method = "Jacobi" if isJacobi else "Gauss-Seidel"
    # print(A, b, sig_figs, initial_guess, tolerance, max_iterations, isJacobi)
    n = len(b)
    x = np.zeros_like(b, dtype=np.float64) if initial_guess is None else initial_guess.copy()

    k = 0
    for k in range(max_iterations):
        x_old = x.copy()

        for i in range(n):
            sum = 0
            for j in range(n):
                if (j == i):
                    continue
                if (isJacobi):
                    sum += A[i][j] * x_old[j]
                else:
                    sum += A[i][j] * x[j]

            x[i] = round_to_sig_figs((b[i] - sum) / A[i, i], sig_figs)

        # Calculate relative error with a small constant to avoid division by zero
        matrix_error = np.abs((x - x_old) / (x + 1e-10))
        error = np.max(matrix_error)

        if error < tolerance:
            return x,k+1

    return x, k+1


# def test_iterative_solver():
#     # Define test cases as tuples of (A matrix, b vector, initial guess, tolerance, max_iterations, sig_figs)
#     test_cases = [
#         (
#             np.array([[4, 1, 2],
#                       [1, 5, 1],
#                       [2, 1, 3]], dtype=np.float64),
#             np.array([4, 7, 3], dtype=np.float64),
#             4,                # Significant figures
#             np.zeros(3),     # Initial guess
#             1e-5,            # Tolerance
#             100            # Max iterations
#         ),
#         (
#             np.array([[10, -1, 2, 0],
#                       [-1, 11, -1, 3],
#                       [2, -1, 10, -1],
#                       [0, 3, -1, 8]], dtype=np.float64),
#             np.array([6, 25, -11, 15], dtype=np.float64),
#             4,                  # Significant figures
#             np.zeros(4),     # Initial guess
#             1e-5,            # Tolerance
#             100,             # Max iterations
#         ),
#         (
#             np.array([[3, 1],
#                       [1, 2]], dtype=np.float64),
#             np.array([9, 8], dtype=np.float64),
#             5,               # Significant figures
#             np.zeros(2),     # Initial guess
#             1e-5,            # Tolerance
#             100,             # Max iterations
#         ),
#         ( #sheet example 1
#             np.array([[5, -1, 1],
#                       [2, 8, -1],
#                       [-1, 1, 4]], dtype=np.float64),
#             np.array([10, 11, 3], dtype=np.float64),
#             20,                # Significant figures
#             np.zeros(3),     # Initial guess
#             0,            # Tolerance
#             3            # Max iterations
#         ),
#         ( #sheet example 2
#             np.array([[9, 1, 1],
#                       [2, 10, 3],
#                       [3, 4, 11]], dtype=np.float64),
#             np.array([10, 19, 7], dtype=np.float64),
#             20,                # Significant figures
#             np.zeros(3),     # Initial guess
#             0,            # Tolerance
#             6            # Max iterations
#         )
        
        
#     ]

#     for i, (A, b, sig_figs, initial_guess, tolerance, max_iterations) in enumerate(test_cases):
#         print(f"Test Case {i + 1}")
#         print("Coefficient matrix A:\n", A)
#         print("Right-hand side vector b:\n", b)

#         # Test with Gauss-Seidel method
#         print("\nGauss-Seidel Method:")
#         solution_seidel = iterative_solver(A, b, sig_figs, initial_guess=initial_guess, tolerance=tolerance,
#                                            max_iterations=max_iterations)
#         print("Solution:", solution_seidel)

#         # Test with Jacobi method
#         print("\nJacobi Method:")
#         solution_jacobi = iterative_solver(A, b, sig_figs, initial_guess=initial_guess, tolerance=tolerance,
#                                            max_iterations=max_iterations, isJacobi=True)
#         print("Solution:", solution_jacobi)

#         print("-" * 50)  # Separator for readability


# # Run the test
# test_iterative_solver()
