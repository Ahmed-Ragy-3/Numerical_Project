import numpy as np

from commonFunctions import backwardElimination

# Test function for backward elimination


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


def test_backwardElimination():

    test_cases = [
        # Integer test case
        (
            np.array([[2, -1, 1],
                      [0, 3, -2],
                      [0, 0, 4]], dtype=np.float64),  # Significant figures
            np.array([3, 3, 8], dtype=np.float64),
            5
        ),
        # Floating-point test case
        (
            np.array([[1.5, -0.5, 0.25],
                      [0, 2.3, -0.7],
                      [0, 0, 3.9]], dtype=np.float64),  # Significant figures
            np.array([1.25, 2.5, 3.75], dtype=np.float64),
            10
        ),
        # infinite nubmer of solution
        (np.array([[5, 1, 2, 3],
                   [0, 0, 2, 3],
                   [0, 0, 0, 5],
                   [0, 0, 0, 0]], dtype=np.float64), np.array([5, 1, 8, 0], dtype=np.float64), 5
         ),
        # infinite again
        (np.array([[5, 0, 2, 3],
                   [0, 1, 2, 3],
                   [0, 0, 0, 0],
                   [0, 0, 0, 1]], dtype=np.float64), np.array([5, 1, 0, 1], dtype=np.float64), 4)

    ]

    for i, (u, b, sig_fig) in enumerate(test_cases):
        # Print original matrix and vector
        print(f"Test Case {
              i + 1}:\n")
        print("original matrix U and vector B\n")
        print_matrix_vector(u, b)
        print()

        # Apply backward elimination
        u,b = backwardElimination(u, b, sig_fig)

        # Print results
        print("After Backward Elimination\n")
        print_matrix_vector(u, b)
        print("-"*50)


# Run the test
test_backwardElimination()
