#!/usr/bin/env -S uv run -s
# /// script
# dependencies = []
# ///
# this_file: src/phiton/config.py

"""Configuration settings for Phiton conversion."""

from dataclasses import dataclass


@dataclass
class ConversionConfig:
    """Configuration settings for Phiton conversion."""

    comments: bool = True
    type_hints: bool = True
    minify: bool = True
    symbols: bool = True
    level: int = 5
