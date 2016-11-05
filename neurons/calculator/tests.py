import unittest

from core.NeuronModule import InvalidParameterException
from neurons.calculator.calculator import Calculator

class TestCalculator(unittest.TestCase):

    """
    Unit test series to check input leads to proper output
    run test suite via:
    `python -m unittest discover`
    from project root
    """

    def test_addition(self):
        calc = Calculator(operation="2 + 7")
        self.assertEqual(calc.result, '9')

    def test_subtraction(self):
        calc = Calculator(operation="2 - 7")
        self.assertEqual(calc.result, '-5')

    def test_multiplicaton(self):
        calc = Calculator(operation="2 x 7.5")
        self.assertEqual(calc.result, '15')

    def test_division(self):
        calc = Calculator(operation="2 / 3")
        self.assertEqual(calc.result, '0 virgule 667')

    def test_cannot_divide_by_zero(self):
        # making sure division by zero raises an InvalidParameterException
        with self.assertRaises(InvalidParameterException):
            calc = Calculator(operation="2 / 0")

    def test_power(self):
        calc = Calculator(operation="2 puissance 5")
        self.assertEqual(calc.result, '32')

    def test_percent(self):
        calc = Calculator(operation="50 % 42")
        self.assertEqual(calc.result, '21')

    def test_percent_text(self):
        # making sure STT replacement works
        calc = Calculator(operation="50 pourcent de 42")
        self.assertEqual(calc.result, '21')

if __name__ == '__main__':
    unittest.main()