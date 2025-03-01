"""Test suite for the calculator module."""

import unittest
import logging
from invenio_et_probo.samples.calculator import Calculator

logger = logging.getLogger(__name__)

class TestCalculator(unittest.TestCase):
    """Test cases for Calculator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        logger.info("Setting up calculator test")
        self.calc = Calculator()
        
    def tearDown(self):
        """Clean up after tests."""
        logger.info("Tearing down calculator test")
        
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        logger.info("Testing addition of positive numbers")
        self.assertEqual(self.calc.add(3, 5), 8)
        logger.info("Addition of positive numbers test passed")
        
    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        logger.info("Testing addition of negative numbers")
        self.assertEqual(self.calc.add(-2, -3), -5)
        logger.info("Addition of negative numbers test passed")
        
    def test_add_zero(self):
        """Test adding zero to a number."""
        logger.info("Testing addition of zero")
        self.assertEqual(self.calc.add(7, 0), 7)
        logger.info("Addition of zero test passed")
        
    def test_subtract_positive_result(self):
        """Test subtraction with positive result."""
        logger.info("Testing subtraction with positive result")
        self.assertEqual(self.calc.subtract(10, 3), 7)
        logger.info("Subtraction with positive result test passed")
        
    def test_subtract_negative_result(self):
        """Test subtraction with negative result."""
        logger.info("Testing subtraction with negative result")
        self.assertEqual(self.calc.subtract(3, 10), -7)
        logger.info("Subtraction with negative result test passed")
        
    def test_multiply_positive_numbers(self):
        """Test multiplying two positive numbers."""
        logger.info("Testing multiplication of positive numbers")
        self.assertEqual(self.calc.multiply(4, 5), 20)
        logger.info("Multiplication of positive numbers test passed")
        
    def test_multiply_negative_numbers(self):
        """Test multiplying two negative numbers."""
        logger.info("Testing multiplication of negative numbers")
        self.assertEqual(self.calc.multiply(-2, -3), 6)
        logger.info("Multiplication of negative numbers test passed")
        
    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        logger.info("Testing multiplication by zero")
        self.assertEqual(self.calc.multiply(5, 0), 0)
        logger.info("Multiplication by zero test passed")
        
    def test_divide_positive_numbers(self):
        """Test dividing two positive numbers."""
        logger.info("Testing division of positive numbers")
        self.assertEqual(self.calc.divide(10, 2), 5)
        logger.info("Division of positive numbers test passed")
        
    def test_divide_negative_numbers(self):
        """Test dividing two negative numbers."""
        logger.info("Testing division of negative numbers")
        self.assertEqual(self.calc.divide(-10, -2), 5)
        logger.info("Division of negative numbers test passed")
        
    def test_divide_by_zero(self):
        """Test that division by zero raises an error."""
        logger.info("Testing division by zero")
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(5, 0)
        logger.info("Division by zero test passed")
        
    def test_power_positive_exponent(self):
        """Test power with positive exponent."""
        logger.info("Testing power operation with positive exponent")
        self.assertEqual(self.calc.power(2, 3), 8)
        logger.info("Power operation with positive exponent test passed")
        
    def test_power_zero_exponent(self):
        """Test power with zero exponent."""
        logger.info("Testing power operation with zero exponent")
        self.assertEqual(self.calc.power(5, 0), 1)
        logger.info("Power operation with zero exponent test passed")
        
    def test_power_negative_exponent(self):
        """Test power with negative exponent."""
        logger.info("Testing power operation with negative exponent")
        self.assertEqual(self.calc.power(2, -2), 0.25)
        logger.info("Power operation with negative exponent test passed")
        
    def test_power_non_integer_exponent(self):
        """Test that non-integer exponent raises TypeError."""
        logger.info("Testing power operation with non-integer exponent")
        with self.assertRaises(TypeError):
            self.calc.power(2, 2.5)
        logger.info("Power operation with non-integer exponent test passed")
        
    def test_failing_addition(self):
        """Test that should fail: incorrect addition."""
        logger.info("Running test that will fail")
        try:
            self.assertEqual(self.calc.add(2, 2), 5, "2 + 2 should equal 4")
        except AssertionError:
            logger.error("Test failed as expected: 2 + 2 != 5")
            raise
        
    def test_failing_multiplication(self):
        """Test that should fail: incorrect multiplication."""
        logger.info("Running test that will fail")
        try:
            self.assertEqual(self.calc.multiply(3, 4), 11, "3 * 4 should equal 12")
        except AssertionError:
            logger.error("Test failed as expected: 3 * 4 != 11")
            raise
        
    def test_failing_power(self):
        """Test that should fail: incorrect power calculation."""
        logger.info("Running test that will fail")
        try:
            self.assertEqual(self.calc.power(2, 4), 15, "2 ^ 4 should equal 16")
        except AssertionError:
            logger.error("Test failed as expected: 2 ^ 4 != 15")
            raise
        
if __name__ == '__main__':
    unittest.main()
