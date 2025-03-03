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
from typing import Any

from loguru import logger

# Import version
try:
    from phiton.__version__ import __version__, version
except ImportError:
    __version__ = "0.0.0"
    version = "0.0.0"

# Import core components
from phiton.config import ConversionConfig
from phiton.dephitonize import dephitonize_phiton
from phiton.phitonize import phitonize_python
from phiton.utils import calculate_stats, optimize_final

__all__ = [
    "ConversionConfig",
    "__version__",
    "calculate_stats",
    "dephitonize_phiton",
    "optimize_final",
    "phitonize_python",
    "version",
]


def phitonize(
    source_code: str, config: ConversionConfig | None = None, *, verbose: bool = False
) -> dict[str, Any]:
    """Compress a Python string to Phiton notation.

    Args:
        source_code: The Python source code to compress
        config: Configuration options for the compression
        verbose: Whether to print verbose output

    Returns:
        A dictionary containing the compressed code and statistics
    """
    if config is None:
        config = ConversionConfig()

    # Process the source code
    result = phitonize_python(source_code, config)

    # Calculate statistics
    stats = calculate_stats(source_code, result)

    # Log statistics if verbose
    if verbose:
        logger.debug(f"Original characters: {stats['original_chars']}")
        logger.debug(f"Compressed characters: {stats['compressed_chars']}")
        logger.debug(f"Compression ratio: {stats['compression_ratio']:.2f}x")

    return {
        "result": result,
        "stats": stats,
    }


def dephitonize(
    phiton_code: str, config: ConversionConfig | None = None, *, verbose: bool = False
) -> dict[str, Any]:
    """Decompress a Phiton string to Python notation.

    Args:
        phiton_code: The Phiton code to decompress
        config: Configuration options for the decompression
        verbose: Whether to print verbose output

    Returns:
        A dictionary containing the decompressed code and statistics
    """
    if config is None:
        config = ConversionConfig()

    # Process the Phiton code
    result = dephitonize_phiton(phiton_code, config)

    # Calculate statistics
    stats = calculate_stats(phiton_code, result)

    # Log statistics if verbose
    if verbose:
        logger.debug(f"Original characters: {stats['original_chars']}")
        logger.debug(f"Decompressed characters: {stats['compressed_chars']}")
        logger.debug(f"Decompression ratio: {stats['compression_ratio']:.2f}x")

    return {
        "result": result,
        "stats": stats,
    }
