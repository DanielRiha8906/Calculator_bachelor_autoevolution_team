"""Retry wrappers for interactive calculator input.

Provides configurable retry loops around operation and operand prompts for
guided interactive mode.  Each wrapper tracks failed attempts, informs the
user how many attempts remain, and returns a sentinel value when the maximum
number of retries is reached.

These wrappers are used exclusively by :func:`~src.input_loop.run_loop`.  CLI
mode intentionally does not use retry logic — it validates once and exits on
any error.

This module does NOT import from :mod:`src.input_loop`.  The validator
callables (:func:`~src.input_loop.get_operation` and
:func:`~src.input_loop.get_operands`) are injected by the caller to avoid a
circular import.
"""

from __future__ import annotations

from typing import Callable

MAX_RETRIES: int = 3


def retry_get_operation(
    input_fn: Callable[[str], str] = input,
    max_retries: int = MAX_RETRIES,
    *,
    _get_operation_fn: Callable[[Callable[[str], str]], str | None] | None = None,
) -> str | None:
    """Wrap a ``get_operation``-style callable with a retry loop.

    Calls the operation-prompt callable up to *max_retries* times.  If the
    user enters an unrecognised operation the function prints how many attempts
    remain and prompts again.  If the user types ``"exit"`` the function
    returns ``None`` immediately without counting the attempt as a failure.

    Args:
        input_fn: Raw input callable (e.g. the built-in ``input``) forwarded
            to the operation-prompt callable.  Defaults to ``input``.
        max_retries: Maximum number of attempts allowed before giving up.
            Defaults to :data:`MAX_RETRIES`.
        _get_operation_fn: The ``get_operation`` callable to use.  Injected by
            :func:`~src.input_loop.run_loop` to avoid a circular import.  Must
            accept ``input_fn`` as its sole positional argument and return
            either a valid operation key, ``None`` (exit), or
            ``"__invalid__"``.

    Returns:
        The validated operation key string on success.  Returns ``None`` if the
        user typed ``"exit"``.  Returns ``"__exhausted__"`` when the maximum
        number of attempts is exceeded so that callers can distinguish
        exhaustion from a deliberate exit.
    """
    if _get_operation_fn is None:
        raise ValueError(
            "retry_get_operation requires _get_operation_fn to be provided."
        )

    for attempt in range(1, max_retries + 1):
        result = _get_operation_fn(input_fn)

        if result is None:
            # User typed "exit" — propagate immediately; not a failed attempt.
            return None

        if result != "__invalid__":
            return result

        remaining = max_retries - attempt
        if remaining > 0:
            print(f"Invalid operation. {remaining} attempt(s) remaining.")

    return "__exhausted__"


def retry_get_operands(
    count: int,
    input_fn: Callable[[str], str] = input,
    max_retries: int = MAX_RETRIES,
    *,
    _get_operands_fn: Callable[[int, Callable[[str], str]], list[float]] | None = None,
) -> list[float]:
    """Wrap a ``get_operands``-style callable with a single-attempt call.

    Calls the operand-prompt callable once and returns the result.  Any
    :exc:`ValueError` raised by the callable is propagated to the caller so
    that the outer loop can display the error and continue.

    .. note::
        Full retry behaviour for operands (multiple attempts with remaining-
        count feedback) is deferred to a future iteration.  The current
        implementation is a thin wrapper that preserves the existing
        :func:`~src.input_loop.run_loop` error-handling contract: a single
        bad operand causes an error message and the loop resumes from the
        top on the next iteration.

    Args:
        count: Number of operands to collect.  Forwarded to
            ``_get_operands_fn``.
        input_fn: Raw input callable forwarded to ``_get_operands_fn``.
            Defaults to ``input``.
        max_retries: Accepted for API consistency with :func:`retry_get_operation`
            but not currently used.
        _get_operands_fn: The ``get_operands`` callable to use.  Injected by
            :func:`~src.input_loop.run_loop` to avoid a circular import.  Must
            accept ``count`` and ``input_fn`` as positional arguments and
            return a list of floats or raise :exc:`ValueError`.

    Returns:
        A list of :class:`float` values on success.

    Raises:
        ValueError: Propagated directly from the underlying callable on
            invalid input.
    """
    if _get_operands_fn is None:
        raise ValueError(
            "retry_get_operands requires _get_operands_fn to be provided."
        )

    return _get_operands_fn(count, input_fn)
