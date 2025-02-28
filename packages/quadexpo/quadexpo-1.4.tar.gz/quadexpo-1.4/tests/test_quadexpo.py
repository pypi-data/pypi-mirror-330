import unittest
import numpy as np
from quadexpo import Quadexpo

class TestQuadexpo(unittest.TestCase):
    def setUp(self):
        self.qe = Quadexpo(1, -2, 3, 0.5)

    def test_evaluate(self):
        result = self.qe.evaluate(5)
        expected_value = 1 * 5**2 - 2 * 5 + 3 * np.exp(-0.5 * 5)
        self.assertAlmostEqual(result, expected_value, places=5)

    def test_integrate(self):
        result = self.qe.integrate(0, 5)
        expected_value = 10.87  # Approximate expected result
        self.assertAlmostEqual(result, expected_value, places=2)

    def test_symbolic_integral(self):
        integral_expr = self.qe.symbolic_integral()
        self.assertIsNotNone(integral_expr)

    def test_generate_data(self):
        x_vals = np.linspace(0, 10, 5)
        df = self.qe.generate_data(x_vals)
        self.assertEqual(len(df), 5)
        self.assertTrue("x" in df.columns)
        self.assertTrue("F(x)" in df.columns)

if __name__ == "__main__":
    unittest.main()
