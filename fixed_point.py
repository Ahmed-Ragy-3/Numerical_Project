
import sys
from math import log
import numpy as np
from ProcessFunction import ProcessFunction
from false_position_method import round_significant
from tabulate import tabulate

def round_significant(value, sig_figs=sys.float_info.dig):
   if abs(value) < 1e-12:
      return 0
   elif value == float('inf') or value == -float('inf'):
      return float('inf')
   else:
      return round(value, sig_figs - int(np.floor(np.log10(abs(value)))) - 1)

# self.function, self.max_iterations, self.tolerance, self.significant_figures, initialguess
def fixed_point(function: ProcessFunction, max_iterations=50, error_tol=1e-5,
                significant_figures=sys.float_info.dig, initial_guess=0):
    #function = ProcessFunction(function_string)

    next_root = initial_guess
    previous_root = None

    table = []
    steps = []
    lines = []

    for i in range(max_iterations):
        steps.append(f"Iteration {i+1}")
        root = next_root
        print("root = ", root)
        g = function.evaluate(root, significant_figures)
        steps.append(f"Next Root = g({root}) = {g}")
        next_root = g
        
        if i==0:
            lines.append([root, 0, root, function.evaluate(root, significant_figures)])
            lines.append([root, function.evaluate(root, significant_figures), next_root, function.evaluate(root, significant_figures)])
        else:
            lines.append([root, function.evaluate(previous_root, significant_figures), root, function.evaluate(root, significant_figures)])
            lines.append([root, function.evaluate(root, significant_figures), next_root, function.evaluate(root, significant_figures)])
        
        previous_root = root

        absolute_error = round_significant(abs(next_root - root), significant_figures)
        steps.append(f"Absolute error = abs({root} - {root}) = {absolute_error}")

        relative_error = round_significant(abs((next_root - root) / root) * 100, significant_figures)
        steps.append(f"Relative error = abs(({next_root} - {root}) / {next_root}) * 100% = {relative_error}%")
        
        correct_digits = np.floor(2 - log(2 * abs(relative_error)))
        if correct_digits < 0:
            correct_digits = 0
        steps.append(f"Correct Digits = floor(2 - log(2 * abs({relative_error})) = {correct_digits}")

        steps.append("\n")
        
        table.append(
            [
                i + 1,
                f"{root}",
                f"{g}",
                f"{next_root}",
                f"{absolute_error}" if absolute_error != float("inf") else "_",
                f"{relative_error}%" if relative_error != float("inf") else "_",
                f"{correct_digits}" if correct_digits != float("inf") else "_"
            ]
        )
        
        if relative_error < error_tol:
            table_str = tabulate(table, headers=["Iteration", "xᵢ", "g(xᵢ)","xᵢ₊₁",
                                                 "Absolute Error", "Relative Error", "Correct Digits"], tablefmt="grid")
            lines.append([0, 0, 10, 10])
            #function.plot_function(-10, 10, lines, method="Fixed Point")
            return next_root, "\n".join(steps), table_str, i+1, correct_digits, relative_error, absolute_error, lines
            #root, steps, table, iterations_done, correct_digits, relative_error, absolute_error
        if abs(next_root) > 1e10:  # Prevent overflow
            raise OverflowError("Value too large, possible divergence.")
    raise ValueError(f"Fixed Point method failed to solve this function with max iterations : {max_iterations} ")

def main():
    
    # function = ProcessFunction("x ^ 3 - x ^ 2 - 10 * x + 7")
    function = ProcessFunction("sqrt((1.7*x+2.5) / 0.9)")
    
    x, steps, table_str, iterations, correct_digits, relative_error, absolute_error, lines = fixed_point(
        function, initial_guess=4, significant_figures=10, error_tol=0.01
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