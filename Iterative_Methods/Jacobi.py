from Approach import Approach
import numpy as np
class Jacobi(Approach):
   def __init__(self, A, b, sig_figs=20, initial_guess=None, tolerance=0, max_iterations=100):
      self.A = np.array(A, dtype=float)
      self.b = np.array(b, dtype=float)
      self.sig_figs = sig_figs
      self.initial_guess = initial_guess
      self.tolerance = tolerance
      self.max_iterations = max_iterations
   
   def solve(self):
      pass