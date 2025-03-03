#!/usr/bin/env python3
# this_file: tests/test_cli.py
"""Tests for the Phiton CLI module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from phiton.cli import compress, print_version


# Get the path to the test data directory
TEST_DATA_DIR = Path(__file__).parent / "data"


def test_print_version(capsys):
    """Test that print_version outputs the version correctly."""
    # Call the print_version function
    print_version()

    # Capture the output
    captured = capsys.readouterr()

    # Check that the output contains "Phiton" and "version"
    assert "Phiton" in captured.out
    assert "version" in captured.out


def test_compress_file():
    """Test compressing a single file with the CLI."""
    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up paths
        input_file = TEST_DATA_DIR / "simple.py"
        output_file = Path(temp_dir) / "simple.phi"

        # Call the compress function
        with patch(
            "sys.argv",
            ["phiton", "compress", str(input_file), "--output-path", str(output_file)],
        ):
            compress(
                input_path=str(input_file),
                output_path=str(output_file),
                level=3,
                verbose=False,
                preview=False,
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

    # Call the compress function with preview=True
    with patch("sys.argv", ["phiton", "compress", str(input_file), "--preview"]):
        compress(input_path=str(input_file), preview=True, level=3, verbose=False)

    # Capture the output
    captured = capsys.readouterr()

    # Check that the output contains "Original Code" and "Compressed Code"
    assert "Original Code" in captured.out
    assert "Compressed Code" in captured.out
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
                "compress",
                str(input_file),
                "--output-path",
                str(output_file1),
                "--level",
                "1",
            ],
        ):
            compress(
                input_path=str(input_file),
                output_path=str(output_file1),
                level=1,
                verbose=False,
                preview=False,
            )

        # Compress with level 5
        with patch(
            "sys.argv",
            [
                "phiton",
                "compress",
                str(input_file),
                "--output-path",
                str(output_file5),
                "--level",
                "5",
            ],
        ):
            compress(
                input_path=str(input_file),
                output_path=str(output_file5),
                level=5,
                verbose=False,
                preview=False,
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

        # Call the compress function with a directory
        with patch(
            "sys.argv",
            ["phiton", "compress", str(input_dir), "--output-path", str(output_dir)],
        ):
            compress(
                input_path=str(input_dir),
                output_path=str(output_dir),
                level=3,
                verbose=False,
                preview=False,
            )

        # Check that the output directory was created
        assert output_dir.exists()

        # Check that output files were created for Python files in the input directory
        assert (output_dir / "simple.py.phi").exists()
        assert (output_dir / "complex.py.phi").exists()
        assert (output_dir / "patterns.py.phi").exists()
