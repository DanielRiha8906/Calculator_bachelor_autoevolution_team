"""Application layer for the calculator — encapsulates all user-interaction logic.

Separates UI concerns (CLI argument parsing, interactive REPL, input validation,
operation dispatch) from the pure-computation :class:`~src.calculator.Calculator`
layer.  Callers instantiate :class:`Application` with a :class:`Calculator`
instance and call either :meth:`run_cli_mode` (argv-aware) or
:meth:`run_interactive` (straight to REPL).
"""

import sys

from .calculator import Calculator
from .error_logging import ErrorLog
from .history import OperationHistory


# ---------------------------------------------------------------------------
# Internal arity map — used by Application methods that need arity information.
# The public ``registry`` attribute exposes only callables (no arity) so that
# callers can inspect the method signature directly.
# ---------------------------------------------------------------------------

_ARITY: dict[str, int] = {
    "add": 2,
    "subtract": 2,
    "multiply": 2,
    "divide": 2,
    "factorial": 1,
    "square": 1,
    "cube": 1,
    "square_root": 1,
    "cube_root": 1,
    "power": 2,
    "log10": 1,
    "ln": 1,
}


class Application:
    """Calculator application layer — handles all user-interaction concerns.

    Args:
        calculator: An instantiated :class:`~src.calculator.Calculator` whose
            methods will be registered and dispatched.

    Attributes:
        calculator: The underlying Calculator instance (read-only by convention).
        registry: A dict mapping operation names to their bound Calculator
            method callables.  Keys are the 12 supported operation names;
            values are plain callables (use ``_ARITY`` for arity information).
    """

    def __init__(self, calculator: Calculator) -> None:
        """Initialise the Application with a Calculator instance.

        Args:
            calculator: A fully-initialised :class:`~src.calculator.Calculator`.
        """
        self.calculator: Calculator = calculator
        self.registry: dict[str, object] = self._build_registry()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_registry(self) -> dict[str, object]:
        """Build the operation registry from the bound Calculator instance.

        Returns:
            A dict mapping each of the 12 operation names to the
            corresponding bound method callable.
        """
        calc = self.calculator
        return {
            "add": calc.add,
            "subtract": calc.subtract,
            "multiply": calc.multiply,
            "divide": calc.divide,
            "factorial": calc.factorial,
            "square": calc.square,
            "cube": calc.cube,
            "square_root": calc.square_root,
            "cube_root": calc.cube_root,
            "power": calc.power,
            "log10": calc.log10,
            "ln": calc.ln,
        }

    def _parse_number(self, raw: str) -> int | float:
        """Convert a string to int if possible, otherwise float.

        Args:
            raw: The raw string to parse.

        Returns:
            An int when the string represents a whole number without a
            decimal point, otherwise a float.

        Raises:
            ValueError: If the string cannot be interpreted as a number.
        """
        try:
            return int(raw)
        except ValueError:
            return float(raw)

    def _parse_cli_arguments(self) -> tuple[str, list[int | float]] | None:
        """Parse and validate sys.argv for CLI mode.

        Returns:
            A ``(operation_name, operands)`` tuple on success, or ``None``
            when no CLI arguments are present (caller should fall through to
            interactive mode).

        Side-effects:
            Prints an error to *stderr* and calls ``sys.exit(1)`` on any
            validation failure.
        """
        if len(sys.argv) <= 1:
            return None

        operation = sys.argv[1].lower()

        if operation not in self.registry:
            print(
                f"Error: Unknown operation '{operation}'. "
                f"Available operations: {list(self.registry.keys())}",
                file=sys.stderr,
            )
            sys.exit(1)

        arity = _ARITY[operation]
        raw_operands = sys.argv[2:]

        if len(raw_operands) != arity:
            print(
                f"Error: operation '{operation}' requires {arity} operand(s), "
                f"got {len(raw_operands)}",
                file=sys.stderr,
            )
            sys.exit(1)

        operands: list[int | float] = []
        for raw in raw_operands:
            try:
                operands.append(self._parse_number(raw))
            except ValueError:
                print(
                    f"Error: Invalid number '{raw}'. Please enter a numeric value.",
                    file=sys.stderr,
                )
                sys.exit(1)

        return operation, operands

    def _execute_cli_mode(self) -> None:
        """Execute the operation determined from sys.argv and print the result.

        Side-effects:
            Prints the result to *stdout*.  On ``ValueError`` or
            ``ZeroDivisionError`` prints the error to *stderr* and calls
            ``sys.exit(1)``.
        """
        parsed = self._parse_cli_arguments()
        if parsed is None:
            return
        operation, operands = parsed
        method = self.registry[operation]
        try:
            result = method(*operands)
            print(result)
        except (ValueError, ZeroDivisionError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

    def _run_interactive_loop(
        self, history_file_path: str | None = None
    ) -> None:
        """Run the interactive REPL loop.

        Args:
            history_file_path: Optional path for the history file.  When None,
                :class:`~src.history.OperationHistory` defaults to
                ``"history.txt"`` in the current working directory.

        The loop continues until the user types ``quit``, ``exit``, or ``q``,
        or until 3 consecutive failures occur (unknown operation, invalid
        operand, or domain error).  On reaching 3 consecutive failures the
        loop prints "Too many invalid attempts. Exiting." and terminates.
        ``EOFError`` is intentionally *not* caught here so that callers can
        decide how to handle a closed stdin.
        """
        history = OperationHistory(history_file_path)
        error_log = ErrorLog()
        consecutive_failures: int = 0

        while True:
            print(
                "Enter operation (add, subtract, multiply, divide, factorial, square, cube,"
            )
            print(
                "square_root, cube_root, power, log10, ln) or 'history' to view history or 'quit' to exit:"
            )
            operation = input("Select operation: ").strip().lower()

            if operation in ("quit", "exit", "q"):
                break

            # Handle 'history' special command before registry lookup.
            if operation == "history":
                entries = history.get_all()
                if not entries:
                    print("History: (empty)")
                else:
                    for i, entry in enumerate(entries, 1):
                        print(f"{i}. {entry}")
                consecutive_failures = 0
                continue

            if operation not in self.registry:
                error_msg = f"Unknown operation '{operation}'."
                error_log.log_error("unsupported_operation", operation, [], error_msg)
                print(f"Error: Unknown operation '{operation}'. Please try again.")
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    print("Too many invalid attempts. Exiting.")
                    break
                continue

            method = self.registry[operation]
            arity = _ARITY[operation]

            # Collect operands
            operands: list[int | float] = []
            error_occurred = False
            for i in range(arity):
                label = "Enter value: " if arity == 1 else f"Enter operand {i + 1}: "
                raw = input(label).strip()
                try:
                    operands.append(self._parse_number(raw))
                except ValueError:
                    error_msg = f"Invalid number '{raw}'. Please enter a numeric value."
                    error_log.log_error("invalid_input", operation, [raw], error_msg)
                    print(f"Error: {error_msg}")
                    consecutive_failures += 1
                    error_occurred = True
                    if consecutive_failures >= 3:
                        print("Too many invalid attempts. Exiting.")
                    break

            if error_occurred:
                if consecutive_failures >= 3:
                    break
                continue

            # Execute the operation
            try:
                result = method(*operands)
                print(f"Result: {result}")
                history.record(operation, operands, result)
                consecutive_failures = 0
            except (ValueError, ZeroDivisionError) as exc:
                error_log.log_error("calculation_error", operation, operands, str(exc))
                print(f"Error: {exc}")
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    print("Too many invalid attempts. Exiting.")
                    break

    # ------------------------------------------------------------------
    # Public entry points
    # ------------------------------------------------------------------

    def run_cli_mode(self) -> None:
        """Handle calculator invocation in both CLI and interactive modes.

        When command-line arguments are present (beyond the program name) this
        method parses them, executes the requested operation, and returns.

        When no command-line arguments are present this method falls back to
        the full interactive REPL loop.  An ``EOFError`` or ``OSError`` from
        the interactive loop is treated as a missing-operation condition: an
        error is printed to *stderr* and the process exits with code 1.
        """
        parsed = self._parse_cli_arguments()
        if parsed is not None:
            operation, operands = parsed
            method = self.registry[operation]
            error_log = ErrorLog()
            try:
                result = method(*operands)
                print(result)
            except (ValueError, ZeroDivisionError) as exc:
                error_log.log_error("calculation_error", operation, operands, str(exc))
                print(f"Error: {exc}", file=sys.stderr)
                sys.exit(1)
            return

        # --- Interactive (REPL) fallback ---
        try:
            self._run_interactive_loop()
        except (EOFError, OSError):
            print(
                "Error: operation required. "
                "Usage: calculator <operation> <operand1> [<operand2> ...]",
                file=sys.stderr,
            )
            sys.exit(1)

    def run_interactive(self) -> None:
        """Run the interactive calculator REPL loop directly.

        Continuously prompts the user to select an operation, then collects
        the required operands and prints the result.  Typing 'quit', 'exit',
        or 'q' terminates the loop.

        This method goes directly to the interactive REPL and does **not**
        inspect ``sys.argv``.  Use :meth:`run_cli_mode` when you want
        argv-aware dispatch.
        """
        self._run_interactive_loop()

    def execute_cli(self, args: list[str]) -> int | float | None:
        """Execute a single operation from a list of string arguments.

        This is a convenience method for programmatic CLI execution without
        manipulating ``sys.argv``.  The first element of *args* must be the
        operation name; subsequent elements are the operands as strings.

        Args:
            args: A list where ``args[0]`` is the operation name and
                ``args[1:]`` are the operand strings.

        Returns:
            The numeric result of the operation.

        Raises:
            SystemExit: If the operation name is unknown, the operand count
                is wrong, or operands cannot be parsed.
            ValueError: If a domain error occurs (e.g. square root of a
                negative number).
            ZeroDivisionError: If division by zero is attempted.
        """
        if not args:
            print(
                "Error: operation required. "
                "Usage: calculator <operation> <operand1> [<operand2> ...]",
                file=sys.stderr,
            )
            sys.exit(1)

        operation = args[0].lower()

        if operation not in self.registry:
            print(
                f"Error: Unknown operation '{operation}'. "
                f"Available operations: {list(self.registry.keys())}",
                file=sys.stderr,
            )
            sys.exit(1)

        arity = _ARITY[operation]
        raw_operands = args[1:]

        if len(raw_operands) != arity:
            print(
                f"Error: operation '{operation}' requires {arity} operand(s), "
                f"got {len(raw_operands)}",
                file=sys.stderr,
            )
            sys.exit(1)

        operands: list[int | float] = []
        for raw in raw_operands:
            try:
                operands.append(self._parse_number(raw))
            except ValueError:
                print(
                    f"Error: Invalid number '{raw}'. Please enter a numeric value.",
                    file=sys.stderr,
                )
                sys.exit(1)

        method = self.registry[operation]
        result = method(*operands)
        print(result)
        return result
