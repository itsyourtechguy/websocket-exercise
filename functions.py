"""
RPC Function Registry
=====================
Contains the actual functions that clients can call remotely.
"""

from typing import Callable, Dict


def add_numbers(a: float, b: float) -> float:
    """
    Add two numbers together.
    
    Raises:
        TypeError: If either argument is not a number
    """
    # Validate input types to prevent runtime errors
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("'a' and 'b' must be numbers")
    return a + b


def multiply_numbers(a: float, b: float) -> float:
    """
    Multiply two numbers together.
    
    Raises:
        TypeError: If either argument is not a number
    """
    # Validate input types to prevent runtime errors
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("'a' and 'b' must be numbers")
    return a * b


def echo(message: str) -> str:
    """
    Return the same message that was sent.
    
    Raises:
        TypeError: If the message is not a string
    """
    # Validate input type to prevent runtime errors
    if not isinstance(message, str):
        raise TypeError("'message' must be a string")
    return message

# This makes it easy to add new functions without changing server code
FUNCTION_REGISTRY: Dict[str, Callable] = {
    "add_numbers": add_numbers,
    "multiply_numbers": multiply_numbers,
    "echo": echo,
}

# Example of how to add a new function:
# 
# def new_function(x: int) -> str:
#     return f"Number is: {x}"
# 
# Then add it to the registry:
# FUNCTION_REGISTRY["new_function"] = new_function