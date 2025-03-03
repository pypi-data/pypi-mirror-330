#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["loguru"]
# ///
# this_file: src/phiton/__init__.py

"""
Phiton: A Python code compressor that converts Python to a more concise notation.

Phiton converts standard Python code into a compressed form using mathematical symbols
and advanced compression techniques. The goal is to create the most compact representation
of Python code while maintaining the ability to convert back to standard Python.
"""

import sys
from typing import Dict, Optional, Union, Any

from loguru import logger

# Configure loguru
logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

# Import version
try:
    from phiton.__version__ import __version__, version
except ImportError:
    __version__ = "0.0.0"
    version = "0.0.0"

# Import core components
from phiton.config import ConversionConfig
from phiton.converter import compress_to_phiton
from phiton.utils import calculate_stats, optimize_final

__all__ = [
    "ConversionConfig",
    "__version__",
    "calculate_stats",
    "compress_file",
    "compress_string",
    "compress_to_phiton",
    "optimize_final",
    "version",
]


def compress_file(
    input_file: str,
    output_file: str | None = None,
    config: ConversionConfig | None = None,
    verbose: bool = False,
) -> dict[str, int | float]:
    """Compress a Python file to Phiton notation.

    Args:
        input_file: Path to the Python file to compress
        output_file: Path to save the compressed Phiton code (defaults to input_file + '.phi')
        config: Optional conversion configuration
        verbose: Whether to print verbose output

    Returns:
        Dictionary with compression statistics

    Raises:
        FileNotFoundError: If input file doesn't exist
        PermissionError: If output file can't be written
        SyntaxError: If input Python code is invalid
    """
    if verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.remove()
        logger.add(sys.stderr, level="INFO")

    if config is None:
        config = ConversionConfig()

    if output_file is None:
        output_file = f"{input_file}.phi"

    logger.info(f"Compressing {input_file} to {output_file}")
    logger.debug(f"Using compression level: {config.level}")

    try:
        with open(input_file, encoding="utf-8") as f:
            source_code = f.read()
    except FileNotFoundError:
        logger.error(f"Input file not found: {input_file}")
        raise
    except Exception as e:
        logger.error(f"Error reading input file: {e!s}")
        raise

    try:
        result = compress_to_phiton(source_code, config)
    except SyntaxError:
        logger.error(f"Invalid Python syntax in {input_file}")
        raise
    except Exception as e:
        logger.error(f"Error during compression: {e!s}")
        raise

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
    except PermissionError:
        logger.error(f"Permission denied when writing to {output_file}")
        raise
    except Exception as e:
        logger.error(f"Error writing output file: {e!s}")
        raise

    stats = calculate_stats(source_code, result)

    logger.info(
        f"Compression complete: {stats['original_chars']} → {stats['compressed_chars']} chars"
    )
    logger.info(f"Compression ratio: {stats['compression_ratio']:.2f}x")

    return stats


def compress_string(
    source_code: str, config: ConversionConfig | None = None, verbose: bool = False
) -> dict[str, Any]:
    """Compress a Python string to Phiton notation.

    Args:
        source_code: Python source code to compress
        config: Optional conversion configuration
        verbose: Whether to print verbose output

    Returns:
        Dictionary with compressed code and statistics

    Raises:
        SyntaxError: If input Python code is invalid
    """
    if verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.remove()
        logger.add(sys.stderr, level="INFO")

    if config is None:
        config = ConversionConfig()

    logger.debug(f"Using compression level: {config.level}")

    try:
        result = compress_to_phiton(source_code, config)
    except SyntaxError:
        logger.error("Invalid Python syntax in input string")
        raise
    except Exception as e:
        logger.error(f"Error during compression: {e!s}")
        raise

    stats = calculate_stats(source_code, result)

    logger.info(
        f"Compression complete: {stats['original_chars']} → {stats['compressed_chars']} chars"
    )
    logger.info(f"Compression ratio: {stats['compression_ratio']:.2f}x")

    return {
        "result": result,
        "stats": stats,
    }
