from ProcessFunction import ProcessFunction
from math import log,floor,pi
import sys
import numpy as np
from false_position_method import round_significant
from tabulate import tabulate

def round_significant(value, sig_figs):
    if value == 0:
        return 0
    elif value == float('inf') or value == -float('inf'):
        return float('inf')
    else:
        return round(value, sig_figs - int(np.floor(np.log10(abs(value)))) - 1)

# self.function, self.max_iterations, self.tolerance, self.significant_figures
def modified_raphson(pf: ProcessFunction, max_iterations=50, error=1e-5, 
                    significant_figures=sys.float_info.dig, initial_guess=0):
    # pf = ProcessFunction(inputString)
    x = initial_guess
    lines = []
    steps = []
    table = []
    correct_digits = 0

    relative_error = float('inf')
    for i in range(max_iterations):
        steps.append("\n")
        steps.append(f"Iteration {i + 1}")
        try: 
         # for case f=1/x
            f = pf.evaluate(x, significant_figures)
            steps.append(f"f({x}) = {f}")
            f_dash = pf.evaluate_first_derivative(x, significant_figures)
            steps.append(f"f'({x}) = {f_dash}")
            f_double_dash = pf.evaluate_second_derivative(x, significant_figures)
            steps.append(f"f''({x}) = {f_double_dash}")
        except ZeroDivisionError as e:
            raise ValueError(f"Division by zero occurred during evaluation: {e} at x = {x}")

        # Avoid division by zero 
        denominator = round_significant(abs(f_dash ** 2 - f * f_double_dash), significant_figures)
        if denominator == 0:
            raise ValueError(f"Division by zero in denominator at iteration {i + 1}")

        x_new = round_significant(x - ((f * f_dash) / denominator), significant_figures)
        
        # lines.append([x_new, function.evaluate(previous_root), root, 0])
              
        # Absolute relative error
        absolute_error = round_significant(abs(x_new - x), significant_figures)
        steps.append(f"Absolute error = abs({x} - {x_new}) = {absolute_error}")

        if x_new != 0:
            relative_error = round_significant((abs(absolute_error / x_new))*100, significant_figures)
            steps.append(f"Relative error = abs(({x_new} - {x}) / {x_new}) * 100 % = {relative_error}%")
            
            if 2 * abs(relative_error) > 0:
                correct_digits = floor(2 - log(2 * abs(relative_error), 10))
                correct_digits = max(correct_digits, 0)
            else:
                correct_digits = significant_figures
                
        
        steps.append("\n")
        table.append([i + 1,
                      f"{x}",
                      f"{x_new}",
                      f"{f}",
                      f"{f_dash}",
                      f"{f_double_dash}",
                      f"{correct_digits}",
                      f"{relative_error}%" if relative_error != float("inf") else "_",
                      f"{absolute_error}" if relative_error != float("inf") else "_",
                    ])

        # Check error
        if relative_error < max(error,1e-12) or absolute_error < max(error,1e-12)  :
            steps.append(f"Correct Digits = {correct_digits}")
            table_str = tabulate(table, headers=["Iteration", "Previous Root", "Root", "f(x)", "f'(x)", "f''(x)",
                                                 "Correct Digits", "Relative Error", "Absolute Error"], tablefmt="grid")
            return x_new, "\n".join(steps), table_str,i + 1, correct_digits, relative_error, absolute_error

        x = x_new
    
    raise ValueError(f"Modified Newton-Raphson method failed to solve this function with max iterations: {max_iterations}")

    
def main():

   x, steps, iterations, correct_digits, relative_error, absolute_error, table_str = modified_raphson("ln(x) - 1", 
                                                                                    initial_guess=0.9, significant_figures=12)
   
   print(x)
   print(steps)
   print(iterations)
   print(correct_digits)
   print(absolute_error)
   print(relative_error)
   print(table_str)
   
   
   
if __name__ == "__main__":
   main()
   
    