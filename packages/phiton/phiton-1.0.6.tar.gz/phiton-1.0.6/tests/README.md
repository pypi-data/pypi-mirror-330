# Phiton Tests

This directory contains tests for the Phiton package.

## Test Structure

- `conftest.py`: Contains pytest fixtures and configuration
- `test_*.py`: Test files for different modules
- `data/`: Contains test data files
  - `simple.py`: A simple Python file for testing basic functionality
  - `complex.py`: A more complex Python file for testing advanced features
  - `patterns.py`: A Python file with common patterns for testing pattern recognition
  - `expected/`: Contains expected output files for comparison

## Running Tests

To run the tests, you need to install the test dependencies:

```bash
pip install -r tests/requirements.txt
```

Then, from the project root directory, run:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=phiton
```

To run a specific test file:

```bash
pytest tests/test_converter.py
```

To run a specific test function:

```bash
pytest tests/test_converter.py::test_compress_simple_level1
```

## Adding New Tests

When adding new tests:

1. Add test data files to the `data/` directory
2. Add expected output files to the `data/expected/` directory
3. Create test functions in the appropriate test file
4. Use fixtures from `conftest.py` where possible

## Test Coverage

The tests aim to cover:

- Configuration options
- Compression functionality
- Utility functions
- CLI commands
- Error handling 