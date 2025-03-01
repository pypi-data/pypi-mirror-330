"""
Core module for Factorchain mathematical framework.
"""

import numpy as np

class Factorchain:
    def __init__(self, functions):
        """Initializes a Factorchain with a sequence of functions."""
        self.functions = functions

    def compute(self, x):
        """Applies the sequence of functions to input x."""
        for func in self.functions:
            x = func(x)
        return x

# Example operations
def poly_expand(x):
    return x**2 + 2*x + 1

def fourier_transform(x):
    return np.fft.fft(x)

def matrix_mult(x, matrix):
    return np.dot(matrix, x)
