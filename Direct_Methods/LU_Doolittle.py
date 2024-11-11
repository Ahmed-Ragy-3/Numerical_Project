from Approach import Approach
import numpy as np


class Doolittle(Approach):
   def __init__(self, A, b, sig_figs=20):
      self.A = np.array(A, dtype=float)
      self.b = np.array(b, dtype=float)
      self.sig_figs = sig_figs
      self.L = None
      self.U = None
   
   def solve(self):
      pass