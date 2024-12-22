from ProcessFunction import ProcessFunction
from math import log,floor
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



def modified_raphson(inputString, initial_guess, max_iterations=50, 
                     error=1e-5, significant_figures=sys.float_info.dig):

   pf = ProcessFunction(inputString)
   x = initial_guess
   steps = []
   table= []
   for i in range(max_iterations):  
      steps.append("\n")
      steps.append(f"Iteration {i + 1}")
      
      f = pf.evaluate(x, significant_figures)
      steps.append(f"f({x}) = {f}")
      
      f_dash = pf.evaluate_first_derivative(x, significant_figures)
      steps.append(f"f'({x}) = {f_dash}")
      
      f_double_dash = pf.evaluate_second_derivative(x, significant_figures)
      steps.append(f"f''({x}) = {f_double_dash}")

  
      # to avoid division by zero
      denominator = round_significant(abs(f_dash ** 2 - f * f_double_dash), significant_figures)
      if denominator == 0:
         raise ValueError(f"Avoid division by zero ,at iteration {i + 1}")
      
      x_new = round_significant(x - ((f * f_dash) / denominator), significant_figures)

    
      # absolute relative error
      absolute_error = round_significant(abs(x_new - x), significant_figures)
      steps.append(f"Absolute error = abs({x} - {x_new}) = {absolute_error}")

      if x_new != 0:
         # relative_error = round_significant(absolute_error, significant_figures) * 100
         relative_error = round_significant(abs(x_new) - abs(x), significant_figures) * 100
         steps.append(f"Relative error = abs(({x_new} - {x}) / {x_new}) * 100 % = {relative_error}%")
      
      steps.append("\n")
      table.append([i + 1,
            f"{x}",
            f"{x_new}",
            f"{f}",
            f"{f_dash}",
            f"{f_double_dash}",
            f"{relative_error}%" if relative_error != float("inf") else "_",
            f"{absolute_error}" if relative_error != float("inf") else "_",
      ])
      
      #check error
      if relative_error < error:
         correct_digits = floor(2 - log(2 * abs(relative_error)))
         steps.append(f"Correct Digits Error = {correct_digits}")
         
         table_str = tabulate(table, headers=["Iteration", "Previous Root", "Root", "f(x)", "f'(x)","f''(x)"
                                              "Absolute Error", "Relative Error"], tablefmt="grid")
         
         return x, "\n".join(steps), i + 1, correct_digits, relative_error, absolute_error, table_str
      
      x = x_new
      
     
   raise ValueError("Modified Newton Rapshon method failed to solve this function with max iterations : {max_iteration} ")



    
def main():
   x, steps, iterations, correct_digits, relative_error, absolute_error, table_str = modified_raphson("x**2 + 2 * x + 1", 
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
   
    