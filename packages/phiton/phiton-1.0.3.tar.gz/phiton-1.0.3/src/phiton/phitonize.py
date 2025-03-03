#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["loguru"]
# ///
# this_file: src/phiton/phitonize.py

"""Python to Phiton conversion functionality."""

import ast
import re
from collections.abc import Sequence

from loguru import logger

from phiton.config import ConversionConfig
from phiton.constants import (ADVANCED_PATTERNS, DOMAIN_PREFIXES,
                              PATTERN_REPLACEMENTS, PYTHON_TO_PHITON)
from phiton.utils import optimize_final, optimize_imports


def phitonize_python(source_code: str, config: ConversionConfig | None = None) -> str:
    """Convert Python code to Phiton notation with enhanced compression.

    Args:
        source_code: Python source code to convert
        config: Optional conversion configuration

    Returns:
        Converted Phiton code with maximum compression

    Raises:
        SyntaxError: If input Python code is invalid
    """
    if config is None:
        config = ConversionConfig()

    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        logger.error("Invalid Python syntax: %s", str(e))
        raise

    # Initialize tracking structures
    symbol_table: dict[str, str] = {}
    expr_freq: dict[str, int] = {}
    scope_stack: list[dict[str, str]] = [{}]

    # Optimize imports first
    if config.level >= 3:
        optimized_imports = optimize_imports(tree)
        for imp in optimized_imports:
            symbol_table[imp] = f"§{len(symbol_table)}"

    def get_pattern_key(node: ast.AST) -> str | None:
        """Get a key for pattern matching if the node matches a common pattern."""
        if isinstance(node, ast.If):
            # Handle common if patterns
            test_str = ast.unparse(node.test)
            body_str = ast.unparse(node.body[0]) if node.body else ""
            pattern = f"{test_str}: {body_str}"
            return pattern if pattern in PATTERN_REPLACEMENTS else None
        elif isinstance(node, ast.ListComp):
            # Handle list comprehension patterns
            return ast.unparse(node)
        return None

    def should_create_symbol(expr: str, freq: int) -> bool:
        """Determine if an expression should be assigned to a local symbol."""
        return (
            freq > 2  # Used more than twice
            and len(expr) > 10  # Long enough to benefit from compression
            and not expr.startswith("§")  # Not already a symbol
            and not any(c in expr for c in "⟨⟩→")  # Not a complex expression
        )

    def get_next_symbol_name() -> str:
        """Generate the next available symbol name."""
        used_names = set().union(*scope_stack)
        for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if c not in used_names:
                return c
        # If single chars exhausted, use numbered symbols
        i = 0
        while f"_{i}" in used_names:
            i += 1
        return f"_{i}"

    def optimize_expression(expr: str) -> str:
        """Apply additional compression optimizations to an expression."""
        # Remove unnecessary parentheses
        expr = re.sub(r"\(\s*([^,()]+)\s*\)", r"\1", expr)
        # Compress whitespace
        expr = re.sub(r"\s+", "", expr)
        # Apply common patterns
        for pattern, replacement in PATTERN_REPLACEMENTS.items():
            if pattern in expr:
                expr = expr.replace(pattern, replacement)
        return expr

    def detect_advanced_pattern(node: ast.AST) -> str | None:
        """Detect if a node matches an advanced pattern."""
        node_str = ast.unparse(node)
        for pattern, replacement in ADVANCED_PATTERNS.items():
            if pattern in node_str:
                return replacement
        return None

    def phitonize_node(node: ast.AST | None) -> str:
        """Convert an AST node to Phiton notation with enhanced compression.

        The compression level affects how aggressively we convert nodes:
        Level 1: Basic conversion with readable symbols and preserved structure
        Level 2: More symbol substitutions but maintain readability
        Level 3: Full symbol substitution with some structure preservation
        Level 4: Aggressive symbol substitution and minimal structure
        Level 5: Maximum compression with shortest possible representation
        """
        if node is None:
            return ""

        # Handle Module node specially
        if isinstance(node, ast.Module):
            return phitonize_body(node.body)

        # Check for advanced patterns first
        if config.level >= 3 and (pattern := detect_advanced_pattern(node)):
            return pattern

        # Check for pattern matches first
        if config.level >= 2 and (pattern_key := get_pattern_key(node)):
            if pattern_key in PATTERN_REPLACEMENTS:
                return PATTERN_REPLACEMENTS[pattern_key]

        # Track expression frequency for higher compression levels
        if config.level >= 3:
            try:
                expr = ast.unparse(node) if isinstance(node, ast.expr) else ""
                if expr:
                    expr_freq[expr] = expr_freq.get(expr, 0) + 1
            except Exception:
                # Skip if unparsing fails
                pass

        if isinstance(node, ast.FunctionDef):
            scope_stack.append({})  # New scope
            args = phitonize_arguments(node.args)
            body = phitonize_body(node.body)
            decorators = "".join(phitonize_node(d) for d in node.decorator_list)
            returns = f"⦂⟮{phitonize_node(node.returns)}⟯" if node.returns else ""
            scope_stack.pop()  # End scope

            # More readable format for lower compression levels
            if config.level <= 2:
                return f"{decorators}def {node.name}({args}){returns}:\n{body}"
            return f"{decorators}ƒ{node.name}({args}){returns}⟨{body}⟩"

        elif isinstance(node, ast.Name):
            # Handle special constants based on compression level
            if node.id == "None":
                return "None" if config.level <= 2 else "∅"
            elif node.id == "True":
                return "True" if config.level <= 2 else "⊤"
            elif node.id == "False":
                return "False" if config.level <= 2 else "⊥"

            # Check for domain-specific prefixes at higher levels
            if config.level >= 3 and node.id in DOMAIN_PREFIXES:
                return DOMAIN_PREFIXES[node.id]

            # Check for local symbol definitions at higher levels
            if config.level >= 3 and config.symbols and node.id in symbol_table:
                return f"§{symbol_table[node.id]}"

            return node.id

        elif isinstance(node, ast.Constant):
            if node.value is None:
                return "None" if config.level <= 2 else "∅"
            elif node.value is True:
                return "True" if config.level <= 2 else "⊤"
            elif node.value is False:
                return "False" if config.level <= 2 else "⊥"
            elif isinstance(node.value, str):
                if config.level >= 3:
                    return f"${node.value}"
                return repr(node.value)
            elif isinstance(node.value, int | float):
                if config.level >= 3:
                    return f"#{node.value}"
                return str(node.value)
            return repr(node.value)

        elif isinstance(node, ast.Return):
            value = phitonize_node(node.value) if node.value else ""
            if config.level <= 2:
                return f"return {value}"
            return f"⇐{value}"

        elif isinstance(node, ast.If):
            test = phitonize_node(node.test)
            body = phitonize_body(node.body)
            orelse = phitonize_body(node.orelse) if node.orelse else ""

            if config.level <= 2:
                result = f"if {test}:\n{body}"
                if orelse:
                    result += f"\nelse:\n{orelse}"
                return result
            return f"⋔{test}⟨{body}⟩{f'⋮{orelse}' if orelse else ''}"

        elif isinstance(node, ast.Call):
            func = phitonize_node(node.func)
            args = [phitonize_node(arg) for arg in node.args]
            kwargs = [f"{kw.arg}={phitonize_node(kw.value)}" for kw in node.keywords]
            all_args = ",".join(filter(None, [",".join(args), ",".join(kwargs)]))

            # Handle domain-specific library calls at higher levels
            if config.level >= 3:
                if isinstance(node.func, ast.Attribute) and isinstance(
                    node.func.value, ast.Name
                ):
                    lib_name = node.func.value.id
                    if lib_name in DOMAIN_PREFIXES:
                        return (
                            f"{DOMAIN_PREFIXES[lib_name]}·{node.func.attr}({all_args})"
                        )

                # Handle common function patterns
                if func in PYTHON_TO_PHITON:
                    return f"{PYTHON_TO_PHITON[func]}({all_args})"

            return f"{func}({all_args})"

        elif isinstance(node, ast.AsyncFunctionDef):
            args = phitonize_arguments(node.args)
            body = phitonize_body(node.body)
            decorators = "".join(phitonize_node(d) for d in node.decorator_list)
            returns = f"⦂⟮{phitonize_node(node.returns)}⟯" if node.returns else ""
            return f"{decorators}⊡ƒ{node.name}({args}){returns}⟨{body}⟩"

        elif isinstance(node, ast.ClassDef):
            bases = ",".join(phitonize_node(b) for b in node.bases)
            body = phitonize_body(node.body)
            decorators = "".join(phitonize_node(d) for d in node.decorator_list)
            return f"{decorators}Σ{node.name}({bases})⟨{body}⟩"

        elif isinstance(node, ast.Yield):
            value = phitonize_node(node.value) if node.value else ""
            return f"↥{value}"

        elif isinstance(node, ast.YieldFrom):
            value = phitonize_node(node.value)
            return f"↥⋮{value}"

        elif isinstance(node, ast.For):
            target = phitonize_node(node.target)
            iter = phitonize_node(node.iter)
            body = phitonize_body(node.body)
            orelse = f"⋮{phitonize_body(node.orelse)}" if node.orelse else ""
            return f"∀{target}∈{iter}⟨{body}⟩{orelse}"

        elif isinstance(node, ast.While):
            test = phitonize_node(node.test)
            body = phitonize_body(node.body)
            orelse = f"⋮{phitonize_body(node.orelse)}" if node.orelse else ""
            return f"⟳{test}⟨{body}⟩{orelse}"

        elif isinstance(node, ast.ExceptHandler):
            type = phitonize_node(node.type) if node.type else ""
            name = f" as {node.name}" if node.name else ""
            body = phitonize_body(node.body)
            return f"⋔{type}{name}⟨{body}⟩"

        elif isinstance(node, ast.With):
            items = ",".join(phitonize_node(item) for item in node.items)
            body = phitonize_body(node.body)
            return f"⊢⊣{items}⟨{body}⟩"

        elif isinstance(node, ast.Match):
            subject = phitonize_node(node.subject)
            cases = "".join(phitonize_node(case) for case in node.cases)
            return f"↦{subject}⟨{cases}⟩"

        elif isinstance(node, ast.match_case):
            pattern = phitonize_match_pattern(node.pattern)
            guard = f"⋔{phitonize_node(node.guard)}" if node.guard else ""
            body = phitonize_body(node.body)
            return f"≐{pattern}{guard}⟨{body}⟩"

        elif isinstance(node, ast.BinOp):
            left = phitonize_node(node.left)
            right = phitonize_node(node.right)
            op = phitonize_operator(node.op)
            return f"{left}{op}{right}"

        elif isinstance(node, ast.Compare):
            left = phitonize_node(node.left)
            ops = [phitonize_operator(op) for op in node.ops]
            comparators = [phitonize_node(comp) for comp in node.comparators]
            parts = [left]
            for op, comp in zip(ops, comparators, strict=False):
                parts.extend([op, comp])
            return "".join(parts)

        elif isinstance(node, ast.Attribute):
            value = phitonize_node(node.value)
            return f"{value}·{node.attr}"

        elif isinstance(node, ast.List):
            elements = [phitonize_node(elt) for elt in node.elts]
            return f"[{','.join(elements)}]"

        elif isinstance(node, ast.Tuple):
            elements = [phitonize_node(elt) for elt in node.elts]
            return f"({','.join(elements)})"

        elif isinstance(node, ast.Dict):
            items = [
                f"{phitonize_node(k)}:{phitonize_node(v)}"
                for k, v in zip(node.keys, node.values, strict=False)
            ]
            return f"{{{','.join(items)}}}"

        elif isinstance(node, ast.Set):
            elements = [phitonize_node(elt) for elt in node.elts]
            return f"{{{','.join(elements)}}}"

        elif isinstance(node, ast.ListComp):
            elt = phitonize_node(node.elt)
            generators = []
            for gen in node.generators:
                target = phitonize_node(gen.target)
                iter_expr = phitonize_node(gen.iter)
                ifs = [f"⋔{phitonize_node(if_expr)}" for if_expr in gen.ifs]
                generators.append(f"∀{target}∈{iter_expr}{''.join(ifs)}")
            return f"⟬{elt} {' '.join(generators)}⟭"

        elif isinstance(node, ast.DictComp):
            key = phitonize_node(node.key)
            value = phitonize_node(node.value)
            generators = []
            for gen in node.generators:
                target = phitonize_node(gen.target)
                iter_expr = phitonize_node(gen.iter)
                ifs = [f"⋔{phitonize_node(if_expr)}" for if_expr in gen.ifs]
                generators.append(f"∀{target}∈{iter_expr}{''.join(ifs)}")
            return f"⟦{key}:{value} {' '.join(generators)}⟧"

        elif isinstance(node, ast.SetComp):
            elt = phitonize_node(node.elt)
            generators = []
            for gen in node.generators:
                target = phitonize_node(gen.target)
                iter_expr = phitonize_node(gen.iter)
                ifs = [f"⋔{phitonize_node(if_expr)}" for if_expr in gen.ifs]
                generators.append(f"∀{target}∈{iter_expr}{''.join(ifs)}")
            return f"⦃{elt} {' '.join(generators)}⦄"

        elif isinstance(node, ast.JoinedStr):
            values = []
            for value in node.values:
                if isinstance(value, ast.FormattedValue):
                    values.append(f"{{{phitonize_node(value.value)}}}")
                elif isinstance(value, ast.Constant):
                    values.append(str(value.value))
            return f"「{''.join(values)}」"

        elif isinstance(node, ast.NamedExpr):
            target = phitonize_node(node.target)
            value = phitonize_node(node.value)
            return f"{target}≝{value}"

        elif isinstance(node, ast.Starred):
            value = phitonize_node(node.value)
            return f"*{value}"

        elif isinstance(node, ast.Lambda):
            args = phitonize_arguments(node.args)
            body = phitonize_node(node.body)
            return f"λ{args}:{body}"

        elif isinstance(node, ast.Subscript):
            value = phitonize_node(node.value)
            slice_expr = phitonize_node(node.slice)
            return f"{value}[{slice_expr}]"

        elif isinstance(node, ast.Slice):
            lower = phitonize_node(node.lower) if node.lower else ""
            upper = phitonize_node(node.upper) if node.upper else ""
            step = f":{phitonize_node(node.step)}" if node.step else ""
            return f"{lower}:{upper}{step}"

        elif isinstance(node, ast.UnaryOp):
            operand = phitonize_node(node.operand)
            if isinstance(node.op, ast.Not):
                return f"¬{operand}"
            elif isinstance(node.op, ast.USub):
                return f"-{operand}"
            elif isinstance(node.op, ast.UAdd):
                return f"+{operand}"
            return f"{node.op.__class__.__name__}({operand})"

        elif isinstance(node, ast.BoolOp):
            op = "∧" if isinstance(node.op, ast.And) else "∨"
            values = [phitonize_node(val) for val in node.values]
            return op.join(values)

        elif isinstance(node, ast.Await):
            value = phitonize_node(node.value)
            return f"⊡{value}"

        elif isinstance(node, ast.AnnAssign):
            target = phitonize_node(node.target)
            annotation = phitonize_node(node.annotation)
            value = f"≔{phitonize_node(node.value)}" if node.value else ""
            return f"{target}⦂{annotation}{value}"

        elif isinstance(node, ast.Assign):
            targets = [phitonize_node(target) for target in node.targets]
            value = phitonize_node(node.value)
            return f"{','.join(targets)}≔{value}"

        elif isinstance(node, ast.AugAssign):
            target = phitonize_node(node.target)
            op = phitonize_operator(node.op)
            value = phitonize_node(node.value)
            return f"{target}△{op}{value}"

        elif isinstance(node, ast.Pass):
            return "⊘"

        elif isinstance(node, ast.Break):
            return "⊠"

        elif isinstance(node, ast.Continue):
            return "⋯"

        elif isinstance(node, ast.Assert):
            test = phitonize_node(node.test)
            msg = f",{phitonize_node(node.msg)}" if node.msg else ""
            return f"⊪{test}{msg}"

        elif isinstance(node, ast.Delete):
            targets = [phitonize_node(target) for target in node.targets]
            return f"del {','.join(targets)}"

        elif isinstance(node, ast.Raise):
            exc = phitonize_node(node.exc) if node.exc else ""
            cause = f" from {phitonize_node(node.cause)}" if node.cause else ""
            return f"↑{exc}{cause}"

        elif isinstance(node, ast.Global):
            return f"global {','.join(node.names)}"

        elif isinstance(node, ast.Nonlocal):
            return f"nonlocal {','.join(node.names)}"

        elif isinstance(node, ast.Import):
            if config.level < 3:
                names = [alias.name for alias in node.names]
                return f"import {','.join(names)}"
            return ""  # Skip imports at higher compression levels

        elif isinstance(node, ast.ImportFrom):
            if config.level < 3:
                module = node.module or ""
                names = [alias.name for alias in node.names]
                return f"from {module} import {','.join(names)}"
            return ""  # Skip imports at higher compression levels

        # Fallback for unhandled nodes
        try:
            return str(ast.unparse(node))
        except Exception:
            return f"<{node.__class__.__name__}>"

    def phitonize_arguments(args: ast.arguments) -> str:
        """Convert function arguments to Phiton notation."""
        parts = []
        for arg in args.args:
            arg_str = arg.arg
            if config.type_hints and arg.annotation:
                type_hint = phitonize_node(arg.annotation)
                arg_str += f"⦂⟮{type_hint}⟯"
            parts.append(arg_str)
        return ",".join(parts)

    def phitonize_body(body: Sequence[ast.AST]) -> str:
        """Convert a list of statements to Phiton notation with optimizations."""
        statements = []
        for node in body:
            stmt = phitonize_node(node)
            # Create local symbols for frequently used expressions
            expr = ast.unparse(node) if isinstance(node, ast.expr) else ""
            if expr and should_create_symbol(expr, expr_freq.get(expr, 0)):
                sym_name = get_next_symbol_name()
                scope_stack[-1][sym_name] = expr
                statements.append(f"§{sym_name}≔{stmt}")
                symbol_table[expr] = sym_name
            else:
                statements.append(stmt)

        return "→".join(optimize_expression(stmt) for stmt in statements)

    def phitonize_operator(op: ast.operator | ast.cmpop | ast.boolop) -> str:
        """Convert Python operator to Phiton symbol."""
        # Simple mapping based on operator class name
        name = op.__class__.__name__
        if name == "Add":
            return "+"
        elif name == "Sub":
            return "-"
        elif name == "Mult":
            return "*"
        elif name == "Div":
            return "/"
        elif name == "Eq":
            return "≡"
        elif name == "NotEq":
            return "≠"
        elif name == "Lt":
            return "<"
        elif name == "LtE":
            return "≤"
        elif name == "Gt":
            return ">"
        elif name == "GtE":
            return "≥"
        elif name == "In":
            return "∈"
        elif name == "NotIn":
            return "∉"
        elif name == "And":
            return "∧"
        elif name == "Or":
            return "∨"
        elif name == "Not":
            return "¬"
        return name

    def phitonize_match_pattern(pattern: ast.pattern | None) -> str:
        """Convert a match pattern to Phiton notation."""
        if pattern is None:
            return "_"
        if isinstance(pattern, ast.MatchValue):
            return phitonize_node(pattern.value)
        elif isinstance(pattern, ast.MatchSingleton):
            if pattern.value is None:
                return "∅"
            elif pattern.value is True:
                return "⊤"
            elif pattern.value is False:
                return "⊥"
        elif isinstance(pattern, ast.MatchSequence):
            patterns = [phitonize_match_pattern(p) for p in pattern.patterns]
            return f"[{','.join(patterns)}]"
        elif isinstance(pattern, ast.MatchStar):
            return f"*{pattern.name}" if pattern.name else "*_"
        elif isinstance(pattern, ast.MatchMapping):
            items = []
            for key, pat in zip(pattern.keys, pattern.patterns, strict=False):
                key_str = phitonize_node(key)
                pat_str = phitonize_match_pattern(pat)
                items.append(f"{key_str}:{pat_str}")
            if pattern.rest:
                items.append(f"**{pattern.rest}")
            return f"{{{','.join(items)}}}"
        elif isinstance(pattern, ast.MatchClass):
            cls = phitonize_node(pattern.cls)
            patterns = [phitonize_match_pattern(p) for p in pattern.patterns]
            kwargs = [
                f"{k}={phitonize_match_pattern(p)}"
                for k, p in zip(pattern.kwd_attrs, pattern.kwd_patterns, strict=False)
            ]
            args = patterns + kwargs
            return f"{cls}({','.join(args)})"
        elif isinstance(pattern, ast.MatchAs):
            if pattern.pattern:
                inner = phitonize_match_pattern(pattern.pattern)
                return f"{inner} as {pattern.name}" if pattern.name else inner
            return pattern.name if pattern.name else "_"
        return "_"  # Fallback for unhandled patterns

    result = phitonize_node(tree)

    # Apply final optimizations
    return optimize_final(result, config.level)
