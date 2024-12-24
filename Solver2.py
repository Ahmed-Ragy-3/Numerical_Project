from ProcessFunction import ProcessFunction
from bracketing_method import bisection_method
from false_position_method import false_position_method
from newton_raphson import newton_raphson
from modified_raphson import modified_raphson
from fixed_point import fixed_point
from secant import secant
from sympy import SympifyError

class Solver:
   def __init__(self, functionString):
      try:
         self.function = ProcessFunction(functionString)
      except SympifyError as e:
         raise ValueError("Invalid function string.")
      
      self.approach = None
      self.initial_guess_1 = None
      self.initial_guess_2 = None
      self.significant_figures = 15
      self.max_iterations = 50
      self.tolerance = 1e-5
      
      
   def set_function(self, functionString):
      try:
         self.function = ProcessFunction(functionString)
      except SympifyError as e:
         self.function = None
         raise ValueError("Invalid function string.")
 
   def setApproach(self, approach: str) -> None:
      match approach:
         case "Bisection":
            self.approach = "Bisection"
         
         case "False-Position":
            self.approach = "False Position"
         
         case "Fixed-Point":
            self.approach = "Fixed Point"
         
         case "Original Newton-Raphson":
            self.approach = "Newton Raphson"
         
         case "Modifed Newton-Raphson":
            self.approach = "Modified Newton Rapshon"
         
         case "Secant":
            self.approach = "Secant"

         case _:
           raise ValueError("Invalid Method Name") 
          
   def set_initial_guess_1(self, initial_guess_1):
      self.initial_guess_1 = initial_guess_1

   def set_initial_guess_2(self, initial_guess_2):
      self.initial_guess_2 = initial_guess_2

   def set_significant_figures(self, significant_figures):
      if significant_figures <= 0:
         raise ValueError("Significant digits must be greater than 0.")
      self.significant_figures = significant_figures

   def set_max_iterations(self, max_iterations):
      if max_iterations <= 0:
         raise ValueError("Max iterations must be greater than 0.")
      self.max_iterations = max_iterations

   def set_tolerance(self, tolerance):
      if tolerance <= 0:
         raise ValueError("Error tolerance must be greater than 0.")
      self.tolerance = tolerance

   # the boundries needs to be changed 
   def plot(self):
      if self.function != None:
         self.function.plot_function(-10, 10, [], self.approach)

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
         match self.approach:
            case "Bisection": # root, steps, table, graph, iterations_done
               root, steps, table, graph, iterations_done = bisection_method(self.function, self.initial_guess_1, self. initial_guess_2, self.significant_figures, self.tolerance, self.max_iterations)
               graph.show()
               
            case "False Position": # root, steps, table, graph, iterations_done
               root, steps, table, graph, iterations_done = false_position_method(self.function, self.initial_guess_1, self. initial_guess_2, self.significant_figures, self.tolerance, self.max_iterations)
               graph.show()
               
            case "Fixed Point": # root, steps, table, iterations_done, correct_digits, relative_error, absolute_error
               root, steps, table, iterations_done, correct_digits, relative_error, absolute_error = fixed_point(self.function, self.initial_guess_1, self. max_iterations,self.tolerance, self.significant_figures)
            
            case "Newton Raphson": # root, steps, table , iterations_done, correct_digits, relative_error, absolute_error
               root, steps, table, iterations_done, correct_digits, relative_error, absolute_error = newton_raphson(self.function, self.initial_guess_1, self.max_iterations, self.tolerance, self.significant_figures)
            
            case "Modified Newton Rapshon": # root, steps, iterations_done, correct_digits, relative_error, absolute_error, table
               root, steps, iterations_done, correct_digits, relative_error, absolute_error, table = modified_raphson(self.function, self.initial_guess_1, self.max_iterations, self.tolerance, self.significant_figures)
            
            case "Secant": # root, steps, table iterations_done, correct_digits, relative_error, absolute_error
               root, steps, table, iterations_done, correct_digits, relative_error, absolute_error = secant(self.function, self.initial_guess_1, self.initial_guess_2,  self.max_iterations, self.tolerance, self.significant_figures)
      except SympifyError as e:
         raise ValueError(f"{e}.")

      solution = ""
      solution += f"Root: {root}\n"
      solution += f"Iterations: {iterations_done}\n"
      solution += f"Correct Digits: {correct_digits}\n"
      solution += f"Relative Error: {relative_error}\n"
      solution += f"Absolute Error: {absolute_error}\n"
      solution += f"{table}\n"
      solution += f"{steps}\n"

      return solution

if __name__ == "__main__":
   
   function_string = "x ^ 3 - x ^ 2 - 10 * x + 7"
   
   try:
      solver = Solver(function_string)

      solver.setApproach("Secant")
      solver.set_initial_guess_1(-3.5)
      solver.set_initial_guess_2(-3)
      solver.set_significant_figures(6)
      solver.set_max_iterations(10)
      solver.set_tolerance(1e-5)

      # solver.plot()

      solution = solver.solve()

      print(solution)
   except ValueError as e:
      error = f"An error occurred: {e}"
      print(error)
