import numpy as np
import commonfunctions

def backward_elimination(u, b, sig_fig=20):
   commonfunctions.output += "\nBackward Elimination:\n"
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
         u[i][k] = commonfunctions.round_to_sig_figs(u[i][k] / pivot, sig_fig)
      commonfunctions.output += f"\nR{i + 1} ←− R{i + 1} / {pivot}\n"
      

      b[i] = commonfunctions.round_to_sig_figs(b[i] / pivot, sig_fig)

      for r in range(i-1, -1, -1):
         mult = commonfunctions.round_to_sig_figs(u[r][j] / u[i][j], sig_fig)
         temp = u[r][j]
         if (mult == 0):
            continue
         b[r] = commonfunctions.round_to_sig_figs(b[r]-mult*b[i], sig_fig)
         for c in range(j, n):
            if c == j:
               u[r][c] = 0
               continue
            u[r][c] = commonfunctions.round_to_sig_figs(u[r][c]-mult*u[r][c], sig_fig)
         commonfunctions.output += f"\nR{i + 1} ←− R{i + 1} - {temp} * R{r + 1}"
         commonfunctions.output += "\n" + commonfunctions.stringify_matrix(u,sig_fig) + "\n"
   commonfunctions.output += "\n" + commonfunctions.stringify_matrix(u,sig_fig) + "\n"
   return u, b