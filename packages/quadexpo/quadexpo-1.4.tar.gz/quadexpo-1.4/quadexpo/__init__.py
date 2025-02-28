import numpy as np
import sympy as sp
import pandas as pd
from scipy.integrate import quad

class Quadexpo:
    def __init__(self, a, b, c, k):
        self.a = a
        self.b = b
        self.c = c
        self.k = k

    def evaluate(self, x):
        """Evaluates the function at a given x."""
        return self.a * x**2 + self.b * x + self.c * np.exp(-self.k * x)

    def integrate(self, x_min, x_max):
        """Computes the definite integral of the function from x_min to x_max."""
        def integrand(x):
            return self.evaluate(x)
        result, _ = quad(integrand, x_min, x_max)
        return result

    def symbolic_integral(self):
        """Computes the symbolic integral of the function."""
        x = sp.symbols('x')
        expr = self.a * x**2 + self.b * x + self.c * sp.exp(-self.k * x)
        return sp.integrate(expr, x)

    def generate_data(self, x_values):
        """Generates a Pandas DataFrame with function evaluations over given x values."""
        data = {"x": x_values, "F(x)": [self.evaluate(x) for x in x_values]}
        return pd.DataFrame(data)
