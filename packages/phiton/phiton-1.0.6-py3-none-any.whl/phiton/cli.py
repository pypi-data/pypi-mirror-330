#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["fire", "rich", "loguru"]
# ///
# this_file: src/phiton/cli.py

"""Command-line interface for Phiton."""

import sys
from pathlib import Path

import fire
from loguru import logger
from rich.console import Console
from rich.table import Table

from phiton import __version__, dephitonize, phitonize
from phiton.config import ConversionConfig

console = Console(stderr=True)


def print_version() -> None:
    """Print the version information."""
    console.print(f"[bold blue]Phiton[/bold blue] version [green]{__version__}[/green]")


def print_stats(
    stats: dict[str, int | float], *, is_decompression: bool = False
) -> None:
    """Print compression statistics in a nice table.

    Args:
        stats: Dictionary with compression statistics
        is_decompression: Whether the stats are for decompression
    """
    operation = "Decompression" if is_decompression else "Compression"
    table = Table(title=f"{operation} Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Original Characters", str(stats["original_chars"]))
    table.add_row("Processed Characters", str(stats["compressed_chars"]))
    table.add_row("Original Lines", str(stats["original_lines"]))
    table.add_row("Processed Lines", str(stats["compressed_lines"]))
    table.add_row(f"{operation} Ratio", f"{stats['compression_ratio']:.2f}x")

    console.print(table)


def phiton(
    input_path: str | Path | None = None,
    output_path: str | Path | None = None,
    level: int = 5,
    *,
    comments: bool = True,
    type_hints: bool = True,
    minify: bool = True,
    symbols: bool = True,
    verbose: bool = False,
    decompress: bool = False,
) -> None:
    """Process Python or Phiton code.

    Args:
        input_path: Path to file or directory to process (stdin if not provided)
        output_path: Path to save the processed output (stdout if not provided)
        level: Compression level (1-5, where 5 is maximum compression)
        comments: Whether to preserve comments
        type_hints: Whether to preserve type hints
        minify: Whether to minify the code
        symbols: Whether to use symbol substitution
        verbose: Whether to print verbose output
        decompress: Whether to decompress Phiton to Python (default is to compress Python to Phiton)
    """

    config = ConversionConfig(
        comments=comments,
        type_hints=type_hints,
        minify=minify,
        symbols=symbols,
        level=level,
    )
    logger.remove()
    logger.add(sys.stderr, level="DEBUG" if verbose else "WARNING")

    phiton_func = dephitonize if decompress else phitonize

    if input_path:
        input_path = Path(input_path)
        source_code = input_path.read_text(encoding="utf-8")
    else:
        source_code = sys.stdin.read()

    if output_path:
        output_path = Path(output_path)

    result = phiton_func(source_code, config, verbose=verbose)
    if output_path:
        output_path.write_text(result["result"], encoding="utf-8")
        if verbose:
            console.print("\n")
            print_stats(result["stats"], is_decompression=decompress)
    else:
        sys.stdout.write(result["result"])


def main() -> None:
    """Main entry point for the CLI."""
    try:
        fire.Fire(phiton)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e!s}")
        sys.exit(1)


if __name__ == "__main__":
    main()
