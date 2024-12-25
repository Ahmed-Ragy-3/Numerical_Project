from ProcessFunction import ProcessFunction
from bracketing_method import bisection_method
from false_position_method import false_position_method
from newton_raphson import newton_raphson
from modified_raphson import modified_raphson
from fixed_point import fixed_point
from secant import secant
from sympy import SympifyError

# names = {
#    "raphson" : "Original Newton-Raphson",
#    "modified_raphson" : "Original Newton-Raphson",
#    "raphson" : "Original Newton-Raphson",
#    "raphson" : "Original Newton-Raphson",
#    "raphson" : "Original Newton-Raphson",
#    "raphson" : "Original Newton-Raphson",
# }

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
      if tolerance <= 0:
         raise ValueError("Error tolerance must be greater than 0.")
      self.tolerance = tolerance

   # the boundaries need to be changed
   def plot(self, low=-10, high=10, lines=[]):
      if self.function != None:
         self.function.plot_function(low, high, lines)
   
   def plot_solution(self, low, high, lines):
      self.plot(low, high, lines)
      

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
      graph = None
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
         
         match self.approach:
            case "Bisection":
               answer, lines = bisection_method(*params, self.initial_guess_1, self.initial_guess_2)
               print("--------------------------")
            case "False Position":
               answer, lines = false_position_method(*params, self.initial_guess_1, self.initial_guess_2)
               
            case "Fixed Point":
               answer, lines = fixed_point(*params, self.initial_guess_1)
            
            case "Newton Raphson":
               answer, lines = newton_raphson(*params, self.initial_guess_1)
            
            case "Modified Newton Raphson":
               answer = modified_raphson(*params, self.initial_guess_1)
            
            case "Secant":
               answer = secant(*params, self.initial_guess_1, self.initial_guess_2)

         root, steps, table, iterations_done, correct_digits, relative_error, absolute_error = answer
         # root, "\n".join(steps), "\n" + table_str, i + 1, correct_digits, relative_error, absolute_error, lines

         solution = ""
         solution += f"Root: {root}\n"
         solution += f"Iterations: {iterations_done}\n"
         solution += f"Correct Digits: {correct_digits}\n"
         solution += f"Relative Error: {relative_error}\n"
         solution += f"Absolute Error: {absolute_error}\n"
         solution += f"{table}\n"
         solution += f"{steps}\n"

         # print(steps)
         # return solution
         
         return solution, lines

      except SympifyError as e:
         raise ValueError(f"error 1{e}.")
      
      # except ValueError as e:
      #    raise ValueError(f"{e}.")

if __name__ == "__main__":
   
   function_string = "x^4 - 1"
   
   try:
      solver = Solver(function_string)

      # solver.plot(-10, 10)

      solver.set_approach("Bisection")
      # solver.set_approach("False Position")
      # solver.set_approach("Fixed Point")
      # solver.set_approach('Newton Raphson')
      # solver.set_approach('Modified Newton Raphson')
      # solver.set_approach("Secant")
      
      solver.set_initial_guess_1(0)
      solver.set_initial_guess_2(2)
      solver.set_significant_figures(5)
      solver.set_max_iterations(50)
      solver.set_tolerance(1e-5)
      
      solution, lines = solver.solve()
      solver.plot_solution(-10, 10, lines)

      print(solution)
   except Exception as e:
      print(f"An error occurred: {e}")
   # except ValueError as e:
   #    error = f"An error occurred: {e}"
   #    print(error)
   # except TypeError as e:
   #    error = f"An error occurred: {e}"
   #    print(error)
      
   