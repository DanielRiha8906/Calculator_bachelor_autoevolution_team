"""Encapsulates all CLI-specific argument parsing, validation, and output logic."""

import sys


class CLIHandler:
    """Handles command-line argument parsing, operand validation, and output for CLI mode."""

    def parse_arguments(self, args: list[str]) -> tuple[str, list[str]]:
        """Parse command-line arguments and return the operation key with operand strings.

        The first element of ``args`` is interpreted as the operation name; all
        remaining elements are treated as raw operand strings.

        Args:
            args: The list of CLI arguments (excluding the program name, i.e.
                  ``sys.argv[1:]``).

        Returns:
            A tuple of ``(operation_key, operand_strings)``.

        Raises:
            ValueError: If ``args`` is empty.
        """
        if not args:
            raise ValueError(
                "No arguments provided. Usage: calculator <operation> [operands...]"
            )
        operation_key = args[0]
        operand_strings = args[1:]
        return operation_key, operand_strings

    def validate_operands(self, operands: list[str], arity: int) -> list[float]:
        """Validate that the operand count matches ``arity`` and convert to floats.

        Args:
            operands: The raw string operands from the command line.
            arity: The expected number of operands for the operation.

        Returns:
            A list of operand values converted to ``float``.

        Raises:
            ValueError: If the number of operands does not match ``arity``, or if
                        any operand string cannot be converted to a float.
        """
        if len(operands) != arity:
            raise ValueError(
                f"Expected {arity} operand(s), got {len(operands)}."
            )
        result: list[float] = []
        for operand in operands:
            try:
                result.append(float(operand))
            except ValueError:
                raise ValueError(
                    f"Invalid operand '{operand}': must be a numeric value."
                )
        return result

    def print_result(self, description: str, operands: list[float], result: float) -> None:
        """Print the operation result to stdout.

        Args:
            description: Human-readable name of the operation performed.
            operands: The operand values used in the operation.
            result: The computed result.
        """
        print(f"Result: {result}")

    def print_error(self, message: str) -> None:
        """Print an error message to stderr.

        Args:
            message: The error description to display.
        """
        print(f"Error: {message}", file=sys.stderr)

    def is_cli_mode(self, args: list[str]) -> bool:
        """Return True if the argument list is non-empty, indicating CLI mode.

        Args:
            args: The list of CLI arguments (typically ``sys.argv[1:]``).

        Returns:
            ``True`` when ``args`` contains at least one element, ``False`` otherwise.
        """
        return bool(args)
