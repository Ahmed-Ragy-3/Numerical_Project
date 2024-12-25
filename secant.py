import math
# from colorama import Fore, Style, init

import sys
from math import log
import numpy as np
from ProcessFunction import ProcessFunction
from false_position_method import round_significant
from tabulate import tabulate

EPSILON = 1e-15

def round_significant(value, significant_figures=sys.float_info.dig):
   """
   Rounds the given value to the specified number of significant figures.
   
   :param value: The float number to round.
   :param significant_figures: The number of significant figures to retain.
   :return: The rounded value.
   """
   # print("value = ",value)
   try:
      if value == 0:
         return 0
      
      if math.isinf(value):
         return float('inf')
      
      decimal_places = significant_figures - 1 - int(math.floor(math.log10(abs(value))))
      return round(value, decimal_places)
   except (ValueError, OverflowError) as e:
      raise ValueError("Error occurred during rounding calculation.") from e

# def round_significant(value, sig_figs=sys.float_info.dig):
#    if value == 0:
#       return 0
#    elif value == float('inf') or value == -float('inf'):
#       return float('inf')
#    else:
#       return round(value, sig_figs - int(np.floor(np.log10(abs(value)))) - 1)


# self.function, self.max_iterations, self.tolerance, self.significant_figures, initialguess1
def secant(function: ProcessFunction, max_iterations=50, error_tol=1e-5, 
         significant_figures=sys.float_info.dig, X0=0, X1=0):
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
   # init()
   #                          ( f(x[i]) * (x[i-1] - x[i]) )
   # rule: x[i + 1] = x[i] -  ----------------------------  
   #                            ( f(x[i-1]) - f(x[i]) )   
         
   # function = ProcessFunction(functionString)
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
         raise ValueError("Division by zero in the formula !")

      following_root = current_root - (numerator / denominator)
      following_root = round_significant(following_root, significant_figures)

      f_xi_plus_1 = function.evaluate(following_root, significant_figures)

      lines.append([previous_root, f_xi_minus_1, following_root, f_xi_plus_1])

      absolute_error = abs(following_root - current_root)
      absolute_error = round_significant(absolute_error, significant_figures)
      
      if following_root == 0:
         raise ValueError("Division by zero on calculating the relative error !")

      relative_error = abs((following_root - current_root) / following_root) * 100
      relative_error = round_significant(relative_error, significant_figures)

      if relative_error <= 0:
         correct_digits = significant_figures
      else:
         correct_digits = math.floor(2 - math.log10(2 * relative_error / 100))
         correct_digits = max(correct_digits, 0)
      
      steps.append(f"x[i-1] = {previous_root}, x[i] = {current_root}")
      steps.append(f"f(x[i-1]) = {f_xi_minus_1}, f(x[i]) = {f_xi}")
      steps.append(f"x[i+1] = {following_root}")
      steps.append(f"Absolute Error = {absolute_error}")
      steps.append(f"Relative Error = {relative_error}%")
      steps.append(f"Correct Digits = {correct_digits}")
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

      # if relative_error < error_tol or absolute_error < EPSILON:
      if relative_error < error_tol or absolute_error < EPSILON or f_xi_plus_1 == 0:
         table_str = tabulate(
            table,
            headers=["Iteration", "xᵢ₋₁", "xᵢ", "f(xᵢ₋₁)", "f(xᵢ)", "xᵢ₊₁", "Absolute Error", "Relative Error"],
            tablefmt="grid"
         )
         #function.plot_function(-10, 10, lines, method="Secant")
         return current_root, "\n".join(steps), table_str, i + 1, correct_digits, relative_error, absolute_error
         #root, steps, table, iterations_done, correct_digits, relative_error, absolute_error

   raise ValueError("Secant Method failed to converge within the maximum number of iterations.")
      
      
def main():
   root, steps, table_str, iterations, correct_digits, relative_error, absolute_error = secant(
      ProcessFunction("x ^ 3 - x ^ 2 - 10 * x + 7"),
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

