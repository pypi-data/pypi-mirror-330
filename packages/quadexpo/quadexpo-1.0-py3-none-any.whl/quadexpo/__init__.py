import numpy as np
from scipy.integrate import quad

def quadexpo_function(a, b, c, k, x_min, x_max):
    """
    Computes the integral of the Quadexpo function from x_min to x_max.
    
    F(x) = ∫[x_min to x_max] [ax^2 + bx + c * e^(-kx)] dx
    
    Parameters:
    - a, b, c, k: Coefficients of the function
    - x_min, x_max: Limits of integration
    
    Returns:
    - The computed integral value
    """
    def integrand(x):
        return a*x**2 + b*x + c * np.exp(-k*x)
    
    result, _ = quad(integrand, x_min, x_max)
    return result
