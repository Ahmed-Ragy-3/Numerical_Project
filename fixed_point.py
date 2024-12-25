from colorama import Fore, Style, init

import sys
from math import log
import numpy as np
from ProcessFunction import ProcessFunction
from false_position_method import round_significant
from tabulate import tabulate

def round_significant(value, sig_figs=sys.float_info.dig):
   if value == 0:
      return 0
   elif value == float('inf') or value == -float('inf'):
      return float('inf')
   else:
      return round(value, sig_figs - int(np.floor(np.log10(abs(value)))) - 1)


def fixed_point(function_string, initial_guess=0, max_iterations=50, error_tol=1e-5,
                significant_figures=sys.float_info.dig):
    function = ProcessFunction(function_string)


    next_root = initial_guess
    previous_root = None

    table = []
    steps = []
    lines = []

    for i in range(max_iterations):
        steps.append(f"Iteration {i+1}")
        root = next_root
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

        relative_error = round_significant(abs((next_root - root) / root) * 100,
                                                           significant_figures)
        steps.append(
            f"Relative error = abs(({next_root} - {root}) / {next_root}) * 100% = {relative_error}%")
        correct_digits = np.floor(2 - log(2 * abs(relative_error)))
        if correct_digits < 0:
            correct_digits = 0
        steps.append(f"Correct Digits = floor(2 - log(2 * abs({relative_error})) = {correct_digits}")

        steps.append("\n")

        table.append(
            [
                i + 1,
                f"{Fore.BLUE}{root}{Style.RESET_ALL}",
                f"{Fore.GREEN}{g}{Style.RESET_ALL}",
                f"{Fore.RED}{next_root}{Style.RESET_ALL}",
                f"{Fore.YELLOW}{absolute_error}{Style.RESET_ALL}" if absolute_error != float("inf") else "_",
                f"{Fore.CYAN}{relative_error}%{Style.RESET_ALL}" if relative_error != float("inf") else "_",
                f"{Fore.MAGENTA}{correct_digits}{Style.RESET_ALL}" if correct_digits != float("inf") else "_"
            ]
        )

        if relative_error < error_tol:
            table_str = tabulate(table, headers=[f"Iteration", f"{Fore.BLUE}Root{Style.RESET_ALL}", f"{Fore.GREEN}g(x){Style.RESET_ALL}",f"{Fore.RED}Next Root{Style.RESET_ALL}",
                                                 f"{Fore.YELLOW}Absolute Error{Style.RESET_ALL}", f"{Fore.CYAN}Relative Error{Style.RESET_ALL}", f"{Fore.MAGENTA}Correct Digits{Style.RESET_ALL}"], tablefmt="grid")
            lines.append([0, 0, 10, 10])
            #function.plot_function(-10, 10, lines, method="Fixed Point")
            return next_root, "\n".join(steps), table_str, i+1, correct_digits, relative_error, absolute_error

    raise ValueError(f"Fixed Point method failed to solve this function with max iterations : {max_iterations} ")

def main():
    x, steps, table_str, iterations, correct_digits, relative_error, absolute_error = fixed_point(
        "sqrt((1.7*x+2.5) / 0.9)", initial_guess=1, significant_figures=10, error_tol=0.01)

    print(x)
    print(steps)
    print(table_str)
    print(iterations)
    print(correct_digits)
    print(absolute_error)
    print(relative_error)

if __name__ == "__main__":
    main()