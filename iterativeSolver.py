import numpy as np
import commonfunctions

# def round_to_sig_figs(x, sig_figs):
#     if x == 0:
#         return 0
#     else:
#         magnitude = int(np.ceil(np.log10(abs(x))))
#         return round(x, sig_figs - magnitude)


def iterative_solver(A, b, sig_figs=20, initial_guess=None, tolerance=0, max_iterations=100, isJacobi=False):
    # method = "Jacobi" if isJacobi else "Gauss-Seidel"
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

            x[i] = commonfunctions.round_to_sig_figs((b[i] - sum) / A[i, i], sig_figs)

        # Calculate relative error with a small constant to avoid division by zero
        matrix_error = np.abs((x - x_old) / (x + 1e-10))
        error = np.max(matrix_error)

        if error < tolerance:
            return x,k+1

    return x, k+1
