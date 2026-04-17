"""CLI entry point for the calculator. Invoked via `python -m src.cli`."""

import sys

from src.input_handler import parse_input, run_calculation


def main() -> None:
    """Run the calculator in CLI mode.

    Reads operand1, operator, and operand2 from positional command-line
    arguments, delegates parsing and dispatch to the input_handler module,
    and prints the result to stdout.

    Usage:
        python -m src.cli <operand1> <operator> <operand2>

    Exits with status 2 if the wrong number of arguments is supplied.
    Exits with status 1 on any input or arithmetic error.
    """
    if len(sys.argv) != 4:
        print(
            "Usage: python -m src.cli <operand1> <operator> <operand2>",
            file=sys.stderr,
        )
        sys.exit(2)

    # sys.argv layout: [script, operand1, operator, operand2]
    # parse_input signature: parse_input(operand_a, operand_b, operator)
    # so operand_b is sys.argv[3] and operator is sys.argv[2].
    try:
        a, b, method_name = parse_input(sys.argv[1], sys.argv[3], sys.argv[2])
        result = run_calculation(a, b, method_name)
    except (ValueError, ZeroDivisionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(result)


if __name__ == "__main__":
    main()
