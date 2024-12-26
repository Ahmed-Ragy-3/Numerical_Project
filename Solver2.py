from ProcessFunction import ProcessFunction
from bracketing_method import bisection_method
from false_position_method import false_position_method
from newton_raphson import newton_raphson
from modified_raphson import modified_raphson
from fixed_point import fixed_point
from secant import secant
from sympy import SympifyError
import time

names = {
   "raphson" : "Original Newton-Raphson",
   "modified_raphson" : "Original Newton-Raphson",
   "raphson" : "Original Newton-Raphson",
   "raphson" : "Original Newton-Raphson",
   "raphson" : "Original Newton-Raphson",
   "raphson" : "Original Newton-Raphson",
}

class Solver:
   def __init__(self):

      self.function = None
      self.approach = None
      self.initial_guess_1 = None
      self.initial_guess_2 = None
      self.significant_figures = 15
      self.max_iterations = 50
      self.tolerance = 1e-5
      self.lines = None
      
   def set_function(self, functionString):
      try:
         self.function = ProcessFunction(functionString)
      except SympifyError as e:
         self.function = None
         raise ValueError(f"Invalid function string. {e}")
 
   def set_approach(self, approach: str) -> None:
      self.approach = approach
          
   def set_initial_guess_1(self, initial_guess_1):
      if initial_guess_1 != "":
         self.initial_guess_1 = initial_guess_1
      else:
         raise ValueError("Invalid initial guess 1")

   def set_initial_guess_2(self, initial_guess_2):
      if initial_guess_2 != "":
         self.initial_guess_2 = initial_guess_2
      else:
         raise ValueError("Invalid initial guess 2")

   def set_significant_figures(self, significant_figures):
      if significant_figures <= 0:
         raise ValueError("Significant digits must be greater than 0.")
      self.significant_figures = significant_figures

   def set_max_iterations(self, max_iterations):
      if max_iterations <= 0:
         raise ValueError("Max iterations must be greater than 0.")
      self.max_iterations = max_iterations

   def set_tolerance(self, tolerance):
      if tolerance < 0:
         raise ValueError("Error tolerance must be greater than 0.")
      self.tolerance = tolerance

   # the boundaries need to be changed
   def plot(self, low=-10, high=10):
      if self.function is not None:
         if(self.approach == "Fixed-Point"):
            liness = []
            liness.append([-1000, -1000, 1000, 1000])
            self.function.plot_function(low, high, liness)
         else:
            self.function.plot_function(low, high, [])


   
   def plot_solution(self, low=-10, high=10):
      if self.lines == None:
         return
      self.function.plot_function(low, high, self.lines)
      

   def solve(self):
      # delete me
      # print(self.approach)
      # print(type(self.approach))
      # print(self.initial_guess_1)
      # print(type(self.initial_guess_1))
      # print(self.initial_guess_2)
      # print(type(self.initial_guess_2))
      # print(self.max_iterations)
      # print(type(self.max_iterations))
      # print(self.significant_figures)
      # print(type(self.significant_figures))
      # print(self.tolerance)
      # print(type(self.tolerance))

      root = None
      steps = None
      table = None
      iterations_done = None
      correct_digits = None
      relative_error = None
      absolute_error = None

      try:
         # All methods has root, steps, table, iterations_done, correct_digits, relative_error, absolute_error
         # tuple contains common returned elements for all methods
         answer = tuple()
         
         # tuple contains the common parameters of the all approaches
         params = (self.function, self.max_iterations, self.tolerance, self.significant_figures)
         
         start_time = time.perf_counter()
         
         match self.approach:
            case "Bisection":
               answer, lines = bisection_method(*params, self.initial_guess_1, self.initial_guess_2)
               self.lines = lines
            case "False-Position":
               answer, lines = false_position_method(*params, self.initial_guess_1, self.initial_guess_2)
               self.lines = lines
            case "Fixed-Point":
               answer, lines = fixed_point(*params, self.initial_guess_1)
               self.lines = lines
            
            case "Original Newton-Raphson":
               answer, lines = newton_raphson(*params, self.initial_guess_1)
               self.lines = lines
            
            case "Modified Newton-Raphson":
               answer = modified_raphson(*params, self.initial_guess_1)
            
            case "Secant":
               answer, lines = secant(*params, self.initial_guess_1, self.initial_guess_2)
               self.lines = lines

         root, steps, table, iterations_done, correct_digits, relative_error, absolute_error = answer

         end_time = time.perf_counter()

         solution = ""
         solution+= self.approach+"\n"
         solution += f"Root: {root}\n"
         solution += f"Iterations: {iterations_done}\n"
         solution += f"Correct Digits: {correct_digits}\n"
         solution += f"Relative Error: {relative_error}\n"
         solution += f"Absolute Error: {absolute_error}\n"
         solution += f"Time taken: {(end_time - start_time) * 1000:.8f} ms\n"
         solution += f"{table}\n"
         solution += f"{steps}\n\n"

         # print(steps)
         # return solution
         
         return solution

      except SympifyError as e:
         raise ValueError(f"{e}.")
      
      # except ValueError as e:
      #    raise ValueError(f"{e}.")


test_cases = [
   "x^3- 5*x^2+3*x-1",
   "exp(-x) -x",
   "x^2",
   "x^4+3*x-4",
   "(x^2-3)/2",
   "(x-1)^3 +0.512",
   "sin(x)"
]


if __name__ == "__main__":
   
   # function_string = test_cases[2]
   # function_string = "sqrt((1.7*x+2.5) / 0.9)"

   try:
      solver = Solver()

      # solver.set_function(test_cases[2])
      solver.set_function("x^2 - 1")

      solver.plot(-10, 10)

      solver.set_approach("False-Position")
      # solver.set_approach("False-Position")

      # solver.set_approach("Fixed-Point")
      solver.set_approach("Original Newton-Raphson")
      # solver.set_approach("Modified Newton-Raphson")
      # solver.set_approach("Secant")
      
      solver.set_initial_guess_1(0)
      solver.set_initial_guess_2(1.5)
      solver.set_significant_figures(5)
      solver.set_max_iterations(50)
      solver.set_tolerance(1e-5)
      
      solution = solver.solve()

      solver.plot_solution(-10, 10)

      print(solution)
   except ValueError as e:
      print(f"An error occurred: {e}")
      
   # except ValueError as e:
   #    error = f"An error occurred: {e}"
   #    print(error)
   # except TypeError as e:
   #    error = f"An error occurred: {e}"
   #    print(error)