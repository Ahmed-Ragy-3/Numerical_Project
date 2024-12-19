import sys
from sympy import symbols, sympify, diff, lambdify
import math

class ProcessFunction:
   def __init__(self, inputString):
      self.x = symbols('x')
      self.f_symbolic = sympify(inputString)
      self.f_prime_symbolic = diff(self.f_symbolic, self.x)  # First derivative
      self.f_double_prime_symbolic = diff(self.f_prime_symbolic, self.x)  # Second derivative

   def evaluateFunction(self):
      return lambdify(self.x, self.f_symbolic)

   def getFirstDif(self):
      return lambdify(self.x, self.f_prime_symbolic)

   def getSecondDir(self):
      return lambdify(self.x, self.f_double_prime_symbolic)

   def evaluate(self, value, significant_figures=sys.float_info.dig):
      func = self.evaluateFunction()
      result = func(value)
      return self.round_significant(result, significant_figures)

   def evaluate_first_derivative(self, value, significant_figures=sys.float_info.dig):
      func = self.getFirstDif()
      result = func(value)
      return self.round_significant(result, significant_figures)

   def evaluate_second_derivative(self, value, significant_figures=sys.float_info.dig):
      func = self.getSecondDir()
      result = func(value)
      return self.round_significant(result, significant_figures)

   @staticmethod
   def round_significant(value, significant_figures=sys.float_info.dig):
      print(significant_figures)
      if value == 0:
         return 0
      else:
         return round(value, significant_figures - 1 - int(math.floor(math.log10(abs(value)))))

# def main():
#    # Create an instance of ProcessFunction
#    func = ProcessFunction("x**2 + 2*x + 1")
   
#    # Evaluate function and derivatives
#    x_value = 2
#    significant_figures = 5

#    func_value = func.evaluate(x_value, significant_figures)
#    first_derivative = func.evaluate_first_derivative(x_value, significant_figures)
#    second_derivative = func.evaluate_second_derivative(x_value, significant_figures)

#    # Print results
#    print(f"f({x_value}) = {func_value}")
#    print(f"f'({x_value}) = {first_derivative}")
#    print(f"f''({x_value}) = {second_derivative}")

# if __name__ == "__main__":
#    main()
