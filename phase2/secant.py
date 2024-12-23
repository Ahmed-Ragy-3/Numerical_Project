import math
from colorama import Fore, Style, init

import sys
from math import log
import numpy as np
from ProcessFunction import ProcessFunction
from false_position_method import round_significant
from tabulate import tabulate

EPSILON = 1e-15

def round_significant(value, sig_figs=sys.float_info.dig):
   if value == 0:
      return 0
   elif value == float('inf') or value == -float('inf'):
      return float('inf')
   else:
      return round(value, sig_figs - int(np.floor(np.log10(abs(value)))) - 1)


def secant(functionString, X0=0, X1=0,  max_iterations=50, error_tol=1e-5, 
                  significant_figures=sys.float_info.dig):
   """
   Parameters:
      functionString (str): The function for which to find the root.
      X0 (float): Initial guess x[i-1].
      X1 (float): Initial guess x[i].
      significant_figures (int, optional): Number of significant figures for rounding.
      error_tol (float): Error threshold for stopping the iterations.
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
   #                          ( f(x[i]) * (x[i-1] - x[i]) )
   # rule: x[i + 1] = x[i] -  ----------------------------  
   #                            ( f(x[i-1]) - f(x[i]) )   
         
   function = ProcessFunction(functionString)
   previous_root = X0
   current_root = X1
   following_root = 0
   
   table = []
   steps = []
   lines = []
   relative_error = float('inf')
   table_str = ""
   correct_digits = 0
   
   for i in range(max_iterations):
      steps.append(f"Iteration {i + 1}")

      f_xi = function.evaluate(current_root, significant_figures)
      f_xi_minus_1 = function.evaluate(previous_root, significant_figures)

      numerator = f_xi * (previous_root - current_root)
      numerator = round_significant(numerator, significant_figures)
      denominator = f_xi_minus_1 - f_xi
      denominator = round_significant(denominator, significant_figures)

      if denominator == 0:
         raise ValueError("Division by zero in the formula!")

      following_root = current_root - (numerator / denominator)
      following_root = round_significant(following_root, significant_figures)

      absolute_error = abs(following_root - current_root)
      absolute_error = round_significant(absolute_error, significant_figures)

      relative_error = abs((following_root - current_root) / following_root) * 100
      relative_error = round_significant(relative_error, significant_figures)

      # correct_digits = math.floor(2 - log(2 * abs(relative_error), 10))
      
      steps.append(f"x[i-1] = {previous_root}, x[i] = {current_root}")
      steps.append(f"f(x[i-1]) = {f_xi_minus_1}, f(x[i]) = {f_xi}")
      steps.append(f"x[i+1] = {following_root}")
      steps.append(f"Absolute Error = {absolute_error}")
      steps.append(f"Relative Error = {relative_error}%")
      steps.append(f"Correct Digits = {correct_digits}")
      # steps.append(f"Correct Digits Error = {correct_digits}")
      steps.append("\n")

      
      table.append([
            i + 1,
            round_significant(previous_root, significant_figures),
            round_significant(current_root, significant_figures),
            round_significant(f_xi_minus_1, significant_figures),
            round_significant(f_xi, significant_figures),
            round_significant(following_root, significant_figures),
            round_significant(absolute_error, significant_figures),
            round_significant(relative_error, significant_figures)
        ])
      
      previous_root = current_root
      current_root = following_root

      if relative_error < error_tol or absolute_error < EPSILON:
         table_str = tabulate(
               table,
               headers=["Iteration", "x[i-1]", "x[i]", "f(x[i-1])", "f(x[i])", "x[i+1]", "Abs Error", "Rel Error"],
               tablefmt="grid"
         )
         function.plot_function(-10, 10, lines)
         return current_root, "\n".join(steps), table_str, i + 1, correct_digits, relative_error, absolute_error

   raise ValueError("Secant Method failed to converge within the maximum number of iterations.")
      
      
def main():
   root, steps, table_str, iterations, correct_digits, relative_error, absolute_error = secant(
      " x ^ 3 - x ^ 2 - 10 * x + 7",
      X0=-3.5,
      X1=-3,
      max_iterations=10,
      significant_figures=6
   )

   print(steps)
   print(table_str)
   print(f"Root: {root}")
   print(f"Iterations: {iterations}")
   print(f"Correct Digits: {correct_digits}")
   print(f"Relative Error: {relative_error}")
   print(f"Absolute Error: {absolute_error}")

if __name__ == "__main__":
   main()

    