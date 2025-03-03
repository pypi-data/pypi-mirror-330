#!/usr/bin/env -S uv run -s
# /// script
# dependencies = []
# ///
# this_file: tests/test_refactored.py

"""Simple test script to verify the refactored Phiton code works correctly."""

import sys
from pathlib import Path

# Add the parent directory to sys.path to allow importing phiton
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from phiton import ConversionConfig, phitonize_python


def main():
    """Test the refactored Phiton code with a simple example."""
    # Sample Python code
    python_code = """
def fibonacci(n: int) -> int:
    '''Return the nth Fibonacci number.'''
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def main():
    for i in range(10):
        print(f"fibonacci({i}) = {fibonacci(i)}")

if __name__ == "__main__":
    main()
"""

    # Test different compression levels
    for level in range(1, 6):
        config = ConversionConfig(level=level)
        phitonize_python(python_code, config)


if __name__ == "__main__":
    main()
