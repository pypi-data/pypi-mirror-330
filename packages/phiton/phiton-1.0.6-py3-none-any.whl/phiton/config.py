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

    def __post_init__(self):
        """Validate the configuration parameters after initialization."""
        # Ensure level is between 1 and 5
        if self.level < 1 or self.level > 5:
            self.level = 5  # Reset to default if out of range
