from abc import ABC, abstractmethod
# Abstract base classes
class Approach:
   @abstractmethod
   def solve(self,A, b, sig_figs=20, initial_guess=None, tolerance=0, max_iterations=100):
      """
      Abstract method that must be implemented by subclasses
      """
      pass