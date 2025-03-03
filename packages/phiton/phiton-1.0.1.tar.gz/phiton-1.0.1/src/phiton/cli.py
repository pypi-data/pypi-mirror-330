#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["fire", "rich", "loguru"]
# ///
# this_file: src/phiton/cli.py

"""Command-line interface for Phiton."""

import os
import sys

import fire
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax

from phiton import __version__, compress_file, compress_string
from phiton.config import ConversionConfig


console = Console()


def print_version() -> None:
    """Print the version information."""
    console.print(f"[bold blue]Phiton[/bold blue] version [green]{__version__}[/green]")


def print_stats(stats: dict[str, int | float]) -> None:
    """Print compression statistics in a nice table.

    Args:
        stats: Dictionary with compression statistics
    """
    table = Table(title="Compression Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Original Characters", str(stats["original_chars"]))
    table.add_row("Compressed Characters", str(stats["compressed_chars"]))
    table.add_row("Original Lines", str(stats["original_lines"]))
    table.add_row("Compressed Lines", str(stats["compressed_lines"]))
    table.add_row("Compression Ratio", f"{stats['compression_ratio']:.2f}x")

    console.print(table)


def compress(
    input_path: str,
    output_path: str | None = None,
    level: int = 5,
    comments: bool = True,
    type_hints: bool = True,
    minify: bool = True,
    symbols: bool = True,
    verbose: bool = False,
    preview: bool = False,
) -> None:
    """Compress Python code to Phiton notation.

    Args:
        input_path: Path to Python file or directory to compress
        output_path: Path to save the compressed output (defaults to input_path + '.phi')
        level: Compression level (1-5, where 5 is maximum compression)
        comments: Whether to preserve comments
        type_hints: Whether to preserve type hints
        minify: Whether to minify the code
        symbols: Whether to use symbol substitution
        verbose: Whether to print verbose output
        preview: Whether to preview the compressed code without saving
    """
    print_version()

    config = ConversionConfig(
        comments=comments,
        type_hints=type_hints,
        minify=minify,
        symbols=symbols,
        level=level,
    )

    if os.path.isfile(input_path):
        # Process a single file
        if preview:
            try:
                with open(input_path, encoding="utf-8") as f:
                    source_code = f.read()

                result = compress_string(source_code, config, verbose)

                console.print("\n[bold]Original Code:[/bold]")
                console.print(Panel(Syntax(source_code, "python", line_numbers=True)))

                console.print("\n[bold]Compressed Code:[/bold]")
                console.print(Panel(result["result"]))

                print_stats(result["stats"])

            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e!s}")
                sys.exit(1)
        else:
            try:
                stats = compress_file(input_path, output_path, config, verbose)
                print_stats(stats)
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e!s}")
                sys.exit(1)

    elif os.path.isdir(input_path):
        # Process a directory
        if output_path and not os.path.isdir(output_path):
            try:
                os.makedirs(output_path)
            except Exception as e:
                console.print(
                    f"[bold red]Error creating output directory:[/bold red] {e!s}"
                )
                sys.exit(1)

        python_files = []
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))

        if not python_files:
            console.print(f"[yellow]No Python files found in {input_path}[/yellow]")
            return

        console.print(
            f"[blue]Found {len(python_files)} Python files to compress[/blue]"
        )

        total_stats: dict[str, int | float] = {
            "original_chars": 0,
            "compressed_chars": 0,
            "original_lines": 0,
            "compressed_lines": 0,
            "compression_ratio": 0.0,
        }

        for py_file in python_files:
            rel_path = os.path.relpath(py_file, input_path)

            if output_path:
                out_file = os.path.join(output_path, rel_path + ".phi")
                os.makedirs(os.path.dirname(out_file), exist_ok=True)
            else:
                out_file = py_file + ".phi"

            try:
                stats = compress_file(py_file, out_file, config, verbose)

                # Accumulate stats
                for key in [
                    "original_chars",
                    "compressed_chars",
                    "original_lines",
                    "compressed_lines",
                ]:
                    total_stats[key] = total_stats[key] + stats[key]

                console.print(
                    f"[green]✓[/green] {rel_path} → {os.path.basename(out_file)}"
                )

            except Exception as e:
                console.print(f"[red]✗[/red] {rel_path}: {e!s}")

        # Calculate overall compression ratio
        if total_stats["original_chars"] > 0:
            total_stats["compression_ratio"] = float(
                total_stats["original_chars"]
            ) / float(total_stats["compressed_chars"])
            console.print("\n[bold]Overall Compression Statistics:[/bold]")
            print_stats(total_stats)

    else:
        console.print(f"[bold red]Error:[/bold red] {input_path} does not exist")
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    try:
        fire.Fire(
            {
                "compress": compress,
                "version": print_version,
            }
        )
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e!s}")
        sys.exit(1)


if __name__ == "__main__":
    main()
