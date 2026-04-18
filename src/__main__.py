import os
import sys

from src.cli import main as cli_main
from src.dispatcher import run_calculation, run_unary_calculation
from src.mode_manager import ModeManager
from src.parser import BINARY_OPERATORS
from src.retry_handler import get_input_with_retries, get_scientific_unary_input_with_retries


def main() -> None:
    """Run the interactive calculator session.

    Supports two modes: "normal" (binary arithmetic) and "scientific"
    (unary trigonometric / transcendental functions).  The user may switch
    modes at any operand prompt by entering ``mode science`` or
    ``mode normal`` instead of a numeric value.  After a mode switch the
    prompt is redisplayed so the user can continue.

    The session runs a single calculation per invocation.  Mode state is
    initialised to "normal" and persists until the user switches.

    Returns cleanly (without sys.exit) when the user exhausts retries, and
    exits with status 1 only on an arithmetic error.
    """
    mode_manager = ModeManager()

    if mode_manager.is_scientific():
        result_tuple = get_scientific_unary_input_with_retries()
        if result_tuple is None:
            return

        method_name, operand = result_tuple

        try:
            result, _calc = run_unary_calculation(operand, method_name)
        except (ValueError, ZeroDivisionError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

        print(f"Result: {result}")
    else:
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
    # When the --gui flag is present, or the CALCULATOR_GUI environment variable
    # is set to "1", launch the tkinter GUI.  When other command-line arguments
    # are present, delegate to the CLI handler.  Otherwise fall back to the
    # interactive mode.
    _gui_requested = (
        "--gui" in sys.argv
        or os.environ.get("CALCULATOR_GUI", "0") == "1"
    )

    if _gui_requested:
        from src.gui import CalculatorGUI

        _app = CalculatorGUI()
        _app.run()
    elif len(sys.argv) > 1:
        cli_main()
    else:
        main()
