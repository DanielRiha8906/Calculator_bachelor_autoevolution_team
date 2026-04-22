"""Centralized validation and retry management for user input.

Provides mode detection, error formatting, and session-scoped validation
classes for both operand (numeric) and operation (string) inputs.  Supports
two runtime modes:

- ``'interactive'``: user is at a TTY; invalid input triggers a retry loop
  up to a configurable maximum.
- ``'cli'``: input arrives from a pipe or script; invalid input immediately
  raises :class:`SystemExit`.
"""

import sys
from collections.abc import Callable


_MAX_RETRIES_DEFAULT: int = 5
_TERMINATION_MSG_TEMPLATE: str = (
    "Maximum retry attempts ({max_retries}) exceeded. Session terminated."
)


def detect_mode() -> str:
    """Detect whether the process is running interactively or as a CLI pipe.

    Returns:
        ``'interactive'`` if :data:`sys.stdin` is a TTY, otherwise ``'cli'``.
    """
    return "interactive" if sys.stdin.isatty() else "cli"


def format_operation_error(available_ops: list[str]) -> str:
    """Format a human-readable error string listing all available operations.

    Args:
        available_ops: The list of valid operation name strings.

    Returns:
        A single-line string such as
        ``"Invalid operation. Available operations: add, subtract, ..."``.
    """
    ops_joined = ", ".join(available_ops)
    return f"Invalid operation. Available operations: {ops_joined}"


class OperandValidationSession:
    """Manages retry logic for numeric operand input.

    In ``'interactive'`` mode the session loops, re-prompting the user on
    each invalid entry until either a valid float is supplied or the maximum
    number of consecutive failures is reached.

    In ``'cli'`` mode a single attempt is made; any failure immediately
    raises :class:`SystemExit`.

    Args:
        mode: ``'interactive'`` or ``'cli'``.
        max_retries: Maximum consecutive failed attempts before the session
            terminates (default 5).
    """

    def __init__(self, mode: str, max_retries: int = _MAX_RETRIES_DEFAULT) -> None:
        self._mode: str = mode
        self._max_retries: int = max_retries
        self._attempt_count: int = 0

    @property
    def attempt_count(self) -> int:
        """Current number of consecutive failed input attempts."""
        return self._attempt_count

    def reset_counter(self) -> None:
        """Reset the consecutive-failure counter to zero."""
        self._attempt_count = 0

    def validate_input(
        self, prompt_fn: Callable[[], str], error_msg: str
    ) -> float | None:
        """Obtain and validate a numeric float value from the user.

        The *prompt_fn* callable is responsible for producing the raw input
        string (e.g. by calling :func:`input` internally).

        In interactive mode the loop continues until a valid float is entered
        or ``max_retries`` consecutive failures have occurred.  On reaching
        the limit a termination message is printed and ``None`` is returned.

        In CLI mode a single call to *prompt_fn* is made.  If parsing fails,
        :class:`SystemExit` is raised with a descriptive message.

        Args:
            prompt_fn: A zero-argument callable that returns a raw input
                string.
            error_msg: Prefix message shown on invalid input
                (interactive mode only).

        Returns:
            The parsed :class:`float`, or ``None`` if the retry limit was
            reached (interactive mode only).

        Raises:
            SystemExit: In CLI mode when the input is not a valid float.
        """
        if self._mode == "cli":
            raw = prompt_fn()
            try:
                value = float(raw)
                return value
            except ValueError:
                raise SystemExit(
                    f"Error: '{raw}' is not a valid number. "
                    "Please supply a numeric value."
                )

        # Interactive mode — retry loop.
        while True:
            raw = prompt_fn()
            try:
                value = float(raw)
                self.reset_counter()
                return value
            except ValueError:
                self._attempt_count += 1
                print(f"  {error_msg} '{raw}' is not a valid number.  Please try again.")
                if self._attempt_count >= self._max_retries:
                    print(
                        _TERMINATION_MSG_TEMPLATE.format(
                            max_retries=self._max_retries
                        )
                    )
                    return None


class OperationValidationSession:
    """Manages retry logic for operation name input.

    In ``'interactive'`` mode the session loops, re-prompting the user on
    each invalid entry until either a recognised operation is supplied or the
    maximum number of consecutive failures is reached.

    In ``'cli'`` mode a single attempt is made; any failure prints the
    available-operations error and immediately raises :class:`SystemExit`.

    Args:
        mode: ``'interactive'`` or ``'cli'``.
        available_ops: The list of valid operation name strings.
        max_retries: Maximum consecutive failed attempts before the session
            terminates (default 5).
    """

    def __init__(
        self,
        mode: str,
        available_ops: list[str],
        max_retries: int = _MAX_RETRIES_DEFAULT,
    ) -> None:
        self._mode: str = mode
        self._available_ops: list[str] = available_ops
        self._max_retries: int = max_retries
        self._attempt_count: int = 0

    @property
    def attempt_count(self) -> int:
        """Current number of consecutive failed input attempts."""
        return self._attempt_count

    def reset_counter(self) -> None:
        """Reset the consecutive-failure counter to zero."""
        self._attempt_count = 0

    def validate_input(self, prompt_fn: Callable[[], str]) -> str | None:
        """Obtain and validate an operation name from the user.

        The *prompt_fn* callable is responsible for producing the raw input
        string.  Comparison against ``available_ops`` is case-insensitive.

        In interactive mode the loop continues until a valid operation is
        entered or ``max_retries`` consecutive failures have occurred.  On
        reaching the limit a termination message is printed and ``None`` is
        returned.

        In CLI mode a single call to *prompt_fn* is made.  If the result is
        not a recognised operation, the available-operations error is printed
        and :class:`SystemExit` is raised.

        Args:
            prompt_fn: A zero-argument callable that returns a raw input
                string.

        Returns:
            The matched operation name string (from ``available_ops``,
            preserving original casing), or ``None`` if the retry limit was
            reached (interactive mode only).

        Raises:
            SystemExit: In CLI mode when the input is not a valid operation.
        """
        ops_lower: dict[str, str] = {op.lower(): op for op in self._available_ops}

        if self._mode == "cli":
            raw = prompt_fn().strip()
            matched = ops_lower.get(raw.lower())
            if matched is not None:
                return matched
            error = format_operation_error(self._available_ops)
            print(error)
            raise SystemExit(
                f"Error: '{raw}' is not a valid operation. "
                f"Available operations: {', '.join(self._available_ops)}"
            )

        # Interactive mode — retry loop.
        while True:
            raw = prompt_fn().strip()
            matched = ops_lower.get(raw.lower())
            if matched is not None:
                self.reset_counter()
                return matched
            self._attempt_count += 1
            print(format_operation_error(self._available_ops))
            if self._attempt_count >= self._max_retries:
                print(
                    _TERMINATION_MSG_TEMPLATE.format(max_retries=self._max_retries)
                )
                return None
