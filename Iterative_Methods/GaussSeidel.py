from Approach import Approach
import numpy as np
from iterativeSolver import iterative_solver
class Seidel(Approach):
   def __init__(self,A, b, sig_figs=20, initial_guess=None, tolerance=0, max_iterations=100):
      self.A = np.array(A, dtype=float)
      self.b = np.array(b, dtype=float)
      self.sig_figs = sig_figs
      self.initial_guess = initial_guess
      self.tolerance = tolerance
      self.max_iterations = max_iterations
   
   def solve(self):
      x = np.zeros_like(self.b, dtype=np.float64) if self.initial_guess is None else self.initial_guess.copy()
      answers,iterations = iterative_solver(self.A,self.b,self.sig_figs,x,self.tolerance,self.max_iterations)
      z = ""
      for i in range(len(answers)) :
         z+=f"x{i+1} = {answers[i]}\n"
      

      return self.A,answers,z
   


      
    


