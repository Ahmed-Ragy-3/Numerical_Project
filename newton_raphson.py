from colorama import Fore, Style, init

import sys
from math import log
import numpy as np
from ProcessFunction import ProcessFunction
from false_position_method import round_significant
from tabulate import tabulate

EPSILON = 1e-15
# EPSILON = sys.f

def round_significant(value, sig_figs=sys.float_info.dig):
   if value == 0:
      return 0
   elif value == float('inf') or value == -float('inf'):
      return float('inf')
   else:
      return round(value, sig_figs - int(np.floor(np.log10(abs(value)))) - 1)


def newton_raphson(function: ProcessFunction, initial_guess=0, max_iterations=50, error_tol=1e-5, 
                  significant_figures=sys.float_info.dig):
   """
   Parameters:
      function (callable): The function for which to find the root.
      initial guess (float): xi.
      significant_figures (int, optional): Number of significant figures for rounding.
      error (float): Error threshold for stopping the iterations.
      max_iterations (int): Maximum number of iterations.

   Returns:
      root:  float
      steps: str
      table: str
      graph: plotly graph object
      iterations done: int
      number of correct significant figures
      approximate relative error: float
   """
   init()
   
   previous_root = None
   root = initial_guess
   i = 0
   table = []
   steps = []
   lines = []
   
   relative_error = float('inf')
   table_str = ""
   correct_digits = 0
   
   def end():
      """
      function that returns all the computed data
      """   
      table_str = tabulate(table, headers=["Iteration", "Previous Root", "Root", "f(x)", "f'(x)",
                                          "Absolute Error", "Relative Error"], tablefmt="grid")
      
      function.plot_function(-3, 3, lines, method="Newton Raphson")
      return root, "\n".join(steps), "\n" + table_str, i + 1, correct_digits, relative_error, absolute_error 
   
   # rule: x[i + 1] = x[i] - (f(x[i]) / f'(x[i]))
   # function = ProcessFunction(functionString)
   
   # i = 0
   for i in range(max_iterations):
      # print(root)
      steps.append(f"Iteration {i + 1}")
      previous_root = root
      
      print("prev = ", previous_root)
      # check if there is an inflection point
      if function.evaluate_second_derivative(previous_root, significant_figures) == 0:
         return end()
         # raise ValueError("Inflection Point Detection")
      
      # evaluate function f(x)
      f = function.evaluate(previous_root, significant_figures)
      steps.append(f"f({round_significant(previous_root, significant_figures)}) = {f}")
      
      # evaluate derivative of function f'(previous root)
      f_dash = function.evaluate_first_derivative(previous_root, significant_figures)
      steps.append(f"f'({previous_root}) = {f_dash}")
   
      # check if f'(x) = 0, 
      if f_dash == 0:
         return end()
         # raise ValueError("Newton Raphson cannot solve this method (f'(x) = 0)")
      
      # Vertical line from (previous_root, 0) to (previous_root, f(previous_root))
      lines.append([root, 0, previous_root, function.evaluate(previous_root)])

      # Compute new root 
      root = round_significant(previous_root - (f / f_dash), significant_figures)
      
      # f_dash = slope = (y2 - y1) / (x2 - x1)
      # Add lines for graph plotting
      # tangent line
      lines.append([previous_root, function.evaluate(previous_root), root, 0])

      
      # Calculate absolute error
      absolute_error = round_significant(abs(root - previous_root), significant_figures)
      steps.append(f"Absolute error = abs({root} - {previous_root}) = {absolute_error}")
      
      # print(absolute_error)
      if absolute_error < error_tol:
         return end()
      
      # print(f"root = {root}, prev = {previous_root}")
      # Calculate approximate relative error
      relative_error = abs(1 - round_significant(abs(previous_root / root), significant_figures))
      relative_error *= 100
      relative_error = round_significant(relative_error, significant_figures)
      steps.append(f"Relative error = abs(({root} - {previous_root}) / {root}) * 100 % = {relative_error}%")
      
      # Check if relative error reached tolerance
      if relative_error < error_tol:
         return end()
      
      # Calculate correct significant digits for root 
      correct_digits = 2 - log(2 * abs(relative_error))
      steps.append(f"{'No Correct Digits' if correct_digits <= 0 else f'Number of Correct Significant Digits = {int(correct_digits)}'}")
      # steps.append(f"the number of correct significant digits = floor(2 - log10(2 * absolute_error)) = 
      # floor(2 - log10(2 * {absolute_error})) = {int(np.floor(2 - np.log10(2 * absolute_error)))}")
      
      steps.append("\n")
      
      table.append(
         [
            i + 1,
            f"{Fore.BLUE}{previous_root}{Style.RESET_ALL}",
            f"{Fore.GREEN}{root}{Style.RESET_ALL}",
            f"{Fore.RED}{f}{Style.RESET_ALL}",
            f"{Fore.YELLOW}{f_dash}{Style.RESET_ALL}",
            f"{Fore.CYAN}{absolute_error}{Style.RESET_ALL}" if relative_error != float("inf") else "_",
            f"{Fore.MAGENTA}{relative_error}%{Style.RESET_ALL}" if relative_error != float("inf") else "_"
         ]
      )
   
      # print(f"root = {root}, relative error = ", relative_error)
   
   raise ValueError("Newton Rapshon method failed to solve this function")
      
      
def main():
   function = ProcessFunction("sqrt((1.7 * x + 2.5) / 0.9)")
   x, steps, iterations, correct_digits, relative_error, absolute_error, table_str = newton_raphson(function, 
                                                                                     initial_guess=0.8, significant_figures=10)
   
   print(x)
   print(steps)
   print(iterations)
   print(correct_digits)
   print(absolute_error)
   print(relative_error)
   print(table_str)
   
   
   
if __name__ == "__main__":
   main()
   
    