#!/usr/bin/env python3
# this_file: tests/test_cli.py
"""Tests for the Phiton CLI module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from phiton.cli import phiton, print_version

# Get the path to the test data directory
TEST_DATA_DIR = Path(__file__).parent / "data"


def test_print_version(capsys):
    """Test that print_version outputs the version correctly."""
    # Call the print_version function
    print_version()

    # Capture the output
    captured = capsys.readouterr()

    # Check that the output contains "Phiton" and "version"
    # The output is going to stderr because we're using rich.console with stderr=True
    assert "Phiton" in captured.err
    assert "version" in captured.err


def test_compress_file():
    """Test compressing a single file with the CLI."""
    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up paths
        input_file = TEST_DATA_DIR / "simple.py"
        output_file = Path(temp_dir) / "simple.phi"

        # Call the phiton function with decompress=False
        with patch(
            "sys.argv",
            ["phiton", str(input_file), "--output-path", str(output_file)],
        ):
            phiton(
                input_path=str(input_file),
                output_path=str(output_file),
                level=3,
                verbose=False,
                decompress=False,
            )

        # Check that the output file was created
        assert output_file.exists()

        # Check that the output file has content
        with open(output_file, encoding="utf-8") as f:
            content = f.read()
            assert len(content) > 0
            assert "ƒ" in content  # Check for Phiton symbols


def test_compress_preview(capsys):
    """Test the preview option of the compress command."""
    # Set up paths
    input_file = TEST_DATA_DIR / "simple.py"

    # Call the phiton function with preview=True and decompress=False
    with patch("sys.argv", ["phiton", str(input_file)]):
        # Since preview is no longer a parameter, we'll capture stdout instead
        phiton(
            input_path=str(input_file),
            level=3,
            verbose=False,
            decompress=False,
        )

    # Capture the output
    captured = capsys.readouterr()

    # Check that the output contains Phiton symbols
    assert "ƒ" in captured.out  # Check for Phiton symbols


def test_compress_with_options():
    """Test compressing a file with different options."""
    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up paths
        input_file = TEST_DATA_DIR / "simple.py"
        output_file1 = Path(temp_dir) / "simple_level1.phi"
        output_file5 = Path(temp_dir) / "simple_level5.phi"

        # Compress with level 1
        with patch(
            "sys.argv",
            [
                "phiton",
                str(input_file),
                "--output-path",
                str(output_file1),
                "--level",
                "1",
            ],
        ):
            phiton(
                input_path=str(input_file),
                output_path=str(output_file1),
                level=1,
                decompress=False,
            )

        # Compress with level 5
        with patch(
            "sys.argv",
            [
                "phiton",
                str(input_file),
                "--output-path",
                str(output_file5),
                "--level",
                "5",
            ],
        ):
            phiton(
                input_path=str(input_file),
                output_path=str(output_file5),
                level=5,
                decompress=False,
            )

        # Check that both output files exist
        assert output_file1.exists()
        assert output_file5.exists()

        # Read the content of both files
        with open(output_file1, encoding="utf-8") as f:
            content1 = f.read()

        with open(output_file5, encoding="utf-8") as f:
            content5 = f.read()

        # Check that level 5 produces more compressed output
        assert len(content5) <= len(content1), (
            "Level 5 should produce more compressed output than level 1"
        )


def test_compress_directory():
    """Test compressing a directory with the CLI."""
    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up paths
        input_dir = TEST_DATA_DIR
        output_dir = Path(temp_dir) / "output"
        output_dir.mkdir(exist_ok=True)

        # Since the CLI doesn't directly support directory processing anymore,
        # we'll test individual files instead
        input_files = ["simple.py", "complex.py", "patterns.py"]

        for input_file in input_files:
            input_path = input_dir / input_file
            output_path = output_dir / f"{input_file}.phi"

            # Call the phiton function for each file
            phiton(
                input_path=str(input_path),
                output_path=str(output_path),
                level=3,
                decompress=False,
            )

        # Check that the output files were created
        assert (output_dir / "simple.py.phi").exists()
        assert (output_dir / "complex.py.phi").exists()
        assert (output_dir / "patterns.py.phi").exists()
