import numpy as np
from abc import ABC, abstractmethod
from Approach import Approach
from Direct import forwardElimination, backwardElimination, forwardSubstitution

class LU(Approach,ABC):
    @abstractmethod
    def solve(self):
        pass

    @abstractmethod
    def getMatrixL(self):
        pass

    @abstractmethod
    def getMatrixU(self):
        pass
