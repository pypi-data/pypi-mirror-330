"""Simple calculator module for demonstrating test cases."""

import logging

logger = logging.getLogger(__name__)

class Calculator:
    """A simple calculator class with basic arithmetic operations."""
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Sum of a and b
        """
        logger.info("Adding %f and %f", a, b)
        result = a + b
        logger.debug("Addition result: %f", result)
        return result
        
    def subtract(self, a: float, b: float) -> float:
        """Subtract two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Difference of a and b
        """
        logger.info("Subtracting %f from %f", b, a)
        result = a - b
        logger.debug("Subtraction result: %f", result)
        return result
        
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Product of a and b
        """
        logger.info("Multiplying %f by %f", a, b)
        result = a * b
        logger.debug("Multiplication result: %f", result)
        return result
        
    def divide(self, a: float, b: float) -> float:
        """Divide two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Quotient of a and b
            
        Raises:
            ZeroDivisionError: If b is zero
        """
        logger.info("Dividing %f by %f", a, b)
        if b == 0:
            logger.error("Division by zero attempted!")
            raise ValueError("Cannot divide by zero")
        result = a / b
        logger.debug("Division result: %f", result)
        return result
        
    def power(self, base: float, exponent: int) -> float:
        """Raise base to the power of exponent.
        
        Args:
            base: Base number
            exponent: Exponent (must be integer)
            
        Returns:
            base raised to exponent power
            
        Raises:
            TypeError: If exponent is not an integer
        """
        logger.info("Calculating %f raised to power %f", base, exponent)
        if not isinstance(exponent, int):
            logger.error("Invalid operation: exponent must be an integer")
            raise TypeError("Exponent must be an integer")
        result = base ** exponent
        logger.debug("Power operation result: %f", result)
        return result
