#!/usr/bin/env -S uv run -s
# /// script
# dependencies = []
# ///
# this_file: src/phiton/utils.py

"""Utility functions for Phiton conversion."""

import ast
import re

from phiton.constants import COMMON_SUBEXPRESSIONS, DOMAIN_PREFIXES


def optimize_imports(tree: ast.AST) -> list[str]:
    """Optimize and combine imports.

    Args:
        tree: AST tree of the Python code

    Returns:
        List of optimized import statements
    """
    imports = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports[alias.name] = alias.asname or alias.name
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports[f"{module}.{alias.name}"] = alias.asname or alias.name

    # Group imports by domain
    domain_imports = {}
    for imp, alias in imports.items():
        for domain in DOMAIN_PREFIXES:
            if imp.startswith(domain):
                if domain not in domain_imports:
                    domain_imports[domain] = []
                domain_imports[domain].append((imp, alias))
                break

    # Generate optimized import statements
    result = []
    for domain, imps in domain_imports.items():
        if len(imps) > 1:
            # Combine multiple imports from same domain
            names = [
                f"{i[0].split('.')[-1]} as {i[1]}"
                if i[0] != i[1]
                else i[0].split(".")[-1]
                for i in imps
            ]
            result.append(f"from {domain} import {', '.join(names)}")
        else:
            imp, alias = imps[0]
            if imp == alias:
                result.append(f"import {imp}")
            else:
                result.append(f"import {imp} as {alias}")

    return result


def optimize_final(code: str, level: int) -> str:
    """Apply final optimizations based on compression level.

    Args:
        code: Phiton code to optimize
        level: Compression level (1-5)

    Returns:
        Optimized Phiton code

    Level 1: Basic symbol substitution, preserve structure
    Level 2: Remove redundant whitespace, combine simple operations
    Level 3: Replace common subexpressions, optimize imports
    Level 4: Aggressive whitespace removal, symbol renaming
    Level 5: Maximum compression, shortest possible representation
    """
    # Level 1: Basic symbol substitution only
    if level < 2:
        # Preserve structure but apply basic symbol mappings
        return re.sub(r"\s+", " ", code)  # Normalize whitespace

    # Level 2: Remove redundant whitespace, combine simple operations
    if level < 3:
        code = re.sub(r"\s+", " ", code)  # Normalize but preserve some whitespace
        return re.sub(r"→\s*→", "→", code)  # Combine arrows

    # Level 3: Replace common subexpressions, optimize imports
    if level < 4:
        # Replace common subexpressions while preserving some readability
        for pattern, replacement in COMMON_SUBEXPRESSIONS.items():
            code = code.replace(pattern, replacement)
        code = re.sub(r"\s+", " ", code)  # Keep single spaces
        return re.sub(r"→\s*→", "→", code)

    # Level 4: Aggressive whitespace removal, symbol renaming
    if level < 5:
        for pattern, replacement in COMMON_SUBEXPRESSIONS.items():
            code = code.replace(pattern, replacement)
        code = re.sub(r"\s+", "", code)  # Remove all whitespace
        code = re.sub(
            r"\(\s*([^,()]+)\s*\)", r"\1", code
        )  # Remove unnecessary parentheses

        # Use shorter names for local symbols
        used_symbols = set(re.findall(r"§(\w+)", code))
        symbol_map = {sym: f"_{i}" for i, sym in enumerate(sorted(used_symbols))}
        for old, new in symbol_map.items():
            code = code.replace(f"§{old}", f"§{new}")

        return code

    # Level 5: Maximum compression
    # Replace common subexpressions
    for pattern, replacement in COMMON_SUBEXPRESSIONS.items():
        code = code.replace(pattern, replacement)

    # Remove all unnecessary characters
    code = re.sub(r"\s+", "", code)
    code = re.sub(r"\(\s*([^,()]+)\s*\)", r"\1", code)
    code = re.sub(r"→\s*→", "→", code)

    # Use shortest possible names for local symbols
    used_symbols = set(re.findall(r"§(\w+)", code))
    symbol_map = {sym: chr(ord("a") + i) for i, sym in enumerate(sorted(used_symbols))}
    for old, new in symbol_map.items():
        code = code.replace(f"§{old}", f"§{new}")

    # Combine repeated operations
    code = re.sub(r"(⊕|⊖|△|▽|◊|◆)\1+", r"\1", code)

    # Use shortest form for common patterns
    replacements = {
        "⋔⊤⟨": "⊤⟨",  # if True:
        "⋔⊥⟨": "⊥⟨",  # if False:
        "⋔∅⟨": "∅⟨",  # if None:
        "⇐⊤": "⇐⊤",  # return True
        "⇐⊥": "⇐⊥",  # return False
        "⇐∅": "⇐∅",  # return None
        "≔∅": "∅",  # = None
        "≔⊤": "⊤",  # = True
        "≔⊥": "⊥",  # = False
    }
    for pattern, repl in replacements.items():
        code = code.replace(pattern, repl)

    return code


def calculate_stats(source: str, result: str) -> dict[str, int | float]:
    """Calculate compression statistics.

    Args:
        source: Original Python code
        result: Converted Phiton code

    Returns:
        Dictionary with compression statistics
    """
    return {
        "original_chars": len(source),
        "compressed_chars": len(result),
        "original_lines": len(source.splitlines()),
        "compressed_lines": len(result.splitlines()),
        "compression_ratio": round(len(result) / len(source) * 100, 2),
    }
