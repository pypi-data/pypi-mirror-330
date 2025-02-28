# Quadexpo 1.4

A Python library implementing the Quadexpo function for modeling complex systems involving both quadratic and exponential behaviors.

## What's New in 1.4?
- **Object-Oriented Design**: Use a class-based approach for easy function manipulation.
- **Symbolic Integration Support**: Compute symbolic integrals using SymPy.
- **Data Handling**: Generate and analyze function evaluations using Pandas.
- **Expanded Test Suite**: More robust tests covering symbolic computation and data generation.

## Installation

```sh
pip install quadexpo
```

## Usage

```python
from quadexpo import Quadexpo
import numpy as np

# Initialize with parameters
qe = Quadexpo(1, -2, 3, 0.5)

# Evaluate at a point
print(qe.evaluate(5))

# Compute definite integral
print(qe.integrate(0, 5))

# Get symbolic integral
print(qe.symbolic_integral())

# Generate function data
x_vals = np.linspace(0, 10, 10)
df = qe.generate_data(x_vals)
print(df)
```

## License

MIT License
