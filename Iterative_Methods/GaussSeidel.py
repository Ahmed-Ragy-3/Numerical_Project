from Approach import Approach
import numpy as np
from iterativeSolver import iterative_solver
class Seidel(Approach):
   def __init__(self):
      pass
   
   def solve(self,A, b, sig_figs=20, initial_guess=None, tolerance=0, max_iterations=100):
      x = np.zeros_like(b, dtype=np.float64) if initial_guess is None else initial_guess.copy()
      answers,iterations = iterative_solver(A,b,sig_figs,x,tolerance,max_iterations)
      z = ""
      for i in range(len(answers)) :
         z+=f"x{i+1} = {answers[i]}\n"
      

      return A,answers,z
   


      
    


