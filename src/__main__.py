import sys

from src.cli import main as cli_main
from src.dispatcher import run_calculation
from src.parser import BINARY_OPERATORS
from src.retry_handler import get_input_with_retries


def main() -> None:
    """Run the interactive calculator.

    Collects two operands and an operator via retry-aware prompts, then
    delegates dispatch to the input_handler module and prints the result.
    Returns cleanly (without sys.exit) when the user exhausts retries, and
    exits with status 1 only on an arithmetic error.
    """
    result_tuple = get_input_with_retries()
    if result_tuple is None:
        return

    first_operand, operator, second_operand = result_tuple
    method_name = BINARY_OPERATORS[operator]

    try:
        result, _calc = run_calculation(first_operand, second_operand, method_name)
    except (ValueError, ZeroDivisionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Result: {result}")


if __name__ == "__main__":
    # When command-line arguments are present (beyond the module name itself),
    # delegate to the CLI handler.  Otherwise fall back to interactive mode.
    if len(sys.argv) > 1:
        cli_main()
    else:
        main()
