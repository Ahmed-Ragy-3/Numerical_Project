import sys
from math import log, floor
import numpy as np
from ProcessFunction import ProcessFunction
from tabulate import tabulate

def fixed_point(function_string, initial_guess=0, max_iterations=50, error_tol=1e-5,
                significant_figures=sys.float_info.dig):
    function = ProcessFunction(function_string)


    next_root = initial_guess

    table = []
    steps = []
    lines = []

    for i in range(max_iterations):
        steps.append(f"Iteration {i + 1}")
        root = next_root
        g = function.evaluate(root, significant_figures)
        steps.append(f"g({root}) = {g}")

        next_root = g

        lines.append(root)

        if i != 0:
            absolute_error = ProcessFunction.round_significant(abs(next_root - root), significant_figures)
            steps.append(f"Absolute error = abs({root} - {root}) = {absolute_error}")

            relative_error = ProcessFunction.round_significant(abs((next_root - root) / root) * 100,
                                                               significant_figures)
            steps.append(
                f"Relative error = abs((root - previous_root) / root) * 100% = abs(({next_root} - {root}) / {next_root}) * 100% = {relative_error}%")
            correct_digits = floor(2 - log(2 * abs(relative_error)))
            if correct_digits < 0:
                correct_digits = 0
            steps.append(f"Correct Digits Error = {correct_digits}")
        else:
            absolute_error = float('inf')
            relative_error = float('inf')
            correct_digits = float('inf')
            steps.append("Since it is the first iteration, relative error cannot be calculated.")

        steps.append("\n")
        # Check if relative error reached tolerance
        table.append(
            [
                i + 1,
                f"{root}",
                f"{g}",
                f"{absolute_error}" if absolute_error != float("inf") else "_",
                f"{relative_error}%" if relative_error != float("inf") else "_",
                f"{correct_digits}" if correct_digits != float("inf") else "_"
            ]
        )

        if relative_error < error_tol:
            table_str = tabulate(table, headers=["Iteration", "Root", "g(x)",
                                                 "Absolute Error", "Relative Error", "Correct Digits"], tablefmt="grid")

            return root, "\n".join(steps), table_str, i + 1, correct_digits, relative_error, absolute_error

    raise ValueError(f"Fixed Point method failed to solve this function with max iterations : {max_iterations} ")

def main():
    x, steps, table_str, iterations, correct_digits, relative_error, absolute_error = fixed_point(
        "sqrt((1.7*x+2.5)/0.9)", initial_guess=5, significant_figures=10, error_tol=0.01)

    print(x)
    print(steps)
    print(table_str)
    print(iterations)
    print(correct_digits)
    print(absolute_error)
    print(relative_error)

if __name__ == "__main__":
    main()