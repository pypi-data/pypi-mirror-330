"""
Example implementations using Factorchain.
"""

from .core import Factorchain, poly_expand, fourier_transform

# Define a Factorchain instance
example_fc = Factorchain([poly_expand, np.sin])

# Compute using Factorchain
result = example_fc.compute(2)
print("Factorchain result:", result)
