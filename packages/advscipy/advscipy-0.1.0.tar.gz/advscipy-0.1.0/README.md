# AdvSciPy

AdvSciPy is an advanced extension of the popular SciPy library, providing enhanced functionality for scientific computing.

## Installation

```bash
pip install advscipy
```

USAGE
from advscipy import advanced_minimize

# Define a simple quadratic function: f(x) = (x - 3)^2

def objective_function(x):
return (x - 3) \*\* 2

# Perform optimization

result = advanced_minimize(objective_function, x0=[0], method='BFGS')
print(result)
