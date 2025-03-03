#!/usr/bin/env python3
# this_file: tests/test_utils.py
"""Tests for the Phiton utils module."""

import ast

from phiton.utils import calculate_stats, optimize_final, optimize_imports


def test_optimize_imports():
    """Test that optimize_imports correctly optimizes import statements."""
    # Sample Python code with imports
    code = """import numpy as np
import pandas as pd
from numpy import array
from pandas import DataFrame
import matplotlib.pyplot as plt
"""

    # Parse the code into an AST
    tree = ast.parse(code)

    # Optimize the imports
    optimized = optimize_imports(tree)

    # Check that the imports were optimized
    assert len(optimized) <= 5, "Imports should be combined"

    # Check that domain-specific imports are grouped
    numpy_imports = [imp for imp in optimized if "numpy" in imp]
    pandas_imports = [imp for imp in optimized if "pandas" in imp]

    assert len(numpy_imports) <= 2, "numpy imports should be combined"
    assert len(pandas_imports) <= 2, "pandas imports should be combined"


def test_optimize_final_levels():
    """Test that optimize_final applies different optimizations based on level."""
    # Sample Phiton code
    code = "ƒ add(a, b)⟨ ⇐ a + b ⟩"

    # Optimize with different levels
    level1 = optimize_final(code, 1)
    level3 = optimize_final(code, 3)
    level5 = optimize_final(code, 5)

    # Check that higher levels produce more optimized code
    assert len(level1) >= len(level3), "Level 3 should be more optimized than level 1"
    assert len(level3) >= len(level5), "Level 5 should be more optimized than level 3"

    # Check specific optimizations
    assert " " in level1, "Level 1 should preserve whitespace"
    assert " " not in level5, "Level 5 should remove all whitespace"


def test_optimize_final_patterns():
    """Test that optimize_final correctly applies pattern replacements."""
    # Sample code with patterns
    code = "x + 1"

    # Optimize with level 5
    optimized = optimize_final(code, 5)

    # Check that patterns were replaced
    assert "x⁺" in optimized, "x + 1 should be replaced with x⁺"

    # Test another pattern
    code = "x ** 2"
    optimized = optimize_final(code, 5)
    assert "x²" in optimized, "x ** 2 should be replaced with x²"


def test_calculate_stats():
    """Test that calculate_stats correctly calculates compression statistics."""
    # Sample source and result
    source = "def add(a, b):\n    return a + b"
    result = "ƒadd(a,b)⟨⇐a+b⟩"

    # Calculate stats
    stats = calculate_stats(source, result)

    # Check that stats are calculated correctly
    assert stats["original_chars"] == len(source)
    assert stats["compressed_chars"] == len(result)
    assert stats["original_lines"] == 2
    assert stats["compressed_lines"] == 1
    assert stats["compression_ratio"] == round(len(result) / len(source) * 100, 2)

    # Check that compression ratio is calculated correctly
    expected_ratio = len(result) / len(source) * 100
    assert abs(stats["compression_ratio"] - expected_ratio) < 0.01, (
        "Compression ratio should be calculated correctly"
    )


def test_optimize_final_whitespace():
    """Test that optimize_final correctly handles whitespace based on level."""
    # Sample code with whitespace
    code = "ƒ add(a, b) ⟨\n    ⇐ a + b\n⟩"

    # Optimize with different levels
    level1 = optimize_final(code, 1)
    level2 = optimize_final(code, 2)
    level4 = optimize_final(code, 4)

    # Check whitespace handling
    assert "\n" not in level1, "Level 1 should normalize but preserve some whitespace"
    assert " " in level1, "Level 1 should preserve spaces"

    assert "\n" not in level2, "Level 2 should remove newlines"
    assert " " in level2, "Level 2 should preserve some spaces"

    assert " " not in level4, "Level 4 should remove all whitespace"
