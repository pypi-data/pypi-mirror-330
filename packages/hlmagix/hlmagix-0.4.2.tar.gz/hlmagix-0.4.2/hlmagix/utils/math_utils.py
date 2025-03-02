# math_utils.py
# This module contains utility functions for mathematical operations

def add(a, b):
    """
    Add two numbers together.
    
    Args:
        a (number): First number
        b (number): Second number
        
    Returns:
        number: The sum of a and b
    """
    return a + b


def multiply(a, b):
    """
    Multiply two numbers.
    
    Args:
        a (number): First number
        b (number): Second number
        
    Returns:
        number: The product of a and b
    """
    return a * b


def divide(a, b):
    """
    Divide first number by second number.
    
    Args:
        a (number): Numerator
        b (number): Denominator
        
    Returns:
        float: The result of a divided by b
        
    Raises:
        ZeroDivisionError: If b is zero
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b