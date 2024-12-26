from colorama import Fore, Style, init

import sys
from math import log
import math
from math import isinf
import numpy as np
from ProcessFunction import ProcessFunction
from tabulate import tabulate

EPSILON = 1e-15


def round_significant(value, sig_figs):
    if value == 0:
        return 0
    elif value == float('inf') or value == -float('inf'):
        return float('inf')
    else:
        return round(value, sig_figs - int(np.floor(np.log10(abs(value)))) - 1)


def newton_raphson(function: ProcessFunction, max_iterations=50, error_tol=1e-5,
                   significant_figures=sys.float_info.dig, initial_guess=0):
    previous_root = None
    root = initial_guess
    i = 0
    table = []
    steps = []
    lines = []

    absolute_error = float('inf')
    relative_error = float('inf')
    table_str = ""
    correct_digits = 0

    def end():
        table_str = tabulate(table, headers=["Iteration", "xᵢ₋₁", "xᵢ", "f(xᵢ)", "f'(xᵢ)",
                                             "Absolute Error", "Relative Error", "Correct Digits"], tablefmt="grid")
        return (root, "\n".join(steps), "\n" + table_str, i + 1, correct_digits, relative_error, absolute_error), lines

    for i in range(max_iterations):
        steps.append(f"Iteration {i + 1}")
        previous_root = root
        previous_root = round_significant(previous_root, significant_figures)
        print(f"Previous root: {previous_root}")

        f = function.evaluate(previous_root, significant_figures)
        f = round_significant(f,significant_figures)
        steps.append(f"f({round_significant(previous_root, significant_figures)}) = {f}")

        f_dash = function.evaluate_first_derivative(previous_root, significant_figures)
        f_dash = round_significant(f_dash, significant_figures)
        steps.append(f"f'({previous_root}) = {f_dash}")

        if f_dash == 0:
            steps.insert(0, f"At iteration {i + 1}: Newton Raphson cannot solve this method (f'(x) = 0)\n")
            return end()
            # raise ValueError("Newton Raphson cannot solve this method (f'(x) = 0)")

        lines.append([root, 0, previous_root, function.evaluate(previous_root)])
        root = round_significant(previous_root - (f / f_dash), significant_figures)
        lines.append([previous_root, function.evaluate(previous_root), root, 0])

        absolute_error = round_significant(abs(root - previous_root), significant_figures)
        steps.append(f"Absolute error = abs({root} - {previous_root}) = {absolute_error}")

        relative_error = abs(1 - round_significant(abs(previous_root / root), significant_figures)) * 100
        relative_error = round_significant(relative_error, significant_figures)
        steps.append(f"Relative error = abs(({root} - {previous_root}) / {root}) * 100 % = {relative_error}%")

        correct_digits = np.floor(2 - math.log10(2 * abs(relative_error))) if relative_error > 0 else significant_figures
        correct_digits = max(correct_digits, 0)
        steps.append(f"Correct Digits = {correct_digits}")

        steps.append(f"Root : {round_significant(root,significant_figures)}\n")

        table.append(
            [
                i + 1,
                f"{previous_root}",
                f"{root}",
                f"{f}",
                f"{f_dash}",
                f"{absolute_error}" if relative_error != float("inf") else "_",
                f"{relative_error}%" if relative_error != float("inf") else "_",
                f"{correct_digits}"
            ]
        )

        if absolute_error < error_tol or relative_error < error_tol:
            break

    steps.insert(0, "Newton failed to solve this function (Diverge)\n")
    return end()


def main():
    function = ProcessFunction("sqrt((1.7*x+2.5) / 0.9)")
    x, steps, table_str, iterations, correct_digits, relative_error, absolute_error, lines = newton_raphson(
        function, max_iterations=10, initial_guess=4, significant_figures=10, error_tol=0.01
    )

    print(x)
    print(steps)
    print(table_str)
    print(iterations)
    print(correct_digits)
    print(absolute_error)
    print(relative_error)


if __name__ == "__main__":
    main()
