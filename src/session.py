"""Session management for the Calculator.

Ties together a :class:`~src.calculator.Calculator` instance and an
:class:`~src.history.OperationHistory` so that every operation performed
through the session is automatically recorded and can later be persisted to
disk.
"""

from .calculator import Calculator
from .history import OperationHistory


class CalculatorSession:
    """Manages a single calculator session with automatic operation logging.

    Creates a :class:`~src.calculator.Calculator` and wraps it so that every
    method call is transparently recorded in an :class:`~src.history.OperationHistory`.
    At the end of the session the history can be written to a file via
    :meth:`save_and_close`.

    Args:
        history_file: Path to the file where the history will be written when
            :meth:`save_and_close` is called.  Defaults to ``"history.txt"``.
    """

    def __init__(self, history_file: str = "history.txt") -> None:
        """Initialise session with a fresh history, calculator, and wrapper."""
        self._history: OperationHistory = OperationHistory()
        self._history_file: str = history_file
        self._calculator: Calculator = Calculator()
        self._wrapped: object = self._wrap_calculator()

    def get_calculator(self) -> object:
        """Return the wrapped calculator that records every operation.

        Returns:
            A wrapper object whose public methods mirror :class:`~src.calculator.Calculator`
            but additionally log each call to the session history.
        """
        return self._wrapped

    def get_history(self) -> list[str]:
        """Return all history entries recorded so far in this session.

        Returns:
            A list of formatted operation strings in insertion order.
        """
        return self._history.get_entries()

    def save_and_close(self) -> None:
        """Write the session history to the configured file.

        Delegates to :meth:`~src.history.OperationHistory.write_to_file`.
        """
        self._history.write_to_file(self._history_file)

    def _wrap_calculator(self) -> object:
        """Create and return a logging wrapper around the calculator.

        Returns:
            An instance of the inner ``_CalculatorWrapper`` class that
            intercepts attribute access to record each operation.
        """
        history = self._history
        calculator = self._calculator

        class _CalculatorWrapper:
            """Proxy for :class:`~src.calculator.Calculator` that logs calls.

            Uses ``__getattr__`` to intercept every method lookup.  When the
            returned callable is invoked, it:

            1. Delegates to the underlying :class:`~src.calculator.Calculator`.
            2. Records the call via :class:`~src.history.OperationHistory`.
            3. Returns the original result unchanged.
            """

            def __getattr__(self, name: str) -> object:
                attr = getattr(calculator, name)
                if not callable(attr):
                    return attr

                def _recording_call(*args: object) -> object:
                    result = attr(*args)
                    history.add_entry(name, list(args), result)
                    return result

                return _recording_call

        return _CalculatorWrapper()
