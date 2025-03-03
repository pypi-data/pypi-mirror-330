#!/usr/bin/env python3
# this_file: tests/test_converter.py
"""Tests for the Phiton converter module."""

import pytest
from pathlib import Path

from phiton import compress_to_phiton, ConversionConfig


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

    # Read the expected output
    expected = read_file(EXPECTED_DIR / "simple_level1.phi")

    # Compress the source code
    config = ConversionConfig(level=1)
    result = compress_to_phiton(source_code, config)

    # Compare the result with the expected output
    # We strip whitespace for comparison to handle platform-specific line endings
    assert result.strip() == expected.strip()


def test_compress_simple_level5():
    """Test compressing a simple Python file with level 5 compression."""
    # Read the test file
    source_code = read_file(TEST_DATA_DIR / "simple.py")

    # Read the expected output
    expected = read_file(EXPECTED_DIR / "simple_level5.phi")

    # Compress the source code
    config = ConversionConfig(level=5)
    result = compress_to_phiton(source_code, config)

    # Compare the result with the expected output
    # We strip whitespace for comparison to handle platform-specific line endings
    assert result.strip() == expected.strip()


def test_compression_levels():
    """Test that higher compression levels produce smaller output."""
    # Read the test file
    source_code = read_file(TEST_DATA_DIR / "complex.py")

    # Compress with different levels
    results = []
    for level in range(1, 6):
        config = ConversionConfig(level=level)
        result = compress_to_phiton(source_code, config)
        results.append(len(result))

    # Check that each level produces smaller or equal output than the previous
    for i in range(1, len(results)):
        assert results[i] <= results[i - 1], (
            f"Level {i + 1} should produce smaller or equal output than level {i}"
        )


def test_config_options():
    """Test that configuration options affect the output."""
    # Read the test file
    source_code = read_file(TEST_DATA_DIR / "simple.py")

    # Test with different configurations
    config1 = ConversionConfig(level=3, comments=True, type_hints=True)
    result1 = compress_to_phiton(source_code, config1)

    config2 = ConversionConfig(level=3, comments=False, type_hints=True)
    result2 = compress_to_phiton(source_code, config2)

    config3 = ConversionConfig(level=3, comments=True, type_hints=False)
    result3 = compress_to_phiton(source_code, config3)

    # Check that different configurations produce different outputs
    assert result1 != result2, (
        "Different comment settings should produce different outputs"
    )
    assert result1 != result3, (
        "Different type_hints settings should produce different outputs"
    )


def test_pattern_recognition():
    """Test that pattern recognition works correctly."""
    # Read the test file with common patterns
    source_code = read_file(TEST_DATA_DIR / "patterns.py")

    # Compress with pattern recognition
    config = ConversionConfig(level=4)
    result = compress_to_phiton(source_code, config)

    # Check for specific pattern replacements
    # List comprehension pattern
    assert "[x**2 for x in numbers]" not in result

    # Control flow pattern
    assert "if x is not None:" not in result

    # Function pattern
    assert "lambda x: x * 2" not in result


def test_syntax_error_handling():
    """Test that syntax errors are handled correctly."""
    # Invalid Python code
    invalid_code = """
    def invalid_function():
        return x +
    """

    # Check that compressing invalid code raises a SyntaxError
    with pytest.raises(SyntaxError):
        compress_to_phiton(invalid_code)
