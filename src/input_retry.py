"""Generic retry logic and input validation with attempt tracking.

Provides a configuration class, a reusable retry wrapper, and a custom
exception for when the retry limit is exceeded.  Contains no I/O itself;
all I/O is injected via callables so the module stays pure and testable.
"""

from dataclasses import dataclass
from typing import Callable, TypeVar

DEFAULT_MAX_RETRIES: int = 3

T = TypeVar("T")


class RetryLimitExceeded(Exception):
    """Raised by ``validate_with_retry`` when the attempt limit is exhausted."""


@dataclass
class InputRetryConfig:
    """Configuration for ``validate_with_retry``.

    Attributes:
        max_attempts: Maximum number of input attempts allowed (including the
            first).  Defaults to ``DEFAULT_MAX_RETRIES``.
    """

    max_attempts: int = DEFAULT_MAX_RETRIES


def validate_with_retry(
    input_fn: Callable[[], T],
    validator: Callable[[T], bool],
    error_formatter: Callable[[T, int, int], str],
    config: InputRetryConfig | None = None,
) -> T:
    """Repeatedly call *input_fn* until *validator* returns ``True`` or the
    attempt limit is reached.

    On each failed attempt, ``error_formatter`` is called with the invalid
    value, the current attempt number (1-based), and the maximum number of
    attempts; its return value is printed to stdout.

    Args:
        input_fn: Zero-argument callable that fetches a single input value.
        validator: Callable that accepts the value returned by *input_fn* and
            returns ``True`` if the value is acceptable, ``False`` otherwise.
            It may also raise an exception to signal invalidity — the exception
            is caught and treated the same as returning ``False``.
        error_formatter: Callable ``(value, attempt, max_attempts) -> str``
            used to format the error message printed on each failure.
        config: An ``InputRetryConfig`` instance.  If ``None``, a default
            instance (``DEFAULT_MAX_RETRIES`` attempts) is used.

    Returns:
        The first value accepted by *validator*.

    Raises:
        RetryLimitExceeded: When all allowed attempts have been exhausted
            without *validator* returning ``True``.
    """
    if config is None:
        config = InputRetryConfig()

    for attempt in range(1, config.max_attempts + 1):
        value = input_fn()
        try:
            valid = validator(value)
        except Exception:
            valid = False

        if valid:
            return value

        print(error_formatter(value, attempt, config.max_attempts))

    raise RetryLimitExceeded(
        f"Input validation failed after {config.max_attempts} attempt(s)."
    )
