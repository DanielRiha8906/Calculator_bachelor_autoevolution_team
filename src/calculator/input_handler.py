"""Input handler classes for the modular calculator (Issue #405).

Provides CLIInput for parsing command-line arguments and InteractiveInput
for reading from stdin in REPL mode.
"""


class CLIInput:
    """Wraps a ``sys.argv``-style list for structured CLI argument access.

    Args:
        argv: The argument vector (e.g. ``sys.argv``).  The first element is
            expected to be the program name.
    """

    def __init__(self, argv: list[str]) -> None:
        self._argv = argv

    def has_operation_args(self) -> bool:
        """Return True if operation arguments are present beyond the program name.

        Returns:
            True when ``len(argv) > 1``, False otherwise.
        """
        return len(self._argv) > 1

    def get_operation_and_operands(self) -> tuple[str, list[str]]:
        """Extract the operation name and raw operand strings.

        Returns:
            A ``(operation_name, operands)`` tuple where *operation_name* is
            ``argv[1]`` and *operands* is ``argv[2:]``.
        """
        return self._argv[1], self._argv[2:]


class InteractiveInput:
    """Reads operation names and operands from stdin for REPL mode."""

    def read_operation(self) -> str:
        """Prompt the user to enter an operation name and return it stripped.

        Returns:
            The operation name string with surrounding whitespace removed.
        """
        return input("Enter operation: ").strip()

    def read_operand(self, label: str) -> str:
        """Prompt the user to enter an operand value and return it stripped.

        Args:
            label: The prompt label shown to the user.

        Returns:
            The raw operand string with surrounding whitespace removed.
        """
        return input(f"{label}: ").strip()

    def show_message(self, message: str) -> None:
        """Print a message to stdout.

        Args:
            message: The message string to display.
        """
        print(message)
