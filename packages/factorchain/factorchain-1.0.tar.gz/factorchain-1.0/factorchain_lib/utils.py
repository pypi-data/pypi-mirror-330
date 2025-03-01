"""
Utility functions for Factorchain framework.
"""

import numpy as np

def taylor_series_expansion(func, x, order=5):
    """Computes the Taylor series expansion of a function."""
    return sum([(func(x) / np.math.factorial(n)) * (x ** n) for n in range(order)])

def partial_fraction_decomposition(num, den):
    """Performs partial fraction decomposition."""
    return np.polydiv(num, den)
