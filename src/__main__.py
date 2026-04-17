import sys

from src.cli import run_cli
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


if __name__ == "__main__":
    # When invoked as `python -m src [args...]`, route to CLI mode if the
    # user supplied any arguments; otherwise run the interactive calculator.
    if len(sys.argv) > 1:
        run_cli()
    else:
        main()
