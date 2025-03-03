#!/usr/bin/env -S uv run -s
# /// script
# dependencies = []
# ///
# this_file: src/phiton/__main__.py

"""Entry point for running the package as a module."""

from phiton.cli import main

if __name__ == "__main__":
    main()
