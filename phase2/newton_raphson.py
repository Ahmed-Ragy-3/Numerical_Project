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


def newton_raphson(functionString, initial_guess=0, max_iterations=50, error_tol=1e-5, 
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
   # rule: x[i + 1] = x[i] - (f(x[i]) / f'(x[i]))
   function = ProcessFunction(functionString)
   
   previous_root = None
   root = initial_guess
   
   table = []
   steps = []
   lines = []
   
   for i in range(max_iterations):
      steps.append(f"Iteration {i + 1}")
      previous_root = root
      f = function.evaluate(previous_root, significant_figures)
      steps.append(f"f({previous_root}) = {f}")
      
      f_dash = function.evaluate_first_derivative(previous_root, significant_figures)
      steps.append(f"f'({previous_root}) = {f_dash}")
      
      if round_significant(f_dash, significant_figures) == 0:
         raise ValueError("Newton Raphson cannot solve this method (f'(x) = 0)")
      
      root = round_significant(previous_root - (f / f_dash))
      
      # absolute relative error
      absolute_error = round_significant(abs(root - previous_root))
      steps.append(f"Absolute error = abs({root} - {previous_root}) = {absolute_error}")
      
      # approximate relative error
      if root != 0:
         relative_error = round_significant(absolute_error / abs(root))
         relative_error *= 100
         steps.append(f"Relative error = abs(({root} - {previous_root}) / {root}) * 100 % = {relative_error}%")
      
      correct_digits = 2 - log(2 * abs(relative_error))
      steps.append(f"Correct Digits Error = {correct_digits}")
      # steps.append(f"the number of correct significant digits = floor(2 - log10(2 * absolute_error)) = floor(2 - log10(2 * {absolute_error})) = {int(np.floor(2 - np.log10(2 * absolute_error)))}")
      
      steps.append("\n")
      # Check if relative error reached tolerance
      table.append(
         [
            i + 1,
            f"{previous_root}",
            f"{root}",
            f"{f}",
            f"{f_dash}",
            f"{absolute_error}" if relative_error != float("inf") else "_",
            f"{relative_error}%" if relative_error != float("inf") else "_"
         ]
      )
      
      if relative_error < error_tol:
         table_str = tabulate(table, headers=["Iteration", "Previous Root", "Root", "f(x)", "f'(x)",
                                              "Absolute Error", "Relative Error"], tablefmt="grid")
         
         return root, "\n".join(steps), table_str, i + 1, correct_digits, relative_error, absolute_error
      
      

   raise ValueError("Newton Rapshon method failed to solve this function")
      
      
def main():
   x, steps, iterations, correct_digits, relative_error, absolute_error, table_str = newton_raphson("x**2 + 2 * x + 1", 
                                                                                    initial_guess=13, significant_figures=6)
   
   print(x)
   print(steps)
   print(iterations)
   print(correct_digits)
   print(absolute_error)
   print(relative_error)
   print(table_str)
   
   
   
if __name__ == "__main__":
   main()
   
    