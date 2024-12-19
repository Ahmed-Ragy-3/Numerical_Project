import numpy as np
from bracketing_method import bisection_method, plot_bisection_results
from false_position_method import false_position_method, plot_interpolation_lines


def func4(x):
    return x**3 - 25

def func(x):
    return x**4 + 3 * x - 4

def func3(x):  # from 11/3 to 13/3, 5 sig_figs, 1e-5 error
    return (3.0 / 2.0) * x - 6.0 - (1 / 2.0) * np.sin(2.0 * x)

def func5(x):
    return 3 * x ** 4 + 6.1 * x ** 3 - 2 * x ** 2 + 3 * x + 2


if __name__ == "__main__":
    root, steps, table, graph, iterations = bisection_method(func4, 2, 3, significant_figures=15, error=1e-10, max_iterations=200)
    graph.show()
    print(steps)
    print(table)
    print("By bisection, root = ", root, " in", iterations, " iterations")

    root, steps, table, graph, iterations = false_position_method(func4, 2, 3, significant_figures=15, error=1e-10, max_iterations=200)
    graph.show()
    print(steps)
    print(table)
    print("By false position, root = ", root, " in", iterations, " iterations")
