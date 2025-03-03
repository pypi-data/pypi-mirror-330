#!/usr/bin/env python3
# this_file: tests/conftest.py
"""Configuration and fixtures for pytest."""

import sys
from pathlib import Path

import pytest

# Add the parent directory to sys.path to allow importing phiton
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))


# Create fixtures for common test resources
@pytest.fixture
def test_data_dir():
    """Return the path to the test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def expected_dir():
    """Return the path to the expected output directory."""
    return Path(__file__).parent / "data" / "expected"


@pytest.fixture
def simple_py_path(test_data_dir):
    """Return the path to the simple.py test file."""
    return test_data_dir / "simple.py"


@pytest.fixture
def complex_py_path(test_data_dir):
    """Return the path to the complex.py test file."""
    return test_data_dir / "complex.py"


@pytest.fixture
def patterns_py_path(test_data_dir):
    """Return the path to the patterns.py test file."""
    return test_data_dir / "patterns.py"


@pytest.fixture
def simple_py_content(simple_py_path):
    """Return the content of the simple.py test file."""
    with open(simple_py_path, encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def complex_py_content(complex_py_path):
    """Return the content of the complex.py test file."""
    with open(complex_py_path, encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def patterns_py_content(patterns_py_path):
    """Return the content of the patterns.py test file."""
    with open(patterns_py_path, encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def temp_output_dir(tmpdir):
    """Return a temporary directory for test output."""
    return Path(tmpdir) / "output"
