import sys
import numpy as np
from tabulate import tabulate
import plotly.graph_objects as go


def round_significant(value, sig_figs):
    if value == 0:
        return 0
    elif value == float('inf') or value == -float('inf'):
        return float('inf')
    else:
        return round(value, sig_figs - int(np.floor(np.log10(abs(value)))) - 1)


def bisection_method(function, low: float, high: float, significant_figures=sys.float_info.dig, error=0.00001, max_iterations=50):
    """
    Parameters:
        function (callable): The function for which to find the root.
        low (float): Lower bound.
        high (float): Upper bound.
        significant_figures (int, optional): Number of significant figures for rounding.
        error (float): Error threshold for stopping the iterations.
        max_iterations (int): Maximum number of iterations.

    Returns:
        root: float, steps: str, table: str, graph: plotly graph object, interations done: int
    """
    min_low = low
    max_high = high
    previous_root = None
    table = []
    steps = []
    lines = []

    low = round_significant(low, significant_figures)
    high = round_significant(high, significant_figures)
    fun_low = round_significant(function(low), significant_figures)
    fun_high = round_significant(function(high), significant_figures)


    steps.append("Check if the function changes sign between low and high:")
    steps.append(f"function(low) * function(high) = function({low}) * function({high}) = {fun_low} * {fun_high}")

    if fun_low * fun_high > 0:
        steps.append("Which is greater than 0. Can't be solved: no bracketing found.")
        graph = plot_bisection_results(function, min_low, max_high, lines)
        return None, "\n".join(steps), "", graph, 0

    steps.append("Which is less than 0. So there is at least one root between the bounds.")
    steps.append(f"the number of iterations needed is = ceil(log2((high - low) / error)) = ceil(log2(({high} - {low}) / {error})) = {int(np.ceil(np.log2((high - low) / error)))}")

    for iteration in range(1, max_iterations + 1):
        low = round_significant(low, significant_figures)
        high = round_significant(high, significant_figures)
        round_significant(function(low), significant_figures)
        round_significant(function(high), significant_figures)

        steps.append(f"\nIteration {iteration}:\n")
        steps.append(f"low = {low}, high = {high}")
        root = round_significant((low + high) / 2.0, significant_figures)
        steps.append(f"Estimated root = (low + high) / 2 = ({low} + {high}) / 2 = {root}")
        fun_root = round_significant(function(root), significant_figures)
        steps.append(f"function(estimated_root) = function({root}) = {fun_root}")

        lines.append(root)

        if previous_root is not None:
            absolute_error = round_significant(abs(root - previous_root), significant_figures)
            relative_error = round_significant(abs((root - previous_root) / root) * 100, significant_figures)
            steps.append(f"Absolute error = abs(root - previous_root) = abs({root} - {previous_root}) = {absolute_error}")
            if absolute_error > error:
                steps.append(f"which is still greater than the error ({error})")
            steps.append(f"Relative error = abs((root - previous_root) / root) * 100% = abs(({root} - {previous_root}) / {root}) * 100% = {relative_error}%")
        else:
            absolute_error = float('inf')
            relative_error = float('inf')
            steps.append("Since it is the first iteration, relative error cannot be calculated.")

        table.append([iteration,
                      f"{low}",
                      f"{high}",
                      f"{root}",
                      f"{relative_error}%" if relative_error != float("inf") else "_",
                      f"{absolute_error}"if relative_error != float("inf") else "_",
                      f"{fun_root}"])

        if function(root) == 0 or absolute_error < error:
            if function(root) == 0:
                steps.append(f"function(root) = function({root}) = 0")
            if absolute_error < error:
                steps.append(f"absolute_error < error as {absolute_error} < {error}")
            steps.append(f"Root found: {root} after {iteration} iterations with {significant_figures} significant figures and {error} error.")
            if absolute_error != 0:
                steps.append(f"the number of correct significant digits = floor(2 - log10(2 * absolute_error)) = floor(2 - log10(2 * {absolute_error})) = {int(np.floor(2 - np.log10(2 * absolute_error)))}")
            table_str = tabulate(table, headers=["Iteration", "Low", "High", "Root", "Relative Error", "Absolute Error", "function(root)"], tablefmt="grid")
            graph = plot_bisection_results(function, min_low, max_high, lines)
            return root, "\n".join(steps), table_str, graph, iteration

        steps.append(f"function(low) * function(root) = function({low}) * function({root}) = {fun_low} * {fun_root}")
        if fun_low * fun_root < 0:
            steps.append(f"Which is less than 0, hence the root is between low and root.")
            steps.append(f"low = {low}")
            steps.append(f"high = root = {root}")
            high = root
        else:
            steps.append(f"Which is greater than 0, hence the root is between root and high.")
            steps.append(f"low = root = {root}")
            steps.append(f"high = {high}")
            low = root

        previous_root = root

    steps.append(f"Maximum iterations reached. Root not found within {max_iterations} iterations.")
    table_str = tabulate(table, headers=["Iteration", "Low", "High", "Root", "Relative Error", "Absolute Error", "function(root)"], tablefmt="grid")
    graph = plot_bisection_results(function, min_low, max_high, lines)
    return root, "\n".join(steps), table_str, graph, max_iterations

def plot_bisection_results(function, low, high, vertical_lines):
    """
    Plots the function and vertical lines for roots.

    Parameters:
        function (callable): The function to plot.
        low (float): Lower bound for plotting.
        high (float): Upper bound for plotting.
        vertical_lines (list): List of root values for vertical lines.
    """
    x_vals = np.linspace(low, high, 1000)
    y_vals = function(x_vals)

    fig = go.Figure()

    # Plot the function
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name="Function", line=dict(color='blue')))

    # Add vertical lines for each root
    for root in vertical_lines:
        fig.add_trace(go.Scatter(x=[root, root], y=[min(y_vals), max(y_vals)], mode='lines', name=f"Root {root}", line=dict(width=0.5)))

        # Add horizontal and vertical lines at x=0 and y=0 for reference
    fig.add_trace(go.Scatter(x=[low, high], y=[0, 0], mode='lines', name='y=0', line=dict(color='black', width=1)))
    fig.add_trace(
        go.Scatter(x=[0, 0], y=[min(y_vals), max(y_vals)], mode='lines', name='x=0', line=dict(color='black', width=1)))

    fig.update_layout(
        title="Bisection Method",
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