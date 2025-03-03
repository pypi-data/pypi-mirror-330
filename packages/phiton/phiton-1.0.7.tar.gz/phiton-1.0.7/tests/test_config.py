#!/usr/bin/env python3
# this_file: tests/test_config.py
"""Tests for the Phiton config module."""

from dataclasses import asdict

from phiton.config import ConversionConfig


def test_default_config():
    """Test that the default configuration has the expected values."""
    config = ConversionConfig()

    # Check default values
    assert config.comments is True
    assert config.type_hints is True
    assert config.minify is True
    assert config.symbols is True
    assert config.level == 5


def test_custom_config():
    """Test that custom configuration values are set correctly."""
    config = ConversionConfig(
        comments=False, type_hints=False, minify=False, symbols=False, level=2
    )

    # Check custom values
    assert config.comments is False
    assert config.type_hints is False
    assert config.minify is False
    assert config.symbols is False
    assert config.level == 2


def test_config_as_dict():
    """Test that the configuration can be converted to a dictionary."""
    config = ConversionConfig(
        comments=True, type_hints=False, minify=True, symbols=False, level=3
    )

    # Convert to dictionary
    config_dict = asdict(config)

    # Check dictionary values
    assert config_dict["comments"] is True
    assert config_dict["type_hints"] is False
    assert config_dict["minify"] is True
    assert config_dict["symbols"] is False
    assert config_dict["level"] == 3


def test_config_level_range():
    """Test that the level is constrained to the valid range."""
    # Test with level below minimum
    config = ConversionConfig(level=0)
    assert config.level == 5  # Should use default

    # Test with level above maximum
    config = ConversionConfig(level=6)
    assert config.level == 5  # Should use default

    # Test with valid levels
    for level in range(1, 6):
        config = ConversionConfig(level=level)
        assert config.level == level
