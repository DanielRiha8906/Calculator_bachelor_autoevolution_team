import argparse
import sys

from src.input_handler import parse_input, run_calculation


def main() -> None:
    """Run the interactive calculator.

    Prompts the user for two operands and an operator, delegates parsing
    and dispatch to the input_handler module, and prints the result.
    Exits with status 1 on any input or arithmetic error.
    """
    operand_a = input("Enter first operand: ")
    operand_b = input("Enter second operand: ")
    operator = input("Enter operator (+, -, *, /): ")

    try:
        a, b, method_name = parse_input(operand_a, operand_b, operator)
        result = run_calculation(a, b, method_name)
    except (ValueError, ZeroDivisionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Result: {result}")


def cli_main(args: list[str] | None = None) -> None:
    """Run the calculator from command-line positional arguments.

    Accepts exactly three positional arguments in infix order:
    operand_a, operator, operand_b (e.g. ``3 + 4``).
    Prints ``Result: {result}`` to stdout on success.
    Prints ``Error: {exc}`` to stderr and exits with status 1 on
    ValueError or ZeroDivisionError.  argparse exits with status 2 if
    the wrong number of arguments is supplied.

    Args:
        args: Argument list to parse.  Defaults to ``sys.argv[1:]`` when
            ``None``.
    """
    parser = argparse.ArgumentParser(
        description="Evaluate a simple arithmetic expression."
    )
    parser.add_argument("operand_a", type=str, help="First operand")
    parser.add_argument("operator", type=str, help="Operator (+, -, *, /)")
    parser.add_argument("operand_b", type=str, help="Second operand")

    parsed = parser.parse_args(args)

    try:
        a, b, method_name = parse_input(parsed.operand_a, parsed.operand_b, parsed.operator)
        result = run_calculation(a, b, method_name)
    except (ValueError, ZeroDivisionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Result: {result}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_main()
    else:
        main()
