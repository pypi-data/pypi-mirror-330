# Factorchain Library

Factorchain is a powerful mathematical framework for optimizing computation chains using interconnected operations.

## Installation
```sh
pip install factorchain
```

## Usage

```python
from factorchain import Factorchain

def square(x):
    return x * x

fc = Factorchain([square, np.sin])
result = fc.compute(3)
print(result)
```

## Features
- Matrix operations
- Fourier Transforms
- Polynomial expansions
- Neural network applications
