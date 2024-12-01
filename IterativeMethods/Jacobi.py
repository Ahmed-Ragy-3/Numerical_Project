# from Approach import Approach
import numpy as np
from ..Helpers.iterativeSolver import iterative_solver

class Jacobi:
   def __init__(self, matrix, b, sig_digs, max_iterations=100, tol=0, initial=None):
      self.matrix = matrix
      self.b = b
      self.max_iterations = max_iterations
      self.iterations = 0
      self.tolerance = tol
      self.significant_digits = sig_digs
      self.initial_guess = initial
      self.answer = []
   
   def solve(self):
      if self.initial_guess is None:
         self.initial_guess = np.zeros_like(self.b, dtype=np.float64)
         
      
      self.answer, self.iterations = iterative_solver(
         self.matrix, self.b, self.significant_digits,
         self.initial_guess, self.tolerance, self.max_iterations, isJacobi=True
      )
      
      return self.answer, self.iterations