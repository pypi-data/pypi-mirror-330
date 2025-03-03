#!/usr/bin/env python3
# this_file: tests/test_converter.py
"""Tests for the Phiton converter module."""

from pathlib import Path

import pytest

from phiton import ConversionConfig, phitonize_python

# Get the path to the test data directory
TEST_DATA_DIR = Path(__file__).parent / "data"
EXPECTED_DIR = TEST_DATA_DIR / "expected"


def read_file(path):
    """Read a file and return its contents."""
    with open(path, encoding="utf-8") as f:
        return f.read()


def test_compress_simple_level1():
    """Test compressing a simple Python file with level 1 compression."""
    # Read the test file
    source_code = read_file(TEST_DATA_DIR / "simple.py")

    # Compress the source code
    config = ConversionConfig(level=1)
    result = phitonize_python(source_code, config)

    # Check that the result is a non-empty string
    assert isinstance(result, str)
    assert len(result) > 0

    # Check for some expected Phiton symbols
    assert "⦂" in result  # Type annotation symbol
    assert "⟮" in result  # Type bracket open
    assert "⟯" in result  # Type bracket close


def test_compress_simple_level5():
    """Test compressing a simple Python file with level 5 compression."""
    # Read the test file
    source_code = read_file(TEST_DATA_DIR / "simple.py")

    # Compress the source code
    config = ConversionConfig(level=5)
    result = phitonize_python(source_code, config)

    # Check that the result is a non-empty string
    assert isinstance(result, str)
    assert len(result) > 0

    # Check for some expected Phiton symbols at level 5
    assert "⦂" in result  # Type annotation symbol
    assert "⟮" in result  # Type bracket open
    assert "⟯" in result  # Type bracket close
    assert "ƒ" in result  # Function symbol


def test_compression_levels():
    """Test that higher compression levels produce more compressed output."""
    # Read the test file
    source_code = read_file(TEST_DATA_DIR / "complex.py")

    # Compress with different levels
    results = {}
    for level in range(1, 6):
        config = ConversionConfig(level=level)
        result = phitonize_python(source_code, config)
        results[level] = len(result)

    # Check that level 5 produces more compressed output than level 1
    assert results[5] < results[1], (
        "Level 5 should produce more compressed output than level 1"
    )

    # Check that the compression is generally increasing with level
    # Note: Some levels might have similar compression ratios due to implementation details
    decreasing_count = 0
    for i in range(1, 5):
        if results[i] < results[i + 1]:
            decreasing_count += 1

    # Allow at most one level to have worse compression than the next
    assert decreasing_count <= 1, (
        f"Too many compression level inversions: {decreasing_count}"
    )


def test_config_options():
    """Test different configuration options."""
    # Read the test file
    source_code = read_file(TEST_DATA_DIR / "complex.py")

    # Test with different configurations
    configs = [
        ConversionConfig(level=5, comments=True, type_hints=True),
        ConversionConfig(level=5, comments=False, type_hints=True),
        ConversionConfig(level=5, comments=True, type_hints=False),
        ConversionConfig(level=5, comments=True, type_hints=True, symbols=False),
    ]

    results = []
    for config in configs:
        result = phitonize_python(source_code, config)
        results.append(result)

    # Check that at least some configurations produce different results
    different_results = set()
    for result in results:
        different_results.add(result)

    # We should have at least 2 different results from our 4 configurations
    assert len(different_results) >= 2, (
        "At least some configurations should produce different results"
    )


def test_pattern_recognition():
    """Test pattern recognition in the compression algorithm."""
    # Read the test file
    source_code = read_file(TEST_DATA_DIR / "patterns.py")

    # Compress with maximum level
    config = ConversionConfig(level=5)
    result = phitonize_python(source_code, config)

    # Check that the result is significantly smaller than the original
    assert len(result) < len(source_code) * 0.8, (
        "Pattern recognition should significantly reduce the size"
    )


def test_syntax_error_handling():
    """Test handling of syntax errors in the input code."""
    # Create a Python file with syntax errors
    source_code = """
    def invalid_function():
        print("This is invalid
        return None
    """

    # Compress the code and expect a SyntaxError
    config = ConversionConfig()
    with pytest.raises(SyntaxError):
        phitonize_python(source_code, config)
