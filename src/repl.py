"""Read-Eval-Print Loop (REPL) interface for the Calculator.

Provides :class:`CalculatorREPL`, a text-based interactive shell that lets a
user invoke any supported calculator operation by typing its name followed by
numeric arguments.  All operations are recorded automatically via the
underlying :class:`~src.session.CalculatorSession`.

Example usage::

    $ python -m src.repl
    Welcome to the Calculator REPL.
    Type 'help' for available commands, 'exit' or 'quit' to quit.
    > add 2 3
    5
    > history
    add(2, 3) = 5
    > exit
    Goodbye!
"""

from .session import CalculatorSession

# Maps command aliases and canonical names to (calculator_method_name, expected_arg_count).
_OPERATIONS: dict[str, tuple[str, int]] = {
    "add": ("add", 2),
    "subtract": ("subtract", 2),
    "multiply": ("multiply", 2),
    "divide": ("divide", 2),
    "square": ("square", 1),
    "cube": ("cube", 1),
    "square_root": ("square_root", 1),
    "sqrt": ("square_root", 1),
    "cube_root": ("cube_root", 1),
    "cbrt": ("cube_root", 1),
    "natural_logarithm": ("natural_logarithm", 1),
    "factorial": ("factorial", 1),
    "logarithm": ("logarithm", 1),
    "power": ("power", 2),
}


class CalculatorREPL:
    """Interactive REPL shell for the Calculator.

    Reads lines from stdin, dispatches calculator operations, and records
    every result via the session history.

    Args:
        history_file: Path to the file where history is written on exit.
            Defaults to ``"history.txt"``.
    """

    def __init__(self, history_file: str = "history.txt") -> None:
        """Initialise with a fresh :class:`~src.session.CalculatorSession`."""
        self._session: CalculatorSession = CalculatorSession(
            history_file=history_file
        )

    def run(self) -> None:
        """Start the REPL loop.

        Prints a welcome message then repeatedly prompts the user for input.
        The loop exits cleanly on ``exit`` or ``quit``, and any exception
        raised during command execution is caught and reported without
        crashing the loop.
        """
        print("Welcome to the Calculator REPL.")
        print("Type 'help' for available commands, 'exit' or 'quit' to quit.")

        while True:
            try:
                line = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                self._session.save_and_close()
                break

            if not line:
                continue

            lower = line.lower()

            if lower in {"exit", "quit"}:
                self._session.save_and_close()
                print("Goodbye!")
                break

            if lower == "history":
                self._display_history()
                continue

            if lower == "help":
                self._handle_help()
                continue

            try:
                self._execute_command(line)
            except Exception as exc:  # noqa: BLE001
                print(f"Error: {exc}")

    def _execute_command(self, command: str) -> None:
        """Parse and execute one calculator command.

        The expected format is::

            operation_name arg1 [arg2]

        Numeric arguments are parsed as floats.  For ``factorial`` the float
        is converted to ``int`` before being forwarded to the calculator.

        Args:
            command: The raw input line from the user.

        Raises:
            ValueError: If an argument cannot be parsed as a number or if the
                wrong number of arguments is supplied.
        """
        parts = command.split()
        op_key = parts[0].lower()
        raw_args = parts[1:]

        if op_key not in _OPERATIONS:
            print(f"Unknown operation: {op_key}")
            return

        method_name, expected_arity = _OPERATIONS[op_key]

        if len(raw_args) != expected_arity:
            raise ValueError(
                f"{op_key} expects {expected_arity} argument(s), "
                f"got {len(raw_args)}."
            )

        try:
            parsed: list[object] = [float(a) for a in raw_args]
        except ValueError:
            raise ValueError(
                f"All arguments must be numeric. Got: {raw_args}"
            )

        # factorial requires an int argument.
        if method_name == "factorial":
            parsed = [int(parsed[0])]

        calculator = self._session.get_calculator()
        result = getattr(calculator, method_name)(*parsed)
        print(_format_result(result))

    def _display_history(self) -> None:
        """Print all history entries to stdout.

        If no operations have been performed yet, prints a placeholder message.
        """
        entries = self._session.get_history()
        if not entries:
            print("No history yet.")
            return
        for entry in entries:
            print(entry)

    def _handle_help(self) -> None:
        """Print a summary of all available commands."""
        print("Available commands:")
        print("  add <a> <b>            - add two numbers")
        print("  subtract <a> <b>       - subtract b from a")
        print("  multiply <a> <b>       - multiply two numbers")
        print("  divide <a> <b>         - divide a by b")
        print("  power <base> <exp>     - raise base to exponent")
        print("  square <x>             - x squared")
        print("  cube <x>               - x cubed")
        print("  square_root <x>        - square root of x  (alias: sqrt)")
        print("  sqrt <x>               - alias for square_root")
        print("  cube_root <x>          - cube root of x    (alias: cbrt)")
        print("  cbrt <x>               - alias for cube_root")
        print("  logarithm <x>          - base-10 logarithm of x")
        print("  natural_logarithm <x>  - natural logarithm of x")
        print("  factorial <n>          - factorial of non-negative integer n")
        print("  history                - show operation history")
        print("  help                   - show this message")
        print("  exit / quit            - save history and exit")


def _format_result(result: object) -> str:
    """Format a calculator result for display.

    Whole-number floats (e.g. ``5.0``) are displayed without a decimal point.
    All other values use their default string representation.

    Args:
        result: The value returned by a calculator method.

    Returns:
        A clean string suitable for printing to the user.
    """
    if isinstance(result, float) and not isinstance(result, bool):
        if result == int(result):
            return str(int(result))
        return str(result)
    return str(result)


def main() -> None:
    """Entry point: create and run a :class:`CalculatorREPL`."""
    CalculatorREPL().run()


if __name__ == "__main__":
    main()
