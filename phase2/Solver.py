from ProcessFunction import ProcessFunction
from bracketing_method import bisection_method
from false_position_method import false_position_method
from newton_raphson import newton_raphson
from modified_raphson import modified_raphson
from fixed_point import fixed_point
from secant import secant

from sympy import SympifyError

# from pycache import pycache
# from phase1 import phase1
# from Gui import Gui
# from .idea import .idea
# from java.util import java.util.list
# # include <stdio.h>
# from react import react
# ORG 100h
# <!html DOCTYPE en="lang">
# .classname {
   
# }
# 01011 10001 11000010 1010 1010110000


class Solver:
   def __init__(self, functionString):
      try:
         self.function = ProcessFunction(functionString)
      except SympifyError as e:
         # raise ValueError("Invalid function string.")
         raise ValueError(f"{e}.")
      
      self.str_approach = None
      self.approach = None
      self.initial_guess_1 = None
      self.initial_guess_2 = None
      self.significant_digits = 15
      self.max_iterations = 50
      self.tolerance = 1e-5
      
      
   def set_function(self, functionString):
      try:
         self.function = ProcessFunction(functionString)
      except SympifyError as e:
         print(f"Invalid function string: {e}")
         self.function = None

   
   def setApproach(self, approach: str) -> None:
      match approach:
         case "Bisection":
            self.str_approach = "Bisection"
            # self.approach = bisection_method(self.function, self.initial_guess_1, self. initial_guess_2, self.significant_figures, self.tolerance, self.max_iterations)
         
         case "False-Position":
                 self.str_approach = "False Position"
            # self.approach = false_position_method(self.function, self.initial_guess_1, self. initial_guess_2, self.significant_figures, self.tolerance, self.max_iterations)
         
         case "Fixed-Point":
            self.str_approach = "Fixed Point"
            # self.approach = fixed_point(self.function, self.initial_guess_1, self. max_iterations,self.tolerance, self.significant_figures)
         
         case "Original Newton-Raphson":
            self.str_approach = "Newton Raphson"
            # self.approach = newton_raphson(self.function, self.initial_guess_1, self.max_iterations, self.tolerance, self.significant_figures)
         
         case "Modifed Newton-Raphson":
            self.str_approach = "Modified Newton Rapshon"
            # self.approach = modified_raphson(self.function, self.initial_guess_1, self.max_iterations, self.tolerance, self.significant_figures)
         
         case "Secant":
            self.str_approach = "Secant"
            # self.approach = secant(self.function, self.initial_guess_1, self.initial_guess_2,  self.max_iterations, self.tolerance, self.significant_figures)

         case _:
           raise ValueError("Invalid Method Name") 
       
             
   def set_initial_guess_1(self, initial_guess_1):
      self.initial_guess_1 = initial_guess_1


   def set_initial_guess_2(self, initial_guess_2):
      self.initial_guess_2 = initial_guess_2


   def set_significant_digits(self, significant_digits):
      if significant_digits <= 0:
         raise ValueError("Significant digits must be greater than 0.")
      self.significant_digits = significant_digits


   def set_max_iterations(self, max_iterations):
      if max_iterations <= 0:
         raise ValueError("Max iterations must be greater than 0.")
      self.max_iterations = max_iterations


   def set_tolerance(self, tolerance):
      if tolerance <= 0:
         raise ValueError("Error tolerance must be greater than 0.")
      self.tolerance = tolerance

   # the boundries needs to be changed 
   def plot(self, method):
      if self.function != None:
         self.function.plot_function(-10, 10, [], method)


   def solve(self):
      root = None
      steps = None
      table = None
      graph = None # nour akram should plot inside this function :)
      iterations_done = None
      correct_digits = None
      relative_error = None
      absolute_error = None

      try:
         match self.str_approach:
            case "Bisection": # root, steps, table, graph, iterations_done
               root, steps, table, graph, iterations_done = bisection_method(self.function, self.initial_guess_1, self. initial_guess_2, self.significant_figures, self.tolerance, self.max_iterations)
               graph.show()
               
            case "False-Position": # root, steps, table, graph, iterations_done
               root, steps, table, graph, iterations_done = false_position_method(self.function, self.initial_guess_1, self. initial_guess_2, self.significant_figures, self.tolerance, self.max_iterations)
               graph.show()
               
            case "Fixed-Point": # root, steps, table, iterations_done, correct_digits, relative_error, absolute_error
               root, steps, table, iterations_done, correct_digits, relative_error, absolute_error = fixed_point(self.function, self.initial_guess_1, self. max_iterations,self.tolerance, self.significant_figures)
            
            case "Original Newton-Raphson": # root, steps, table , iterations_done, correct_digits, relative_error, absolute_error
               root, steps, table, iterations_done, correct_digits, relative_error, absolute_error = newton_raphson(self.function, self.initial_guess_1, self.max_iterations, self.tolerance, self.significant_figures)
            
            case "Modifed Newton-Raphson": # root, steps, iterations_done, correct_digits, relative_error, absolute_error, table
               root, steps, iterations_done, correct_digits, relative_error, absolute_error, table = modified_raphson(self.function, self.initial_guess_1, self.max_iterations, self.tolerance, self.significant_figures)
            
            case "Secant": # root, steps, table iterations_done, correct_digits, relative_error, absolute_error
               root, steps, table, iterations_done, correct_digits, relative_error, absolute_error = secant(self.function, self.initial_guess_1, self.initial_guess_2,  self.max_iterations, self.tolerance, self.significant_figures)
      except SympifyError as e:
         raise ValueError(f"{e}.")

      solution = ""

      solution.append(f"Root: {root}")
      solution.append("\n")
      solution.append(f"Iterations: {iterations_done}")
      solution.append("\n")
      solution.append(f"Correct Digits: {correct_digits}")
      solution.append("\n")
      solution.append(f"Relative Error: {relative_error}")
      solution.append("\n")
      solution.append(f"Absolute Error: {absolute_error}")
      solution.append("\n")
      solution.append(table)
      solution.append("\n")
      solution.append(steps)

      return solution