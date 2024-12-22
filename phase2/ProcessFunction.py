import sys
from sympy import symbols, sympify, diff, lambdify
import math
import numpy as np
from tabulate import tabulate
import plotly.graph_objects as go


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
      if value == 0:
         return 0
      else:
         return round(value, significant_figures - 1 - int(math.floor(math.log10(abs(value)))))

   def plot_function(self, low, high, lines):
      """
      Plots the interpolation lines and the function for False Position Method using Plotly.

      Parameters:
         lines (list): List of [low, fun_low, high, fun_high] at each iteration.
         low (float): The lower bound for plotting.
         high (float): The upper bound for plotting.
      """
      # Evaluate the function at x values
      func = self.evaluateFunction()
      x_vals = np.linspace(low, high, 2000)
      y_vals = func(x_vals)

      fig = go.Figure()

      # Plot the main function
      fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name="Function", line=dict(color='blue')))

      # Plot interpolation lines
      for line in lines:
         low_point, fun_low_point, high_point, fun_high_point = line
         fig.add_trace(go.Scatter(
            x=[low_point, high_point], 
            y=[fun_low_point, fun_high_point], 
            mode='lines', 
            name=f"Interpolation: {low_point} - {high_point}", 
            line=dict(width=3)
         ))

      # Add reference lines at x=0 and y=0
      fig.add_trace(go.Scatter(x=[low, high], y=[0, 0], mode='lines', name='y=0', line=dict(color='black', width=2)))
      fig.add_trace(go.Scatter(x=[0, 0], y=[min(y_vals), max(y_vals)], mode='lines', name='x=0', line=dict(color='black', width=1)))

      # Update layout
      fig.update_layout(
         title="False Position Method Interpolation Lines",
         xaxis_title="x",
         yaxis_title="f(x)",
         showlegend=True,
         plot_bgcolor='white',
         paper_bgcolor='white',
         xaxis=dict(showgrid=True, gridcolor='lightgray'),
         yaxis=dict(showgrid=True, gridcolor='lightgray'),
         font=dict(color='black')
      )

      fig.show()
