#!/usr/bin/env python3
"""A simple Python file for testing Phiton conversion."""
import contextlib


def add(a: int, b: int) -> int:
    """Add two numbers and return the result.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b


def subtract(a: int, b: int) -> int:
    """Subtract b from a and return the result."""
    return a - b


def multiply(a: int, b: int) -> int:
    """Multiply two numbers and return the result."""
    return a * b


def divide(a: int, b: int) -> float:
    """Divide a by b and return the result."""
    if b == 0:
        msg = "Cannot divide by zero"
        raise ValueError(msg)
    return a / b


def main():
    """Main function to demonstrate the operations."""
    x = 10


    # Test error handling
    with contextlib.suppress(ValueError):
        divide(x, 0)


if __name__ == "__main__":
    main()
