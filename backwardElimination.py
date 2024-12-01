import numpy as np
from commonfunctions import round_to_sig_figs

def backward_elimination(u, b, sig_fig=20):
   n = len(u)
   for i in range(n-1, -1, -1):
      j = i
      while j < n and u[i][j] == 0:
         j += 1
      if (j == n or u[i][j] == 0):
         continue
      pivot = u[i][j]

      u[i][j] = 1

      for k in range(j+1, n):
         u[i][k] = round_to_sig_figs(u[i][k] / pivot, sig_fig)

      b[i] = round_to_sig_figs(b[i] / pivot, sig_fig)

      for r in range(i-1, -1, -1):
         mult = round_to_sig_figs(u[r][j]/u[i][j], sig_fig)
         if (mult == 0):
            continue
         b[r] = round_to_sig_figs(b[r]-mult*b[i], sig_fig)
         for c in range(j, n):
            if c == j:
               u[r][c] = 0
               continue
            u[r][c] = round_to_sig_figs(u[r][c]-mult*u[r][c], sig_fig)
   
   return u, b