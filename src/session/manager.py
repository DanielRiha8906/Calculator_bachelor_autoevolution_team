"""Session state management for interactive calculator mode."""


class SessionManager:
    """Manages session state for an interactive calculator session.

    Tracks retry attempts across input phases and provides lifecycle hooks
    for the session (increment/reset retry counter).

    Args:
        calculator: A Calculator instance used for computations.
        error_logger: An ErrorLogger instance used to log errors.
        history: An OperationHistory instance used to record operations.
    """

    _MAX_ATTEMPTS = 5

    def __init__(self, calculator, error_logger, history) -> None:
        self._calculator = calculator
        self._error_logger = error_logger
        self._history = history
        self._retry_count = 0

    def increment_retry_count(self) -> bool:
        """Increment the consecutive-invalid-input counter.

        Returns:
            ``True`` when the counter has reached or exceeded ``_MAX_ATTEMPTS``,
            indicating the session should be terminated.
        """
        self._retry_count += 1
        return self._retry_count >= self._MAX_ATTEMPTS

    def reset_retry_count(self) -> None:
        """Reset the consecutive-invalid-input counter to zero."""
        self._retry_count = 0
