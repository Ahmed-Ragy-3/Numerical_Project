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
      # print(self.f_double_prime_symbolic.__str__())

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
      
   def plot_function(self, low, high, lines, method="Function"):
      """
      Plots the graph using Plotly.

      Parameters:
         lines (list): List of [low, fun_low, high, fun_high] at each iteration.
         low (float): The lower bound for plotting.
         high (float): The upper bound for plotting.
      """
      print(low)
      print(high)
      print(lines)
      print(method)
      # Evaluate the function at x values
      func = self.evaluateFunction()
      x_vals = np.linspace(low, high, 2000)
      # x_vals = np.linspace(low, high, 20)
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
            line=dict(width=2)
         ))

      # Add reference lines at x=0 and y=0
      fig.add_trace(go.Scatter(x=[low, high], y=[0, 0], mode='lines', name='y=0', line=dict(color='black', width=2)))
      fig.add_trace(go.Scatter(x=[0, 0], y=[min(y_vals), max(y_vals)], mode='lines', name='x=0', line=dict(color='black', width=1)))

      # Adjust the range for better zooming
      # y_range1 = [min(y_vals) - abs(min(y_vals)) * 0.1, max(y_vals) + abs(max(y_vals)) * 0.1]  # Add some padding
      # x_range1 = [low - abs(low) * 0.1, high + abs(high) * 0.1]
      FACTOR = 2 / 3
      x_range1 = [low * FACTOR , high * FACTOR]

      # print(x_range1)
      # print(y_range1)

      # x_range1 = 10
      y_range1 = x_range1

      # Update layout
      fig.update_layout(
         title=f"{method}",
         xaxis_title="x",
         yaxis_title="f(x)",
         showlegend=True,
         plot_bgcolor='white',
         paper_bgcolor='white',
         # xaxis=dict(showgrid=True, gridcolor='lightgray'),
         # yaxis=dict(scaleanchor="x", showgrid=True, gridcolor='lightgray'),
         xaxis=dict(showgrid=True, gridcolor='lightgray', range=x_range1),
         yaxis=dict(scaleanchor="x", showgrid=True, gridcolor='lightgray', range=y_range1),
         font=dict(color='black')
      )

      fig.show()
