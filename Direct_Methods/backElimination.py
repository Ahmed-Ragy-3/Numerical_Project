import numpy as np


def round_to_sig_figs(x, sig_figs):
    if x == 0:
        return 0
    else:
        magnitude = int(np.ceil(np.log10(abs(x))))
        return round(x, sig_figs - magnitude)


def backwardElimination(u, b, sig_fig=20):
    n = len(u)
    for i in range(n-1, -1, -1):
        j = i
        while j < n and u[i][j] == 0:
            j += 1
        if (j == n or u[i][j] == 0):
            continue
        pivot = u[i][j]

        u[i][j] = 1

        """ u[i] = u[i]/pivot
        b[i] = b[i]/pivot without sig fig"""

        for k in range(j+1, n):
            u[i][k] = round_to_sig_figs(u[i][k] / pivot, sig_fig)

        b[i] = round_to_sig_figs(b[i] / pivot, sig_fig)

        for r in range(i-1, -1, -1):
            mult = round_to_sig_figs(u[r][j]/u[i][j], sig_fig)
            if (mult == 0):
                continue
            b[r] = round_to_sig_figs(b[r]-mult*b[i], sig_fig)
            for c in range(j, n):
                if (c == j):
                    u[r][c] = 0
                    continue
                u[r][c] = round_to_sig_figs(u[r][c]-mult*u[r][c], sig_fig)

        """ without sig fig for r in range (i-1,-1,-1):
            mult = u[r][j]/u[i][j]
            b[r] = b[r]-mult*b[i]
            u[r] = u[r]-mult*u[i] """
