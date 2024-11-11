import numpy as np
from GaussSeidel import Seidel
def test_iterative_solver():
    # Define test cases as tuples of (A matrix, b vector, initial guess, tolerance, max_iterations, sig_figs)
    test_cases = [
        (
            np.array([[4, 1, 2],
                      [1, 5, 1],
                      [2, 1, 3]], dtype=np.float64),
            np.array([4, 7, 3], dtype=np.float64),
            4,                # Significant figures
            np.zeros(3),     # Initial guess
            1e-5,            # Tolerance
            100            # Max iterations
        ),
        (
            np.array([[10, -1, 2, 0],
                      [-1, 11, -1, 3],
                      [2, -1, 10, -1],
                      [0, 3, -1, 8]], dtype=np.float64),
            np.array([6, 25, -11, 15], dtype=np.float64),
            4,                  # Significant figures
            np.zeros(4),     # Initial guess
            1e-5,            # Tolerance
            100,             # Max iterations
        ),
        (
            np.array([[3, 1],
                      [1, 2]], dtype=np.float64),
            np.array([9, 8], dtype=np.float64),
            5,               # Significant figures
            np.zeros(2),     # Initial guess
            1e-5,            # Tolerance
            100,             # Max iterations
        ),
        ( #sheet example 1
            np.array([[5, -1, 1],
                      [2, 8, -1],
                      [-1, 1, 4]], dtype=np.float64),
            np.array([10, 11, 3], dtype=np.float64),
            20,                # Significant figures
            np.zeros(3),     # Initial guess
            0,            # Tolerance
            3            # Max iterations
        ),
        ( #sheet example 2
            np.array([[9, 1, 1],
                      [2, 10, 3],
                      [3, 4, 11]], dtype=np.float64),
            np.array([10, 19, 7], dtype=np.float64),
            20,                # Significant figures
            np.zeros(3),     # Initial guess
            0,            # Tolerance
            6            # Max iterations
        )
        
        
    ]

    for i, (A, b, sig_figs, initial_guess, tolerance, max_iterations) in enumerate(test_cases):
        p = Seidel(A,b,sig_figs,initial_guess,tolerance,max_iterations)
        print(f"Test Case {i + 1}")
        print("Coefficient matrix A:\n", A)
        print("Right-hand side vector b:\n", b)

        # Test with Gauss-Seidel method
        print("\nGauss-Seidel Method:\n")
        a,b,x = p.solve()
        print("Solution:")
        print(x)

        

        print("-" * 50)  # Separator for readability


# Run the test
test_iterative_solver()