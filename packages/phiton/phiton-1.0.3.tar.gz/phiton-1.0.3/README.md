# Phiton

Phiton is a Python code compressor that converts standard Python code into a more concise notation using mathematical symbols and advanced compression techniques.

For example, this Python code:
```python
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)
```

Can be compressed to:
```
ƒfactorialn⟨⋔n≤#1⟨⇐#1⟩⋮⇐n*factorialn-#1⟩
```

## Features

- Convert Python code to a compressed symbolic notation
- Adjustable compression levels (1-5)
- Preserve comments and type hints (optional)
- Command-line interface with rich output
- Support for processing individual files or entire directories
- Detailed compression statistics

## Installation

Using pip:
```bash
pip install phiton
```

Using uv (recommended for faster installation):
```bash
uv pip install phiton
```

Or install directly from the repository:

```bash
pip install git+https://github.com/twardoch/phiton.git
```

For development, you can install with extras:

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Install with testing dependencies
pip install -e ".[test]"

# Install with all dependencies
pip install -e ".[all]"
```

## Usage

### Command Line

Compress a Python file:

```bash
python -m phiton example.py
```

Read from stdin and write to stdout:

```bash
cat example.py | python -m phiton > example.phi
```

Preview compression without saving:

```bash
python -m phiton example.py --preview
```

Compress with specific options:

```bash
python -m phiton example.py --level=3 --comments=False --type-hints=False
```

Compress an entire directory:

```bash
python -m phiton my_project/ --output-path=compressed/
```

Show version:

```bash
python -m phiton version
```

### Python API

```python
from phiton import compress_string, compress_file, ConversionConfig

# Basic usage
result = compress_string("def hello(name: str) -> str:\n    return f'Hello, {name}!'")
print(result["result"])  # Compressed code
print(result["stats"])   # Compression statistics

# With custom configuration
config = ConversionConfig(
    level=3,             # Compression level (1-5)
    comments=False,      # Don't preserve comments
    type_hints=True,     # Preserve type hints
    minify=True,         # Minify the code
    symbols=True,        # Use symbol substitution
)
result = compress_string("def hello(name: str) -> str:\n    return f'Hello, {name}!'", config)

# a file
stats = compress_file("example.py", "example.phi", config)
```

## Compression Levels

Phiton offers 5 compression levels:

1. **Basic**: Minimal symbol substitution, preserves structure and readability
2. **Moderate**: More symbol substitutions while maintaining readability
3. **Standard**: Full symbol substitution with some structure preservation
4. **High**: Aggressive symbol substitution and minimal structure
5. **Maximum**: Highest compression with shortest possible representation

## Symbol Examples

| Python | Phiton | Description |
|--------|--------|-------------|
| `def`  | `ƒ`    | Function definition |
| `return` | `⇐`  | Return statement |
| `if`   | `⋔`    | Conditional |
| `for`  | `∀`    | For loop |
| `in`   | `∈`    | Membership test |
| `None` | `∅`    | None value |
| `True` | `⊤`    | True value |
| `False` | `⊥`   | False value |
| `and`  | `∧`    | Logical AND |
| `or`   | `∨`    | Logical OR |
| `not`  | `¬`    | Logical NOT |
| `==`   | `≡`    | Equality |
| `!=`   | `≠`    | Inequality |
| `<=`   | `≤`    | Less than or equal |
| `>=`   | `≥`    | Greater than or equal |
| `=`    | `≔`    | Assignment |

## Project Structure

```
phiton/
├── examples/           # Example files for testing
├── src/
│   └── phiton/         # Main package
│       ├── __init__.py # Package entry point
│       ├── __main__.py # CLI entry point
│       ├── cli.py      # Command-line interface
│       ├── config.py   # Configuration dataclass
│       ├── constants.py # Symbol mappings
│       ├── converter.py # Core conversion logic
│       └── utils.py    # Utility functions
└── tests/              # Test suite
    ├── data/           # Test data files
    ├── test_cli.py     # CLI tests
    ├── test_config.py  # Configuration tests
    ├── test_converter.py # Converter tests
    └── test_utils.py   # Utility tests
```

## Development

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/twardoch/phiton.git
   cd phiton
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev,test]"
   ```

### Testing

Run the tests:
```bash
python -m pytest
```

Run with coverage:
```bash
python -m pytest --cov=src/phiton
```

### Linting

Run the linter:
```bash
ruff check .
```

Fix linting issues:
```bash
ruff check --fix --unsafe-fixes .
```

Format the code:
```bash
ruff format .
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 