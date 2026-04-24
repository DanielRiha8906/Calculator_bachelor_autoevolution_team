"""Batch (non-interactive) command-line interface for the calculator.

Provides functions to parse command-line arguments, execute a single
calculation, and print results or errors.  Entry point is batch_main().
"""

import sys

from .calculator import Calculator
from .cli import OPERATIONS, display_result_unary, display_result_binary

# Batch-mode operation registry: maps the operation key used on the command
# line (always the Calculator method name or a consistent alias) to
# (arity, method_name, display_key) triples.
#
# The interactive OPERATIONS dict in cli.py uses symbol keys (+, -, …) for
# the arithmetic operators and method-name keys for the unary ops.  For the
# batch interface we expose every operation under its Calculator method name
# so that callers write "add 5 3" rather than "+ 5 3".
_BATCH_OPERATIONS: dict[str, tuple[int, str, str]] = {
    "add":       (2, "add",         "+"),
    "subtract":  (2, "subtract",    "-"),
    "multiply":  (2, "multiply",    "*"),
    "divide":    (2, "divide",      "/"),
    "power":     (2, "power",       "power"),
    "square":    (1, "square",      "square"),
    "cube":      (1, "cube",        "cube"),
    "sqrt":      (1, "square_root", "sqrt"),
    "cbrt":      (1, "cube_root",   "cbrt"),
    "factorial": (1, "factorial",   "factorial"),
    "log":       (1, "log",         "log"),
    "ln":        (1, "ln",          "ln"),
}


def parse_batch_args(argv: list[str]) -> tuple[str | None, list[str]]:
    """Parse a raw argument list into an operation key and operand strings.

    Args:
        argv: The argument list (typically sys.argv[1:]).

    Returns:
        A 2-tuple ``(operation_key, operands)`` where *operation_key* is
        ``None`` when the help flag is present or argv is empty, and
        *operands* is the remaining argument strings.
    """
    if not argv:
        return (None, [])
    if argv[0] in ("--help", "-h"):
        return (None, [])
    return (argv[0], argv[1:])


def print_help() -> None:
    """Print usage information and the list of supported operations to stdout."""
    lines = [
        "Usage: python -m src <operation> [operand ...]",
        "",
        "Batch-mode calculator.  Provide an operation and the required operands",
        "as positional arguments.  The result is printed to stdout.",
        "",
        "Supported operations:",
    ]
    for key, (arity, method_name, _display) in _BATCH_OPERATIONS.items():
        arity_str = "unary" if arity == 1 else "binary"
        lines.append(f"  {key:<12} ({arity_str})")
    lines.append("")
    lines.append("Help flags: --help, -h")
    print("\n".join(lines))


def execute_batch(operation_key: str, operands: list[str]) -> int:
    """Execute a single batch calculation and print the result.

    Args:
        operation_key: The name of the operation to perform (e.g. ``"add"``).
        operands: String representations of the numeric operands.

    Returns:
        ``0`` on success, ``1`` on any error (unknown operation, wrong operand
        count, non-numeric input, domain error).
    """
    if operation_key not in _BATCH_OPERATIONS:
        print(
            f"Error: unknown operation '{operation_key}'.  "
            f"Run with --help to see supported operations.",
            file=sys.stderr,
        )
        return 1

    arity, method_name, display_key = _BATCH_OPERATIONS[operation_key]

    if len(operands) != arity:
        print(
            f"Error: '{operation_key}' requires exactly {arity} operand(s), "
            f"but {len(operands)} were provided.",
            file=sys.stderr,
        )
        return 1

    try:
        parsed = [float(op) for op in operands]
    except ValueError as exc:
        print(f"Error: invalid numeric argument — {exc}", file=sys.stderr)
        return 1

    calc = Calculator()
    method = getattr(calc, method_name)

    try:
        if arity == 1:
            result = method(parsed[0])
            # Use the matching key from the interactive OPERATIONS dict when
            # it exists; otherwise fall back to display_key.
            if display_key in OPERATIONS:
                display_result_unary(display_key, parsed[0], result)
            else:
                print(f"{display_key}({parsed[0]}) = {result}")
        else:
            result = method(parsed[0], parsed[1])
            if display_key in OPERATIONS:
                display_result_binary(display_key, parsed[0], parsed[1], result)
            else:
                print(f"{parsed[0]} {display_key} {parsed[1]} = {result}")
    except ZeroDivisionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


def batch_main(argv: list[str]) -> None:
    """Entry point for batch-mode CLI.

    Parses *argv*, dispatches to the appropriate Calculator method, writes
    the result to stdout, and terminates the process with an appropriate
    exit code (``sys.exit``).

    Args:
        argv: The argument list (typically sys.argv[1:]).
    """
    if not argv:
        print(
            "Error: no operation specified.  Run with --help to see usage.",
            file=sys.stderr,
        )
        sys.exit(1)
        return

    operation_key, operands = parse_batch_args(argv)

    if operation_key is None:
        # Help flag was present.
        print_help()
        sys.exit(0)
        return

    exit_code = execute_batch(operation_key, operands)
    sys.exit(exit_code)
