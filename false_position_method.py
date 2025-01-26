import sys
import numpy as np
from tabulate import tabulate
import plotly.graph_objects as go
from ProcessFunction import ProcessFunction


def round_significant(value, sig_figs):
    if value == 0:
        return 0
    elif value == float('inf') or value == -float('inf'):
        return float('inf')
    else:
        return round(value, sig_figs - int(np.floor(np.log10(abs(value)))) - 1)

# self.function, self.max_iterations, self.tolerance, self.significant_figures, initialguess1
def false_position_method(function: ProcessFunction, max_iterations=50, error=0.00001, significant_figures=sys.float_info.dig,
                     low=-10.0, high=10.0):
    """
    Parameters:
        function (callable): The function for which to find the root.
        low (float): Lower bound.
        high (float): Upper bound.
        significant_figures (int, optional): Number of significant figures for rounding.
        error (float): Error threshold for stopping the iterations.
        max_iterations (int): Maximum number of iterations.

    Returns:
        root: float, steps: str, table: str, lines: array[line]
    """
    
    min_low = low
    max_high = high
    previous_root = None
    table = []
    steps = []
    lines = []

    low = round_significant(low, significant_figures)
    high = round_significant(high, significant_figures)
    fun_low = round_significant(function.evaluate(low), significant_figures)
    fun_high = round_significant(function.evaluate(high), significant_figures)

    steps.append("Check if the function changes sign between low and high:")
    steps.append(f"function(low) * function(high) = function({low}) * function({high}) = {fun_low} * {fun_high}")

    if fun_low * fun_high > 0:
        steps.append("Which is greater than 0. Can't be solved: no bracketing found.")
        raise ValueError(f"It can't be solved by false position method, there f({low}) * f({high}) > 0")

    steps.append("Which is less than 0. So there is at least one root between the bounds.")
    correct_digits = 0
    for iteration in range(1, max_iterations + 1):
        low = round_significant(low, significant_figures)
        high = round_significant(high, significant_figures)
        fun_low = round_significant(function.evaluate(low), significant_figures)
        fun_high = round_significant(function.evaluate(high), significant_figures)
        lines.append([low, fun_low, high, fun_high])

        steps.append(f"\nIteration {iteration}:\n")
        steps.append(f"low = {low}, high = {high}")
        root = round_significant((low * fun_high - high * fun_low) / (fun_high - fun_low), significant_figures)
        steps.append(f"Estimated root = (low * fun(high) - high * fun(low)) / (fun(high) - fun(low)) = ({low} * {fun_high} - {high} * {fun_low}) / ({fun_high} - {fun_low}) = {root}")
        fun_root = round_significant(function.evaluate(root), significant_figures)
        steps.append(f"function(estimated_root) = function({root}) = {fun_root}")

        if previous_root is not None:
            absolute_error = round_significant(abs(root - previous_root), significant_figures)
            relative_error = round_significant(abs((root - previous_root) / root) * 100, significant_figures)
            steps.append(
                f"Absolute error = abs(root - previous_root) = abs({root} - {previous_root}) = {absolute_error}")
            if absolute_error > error:
                steps.append(f"which is still greater than the error ({error})")
            if absolute_error != 0:
                correct_digits = int(np.floor(2 - np.log10(2 * absolute_error)))
                steps.append(
                    f"the number of correct significant digits = floor(2 - log10(2 * absolute_error)) = floor(2 - log10(2 * {absolute_error})) = {correct_digits}")

            steps.append(
                f"Relative error = abs((root - previous_root) / root) * 100% = abs(({root} - {previous_root}) / {root}) * 100% = {relative_error}%")
        else:
            absolute_error = float('inf')
            relative_error = float('inf')
            steps.append("Since it is the first iteration, relative error cannot be calculated.")

        table.append([iteration,
                      f"{low}",
                      f"{high}",
                      f"{root}",
                      f"{relative_error}%" if relative_error != float("inf") else "_",
                      f"{absolute_error}" if relative_error != float("inf") else "_",
                      f"{fun_root}"])

        if function.evaluate(root) == 0 or absolute_error <= error:
            if function.evaluate(root) == 0:
                steps.append(f"function(root) = function({root}) = 0")
            if absolute_error < error:
                steps.append(f"absolute_error < error as {absolute_error} < {error}")
            steps.append(
                f"Root found: {root} after {iteration} iterations with {significant_figures} significant figures and {error} error.")
            if absolute_error != 0:
                correct_digits = int(np.floor(2 - np.log10(2 * absolute_error)))
                steps.append(
                    f"the number of correct significant digits = floor(2 - log10(2 * absolute_error)) = floor(2 - log10(2 * {absolute_error})) = {correct_digits}")
            table_str = tabulate(table, headers=["Iteration", "Low", "High", "Root", "Relative Error", "Absolute Error",
                                                 "function(root)"], tablefmt="grid")
            
            return (root, "\n".join(steps), table_str, iteration, correct_digits, relative_error, absolute_error), lines

        steps.append(f"function(root) = function({root}) = {fun_root}")
        if fun_root < 0:
            steps.append(f"Which is less than 0, hence the root is between low and root.")
            steps.append(f"low = root = {root}")
            steps.append(f"high = {high}")
            low = root
        else:
            steps.append(f"Which is greater than 0, hence the root is between root and high.")
            steps.append(f"low = {low}")
            steps.append(f"high = root = {root}")
            high = root

        previous_root = root

    #steps.append(f"Maximum iterations reached. Root not found within {max_iterations} iterations.")
    table_str = tabulate(table, headers=["Iteration", "Low", "High", "Root", "Relative Error", "Absolute Error",
                                         "function(root)"], tablefmt="grid")

    return (root, "\n".join(steps),f"Maximum iterations reached. Root not found within {max_iterations} iterations.\n" + table_str, iteration, correct_digits, relative_error, absolute_error), lines

    


def plot_interpolation_lines(function, low, high, lines):
    """
    Plots the interpolation lines and the function for False Position Method using Plotly.

    Parameters:
        lines (list): List of [low, fun_low, high, fun_high] at each iteration.
        function (callable): The function to plot.
        low (float): The lower bound for plotting.
        high (float): The upper bound for plotting.
    """
    x_vals = np.linspace(low, high, 2000)
    y_vals = function(x_vals)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name="Function", line=dict(color='blue')))

    for line in lines:
        low_point, fun_low_point, high_point, fun_high_point = line
        fig.add_trace(go.Scatter(x=[low_point, high_point], y=[fun_low_point, fun_high_point], mode='lines',
                                 name=f"Interpolation: {low_point} - {high_point}", line=dict( width=0.5)))

    # Add horizontal and vertical lines at x=0 and y=0 for reference
    fig.add_trace(go.Scatter(x=[low, high], y=[0, 0], mode='lines', name='y=0', line=dict(color='black', width=1)))
    fig.add_trace(go.Scatter(x=[0, 0], y=[min(y_vals), max(y_vals)], mode='lines', name='x=0', line=dict(color='black', width=1)))

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
    return fig