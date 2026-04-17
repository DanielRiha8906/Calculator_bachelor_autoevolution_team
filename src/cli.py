"""CLI interface for the calculator.

Accepts three positional arguments (operand_a, operator, operand_b) and
prints the result to stdout.  On error the diagnostic is written to stderr
and the process exits with a non-zero status code.

Exit codes:
    0 — successful calculation
    1 — input or arithmetic error (ValueError, ZeroDivisionError)
    2 — argument-parsing error (argparse default)
"""

import argparse
import sys

from src.input_handler import parse_input, run_calculation


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser for the CLI.

    Returns:
        A configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="calculator",
        description=(
            "Command-line calculator. "
            "Provide two numeric operands and one operator."
        ),
        epilog=(
            "Examples:\n"
            "  python -m src 2 + 3\n"
            '  python -m src "2 + 3"\n'
            "  python -m src 10 / 4"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "operand_a",
        metavar="OPERAND_A",
        help="The first numeric operand (e.g. 2 or 2.5).",
    )
    parser.add_argument(
        "operator",
        metavar="OPERATOR",
        help="The arithmetic operator: +, -, *, /.",
    )
    parser.add_argument(
        "operand_b",
        metavar="OPERAND_B",
        help="The second numeric operand (e.g. 3 or 1.5).",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Parse CLI arguments and run the requested calculation.

    Writes the result to stdout on success.  Writes a human-readable error
    message to stderr and exits with status 1 on a ValueError or
    ZeroDivisionError.  argparse handles --help and bad argument counts,
    exiting with status 2 automatically.

    Args:
        argv: Argument list to parse.  Defaults to sys.argv[1:] when None.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        a, b, method_name = parse_input(args.operand_a, args.operand_b, args.operator)
        result = run_calculation(a, b, method_name)
    except (ValueError, ZeroDivisionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Result: {result}")
