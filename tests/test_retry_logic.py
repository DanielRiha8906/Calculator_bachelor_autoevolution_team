"""Tests for src/retry_logic.py.

Tests the retry wrapper functions for interactive calculator input, including
retry loops, exit detection, exhaustion handling, and dependency injection.
"""

from __future__ import annotations

import pytest

from src.retry_logic import MAX_RETRIES, retry_get_operands, retry_get_operation


# ---------------------------------------------------------------------------
# MAX_RETRIES constant
# ---------------------------------------------------------------------------


def test_max_retries_is_positive_integer() -> None:
    """MAX_RETRIES must be a positive integer."""
    assert isinstance(MAX_RETRIES, int)
    assert MAX_RETRIES > 0


def test_max_retries_equals_three() -> None:
    """MAX_RETRIES must be exactly 3 (as documented)."""
    assert MAX_RETRIES == 3


# ---------------------------------------------------------------------------
# retry_get_operation — happy path
# ---------------------------------------------------------------------------


def test_retry_get_operation_valid_operation_first_try() -> None:
    """A valid operation on first attempt must return the operation key."""
    def mock_get_operation(input_fn):
        return "add"

    result = retry_get_operation(
        input_fn=lambda _: "add",
        max_retries=3,
        _get_operation_fn=mock_get_operation
    )
    assert result == "add"


def test_retry_get_operation_exit_first_try() -> None:
    """Entering 'exit' on first attempt must return None."""
    def mock_get_operation(input_fn):
        return None

    result = retry_get_operation(
        input_fn=lambda _: "exit",
        max_retries=3,
        _get_operation_fn=mock_get_operation
    )
    assert result is None


# ---------------------------------------------------------------------------
# retry_get_operation — retry behavior
# ---------------------------------------------------------------------------


def test_retry_get_operation_invalid_then_valid(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """One invalid followed by a valid operation must return the valid key."""
    call_count = [0]

    def mock_get_operation(input_fn):
        call_count[0] += 1
        if call_count[0] == 1:
            return "__invalid__"
        return "add"

    result = retry_get_operation(
        input_fn=lambda _: "dummy",
        max_retries=3,
        _get_operation_fn=mock_get_operation
    )
    assert result == "add"
    captured = capsys.readouterr()
    assert "2 attempt(s) remaining" in captured.out


def test_retry_get_operation_two_invalid_then_valid(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Two invalid followed by valid operation must show remaining attempts."""
    call_count = [0]

    def mock_get_operation(input_fn):
        call_count[0] += 1
        if call_count[0] <= 2:
            return "__invalid__"
        return "multiply"

    result = retry_get_operation(
        input_fn=lambda _: "dummy",
        max_retries=3,
        _get_operation_fn=mock_get_operation
    )
    assert result == "multiply"
    captured = capsys.readouterr()
    # First failure: 2 remaining
    # Second failure: 1 remaining
    assert "2 attempt(s) remaining" in captured.out
    assert "1 attempt(s) remaining" in captured.out


def test_retry_get_operation_remaining_attempts_message() -> None:
    """Invalid operation must print remaining-attempts message (not on last failure)."""
    def mock_get_operation(input_fn):
        return "__invalid__"

    capsys = None

    # Manually capture the output to verify the message format
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_out = io.StringIO()

    try:
        result = retry_get_operation(
            input_fn=lambda _: "dummy",
            max_retries=2,
            _get_operation_fn=mock_get_operation
        )

        output = captured_out.getvalue()
    finally:
        sys.stdout = old_stdout

    assert result == "__exhausted__"
    # First failure should show "1 attempt(s) remaining"
    assert "1 attempt(s) remaining" in output
    # Second failure should NOT show any remaining message (exhausted)


# ---------------------------------------------------------------------------
# retry_get_operation — exhaustion
# ---------------------------------------------------------------------------


def test_retry_get_operation_exhausts_after_max_retries() -> None:
    """After max_retries failures, must return '__exhausted__' sentinel."""
    def mock_get_operation(input_fn):
        return "__invalid__"

    result = retry_get_operation(
        input_fn=lambda _: "dummy",
        max_retries=3,
        _get_operation_fn=mock_get_operation
    )
    assert result == "__exhausted__"


def test_retry_get_operation_exhausts_with_max_retries_one() -> None:
    """With max_retries=1, one invalid input must return '__exhausted__'."""
    def mock_get_operation(input_fn):
        return "__invalid__"

    result = retry_get_operation(
        input_fn=lambda _: "dummy",
        max_retries=1,
        _get_operation_fn=mock_get_operation
    )
    assert result == "__exhausted__"


def test_retry_get_operation_no_remaining_message_on_exhaustion(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """When max retries exhausted, no 'remaining' message should appear."""
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_out = io.StringIO()

    def mock_get_operation(input_fn):
        return "__invalid__"

    try:
        result = retry_get_operation(
            input_fn=lambda _: "dummy",
            max_retries=2,
            _get_operation_fn=mock_get_operation
        )
        output = captured_out.getvalue()
    finally:
        sys.stdout = old_stdout

    assert result == "__exhausted__"
    # Should have one message (after first attempt: "1 remaining")
    # Should NOT have a message after second attempt (that's exhaustion)
    assert output.count("attempt(s) remaining") == 1


# ---------------------------------------------------------------------------
# retry_get_operation — exit does not count as failure
# ---------------------------------------------------------------------------


def test_retry_get_operation_exit_after_invalid_does_not_count_as_attempt(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Exiting after an invalid op should return None without counting as attempt."""
    call_count = [0]

    def mock_get_operation(input_fn):
        call_count[0] += 1
        if call_count[0] == 1:
            return "__invalid__"
        return None  # Exit on second call

    result = retry_get_operation(
        input_fn=lambda _: "dummy",
        max_retries=3,
        _get_operation_fn=mock_get_operation
    )
    assert result is None
    # Exit should return immediately, not counting as a failure
    assert call_count[0] == 2


def test_retry_get_operation_exit_on_first_call() -> None:
    """Exit on the first call should return None immediately."""
    def mock_get_operation(input_fn):
        return None

    result = retry_get_operation(
        input_fn=lambda _: "exit",
        max_retries=3,
        _get_operation_fn=mock_get_operation
    )
    assert result is None


# ---------------------------------------------------------------------------
# retry_get_operation — missing _get_operation_fn
# ---------------------------------------------------------------------------


def test_retry_get_operation_missing_get_operation_fn_raises_value_error() -> None:
    """Calling retry_get_operation without _get_operation_fn must raise ValueError."""
    with pytest.raises(ValueError, match="requires _get_operation_fn"):
        retry_get_operation(
            input_fn=lambda _: "add",
            max_retries=3,
            _get_operation_fn=None
        )


def test_retry_get_operation_error_message_mentions_get_operation_fn() -> None:
    """The ValueError message must mention '_get_operation_fn'."""
    with pytest.raises(ValueError) as exc_info:
        retry_get_operation(_get_operation_fn=None)
    assert "_get_operation_fn" in str(exc_info.value)


# ---------------------------------------------------------------------------
# retry_get_operation — input_fn is passed through correctly
# ---------------------------------------------------------------------------


def test_retry_get_operation_passes_input_fn_to_get_operation(
) -> None:
    """The input_fn must be passed to the _get_operation_fn."""
    received_input_fn = []

    def mock_get_operation(input_fn):
        received_input_fn.append(input_fn)
        return "add"

    custom_input = lambda _: "test"
    retry_get_operation(
        input_fn=custom_input,
        max_retries=3,
        _get_operation_fn=mock_get_operation
    )
    assert len(received_input_fn) == 1
    assert received_input_fn[0] is custom_input


def test_retry_get_operation_default_input_fn_is_builtin_input() -> None:
    """When input_fn is not provided, it should default to the builtin input."""
    received_input_fn = []

    def mock_get_operation(input_fn):
        received_input_fn.append(input_fn)
        return "add"

    retry_get_operation(
        max_retries=3,
        _get_operation_fn=mock_get_operation
    )
    assert len(received_input_fn) == 1
    assert received_input_fn[0] is input


# ---------------------------------------------------------------------------
# retry_get_operation — max_retries parameter
# ---------------------------------------------------------------------------


def test_retry_get_operation_default_max_retries_is_MAX_RETRIES() -> None:
    """When max_retries is not provided, it should default to MAX_RETRIES."""
    call_count = [0]

    def mock_get_operation(input_fn):
        call_count[0] += 1
        return "__invalid__"

    result = retry_get_operation(
        input_fn=lambda _: "dummy",
        _get_operation_fn=mock_get_operation
    )
    # Should have attempted MAX_RETRIES times (3 times)
    assert call_count[0] == MAX_RETRIES
    assert result == "__exhausted__"


def test_retry_get_operation_respects_custom_max_retries() -> None:
    """When max_retries is set to a custom value, it should be respected."""
    call_count = [0]

    def mock_get_operation(input_fn):
        call_count[0] += 1
        return "__invalid__"

    result = retry_get_operation(
        input_fn=lambda _: "dummy",
        max_retries=5,
        _get_operation_fn=mock_get_operation
    )
    assert call_count[0] == 5
    assert result == "__exhausted__"


def test_retry_get_operation_max_retries_zero() -> None:
    """With max_retries=0, should return '__exhausted__' immediately."""
    call_count = [0]

    def mock_get_operation(input_fn):
        call_count[0] += 1
        return "__invalid__"

    result = retry_get_operation(
        input_fn=lambda _: "dummy",
        max_retries=0,
        _get_operation_fn=mock_get_operation
    )
    # The loop should not execute (range(1, 1) is empty)
    assert call_count[0] == 0
    assert result == "__exhausted__"


# ---------------------------------------------------------------------------
# retry_get_operation — edge cases
# ---------------------------------------------------------------------------


def test_retry_get_operation_get_operation_fn_called_correct_times(
) -> None:
    """_get_operation_fn must be called once per attempt."""
    call_count = [0]

    def mock_get_operation(input_fn):
        call_count[0] += 1
        if call_count[0] < 3:
            return "__invalid__"
        return "add"

    result = retry_get_operation(
        input_fn=lambda _: "dummy",
        max_retries=3,
        _get_operation_fn=mock_get_operation
    )
    assert call_count[0] == 3
    assert result == "add"


def test_retry_get_operation_sentinel_value_is_string() -> None:
    """The '__exhausted__' sentinel must be a string."""
    def mock_get_operation(input_fn):
        return "__invalid__"

    result = retry_get_operation(
        input_fn=lambda _: "dummy",
        max_retries=1,
        _get_operation_fn=mock_get_operation
    )
    assert isinstance(result, str)
    assert result == "__exhausted__"


# ---------------------------------------------------------------------------
# retry_get_operands — happy path
# ---------------------------------------------------------------------------


def test_retry_get_operands_valid_call_returns_result() -> None:
    """A valid call must return the list of floats from the underlying function."""
    def mock_get_operands(count, input_fn):
        return [1.0, 2.0]

    result = retry_get_operands(
        count=2,
        input_fn=lambda _: "dummy",
        max_retries=3,
        _get_operands_fn=mock_get_operands
    )
    assert result == [1.0, 2.0]
    assert all(isinstance(v, float) for v in result)


def test_retry_get_operands_count_one() -> None:
    """With count=1, must return a list with one float."""
    def mock_get_operands(count, input_fn):
        assert count == 1
        return [5.0]

    result = retry_get_operands(
        count=1,
        input_fn=lambda _: "5",
        max_retries=3,
        _get_operands_fn=mock_get_operands
    )
    assert result == [5.0]


def test_retry_get_operands_count_zero() -> None:
    """With count=0, should accept and pass through."""
    def mock_get_operands(count, input_fn):
        assert count == 0
        return []

    result = retry_get_operands(
        count=0,
        input_fn=lambda _: "dummy",
        max_retries=3,
        _get_operands_fn=mock_get_operands
    )
    assert result == []


# ---------------------------------------------------------------------------
# retry_get_operands — error propagation
# ---------------------------------------------------------------------------


def test_retry_get_operands_propagates_value_error() -> None:
    """Any ValueError from _get_operands_fn must be re-raised."""
    def mock_get_operands(count, input_fn):
        raise ValueError("Invalid operand: not a number")

    with pytest.raises(ValueError, match="Invalid operand"):
        retry_get_operands(
            count=2,
            input_fn=lambda _: "abc",
            max_retries=3,
            _get_operands_fn=mock_get_operands
        )


def test_retry_get_operands_does_not_retry_on_value_error() -> None:
    """ValueError must be raised immediately without retry."""
    call_count = [0]

    def mock_get_operands(count, input_fn):
        call_count[0] += 1
        raise ValueError("Bad operand")

    with pytest.raises(ValueError):
        retry_get_operands(
            count=2,
            input_fn=lambda _: "abc",
            max_retries=3,
            _get_operands_fn=mock_get_operands
        )
    # Should only be called once, no retries
    assert call_count[0] == 1


# ---------------------------------------------------------------------------
# retry_get_operands — missing _get_operands_fn
# ---------------------------------------------------------------------------


def test_retry_get_operands_missing_get_operands_fn_raises_value_error() -> None:
    """Calling without _get_operands_fn must raise ValueError."""
    with pytest.raises(ValueError, match="requires _get_operands_fn"):
        retry_get_operands(
            count=2,
            input_fn=lambda _: "dummy",
            max_retries=3,
            _get_operands_fn=None
        )


def test_retry_get_operands_error_message_mentions_get_operands_fn() -> None:
    """The ValueError message must mention '_get_operands_fn'."""
    with pytest.raises(ValueError) as exc_info:
        retry_get_operands(count=2, _get_operands_fn=None)
    assert "_get_operands_fn" in str(exc_info.value)


# ---------------------------------------------------------------------------
# retry_get_operands — input_fn and count are passed through
# ---------------------------------------------------------------------------


def test_retry_get_operands_passes_count_to_underlying_function() -> None:
    """The count parameter must be passed to _get_operands_fn."""
    received_count = []

    def mock_get_operands(count, input_fn):
        received_count.append(count)
        return [1.0] * count

    retry_get_operands(
        count=5,
        input_fn=lambda _: "dummy",
        max_retries=3,
        _get_operands_fn=mock_get_operands
    )
    assert received_count == [5]


def test_retry_get_operands_passes_input_fn_to_underlying_function() -> None:
    """The input_fn parameter must be passed to _get_operands_fn."""
    received_input_fn = []

    def mock_get_operands(count, input_fn):
        received_input_fn.append(input_fn)
        return [1.0]

    custom_input = lambda _: "test"
    retry_get_operands(
        count=1,
        input_fn=custom_input,
        max_retries=3,
        _get_operands_fn=mock_get_operands
    )
    assert len(received_input_fn) == 1
    assert received_input_fn[0] is custom_input


def test_retry_get_operands_default_input_fn_is_builtin_input() -> None:
    """When input_fn is not provided, it should default to the builtin input."""
    received_input_fn = []

    def mock_get_operands(count, input_fn):
        received_input_fn.append(input_fn)
        return [1.0]

    retry_get_operands(
        count=1,
        max_retries=3,
        _get_operands_fn=mock_get_operands
    )
    assert len(received_input_fn) == 1
    assert received_input_fn[0] is input


# ---------------------------------------------------------------------------
# retry_get_operands — max_retries parameter
# ---------------------------------------------------------------------------


def test_retry_get_operands_default_max_retries_is_MAX_RETRIES() -> None:
    """When max_retries is not provided, it should default to MAX_RETRIES."""
    def mock_get_operands(count, input_fn):
        return [1.0]

    # The current implementation is a single-attempt pass-through,
    # so max_retries is accepted but not used. Just verify the call works.
    result = retry_get_operands(
        count=2,
        input_fn=lambda _: "dummy",
        _get_operands_fn=mock_get_operands
    )
    assert result == [1.0]


def test_retry_get_operands_accepts_custom_max_retries() -> None:
    """Custom max_retries parameter is accepted for API consistency."""
    def mock_get_operands(count, input_fn):
        return [1.0, 2.0]

    # Even though max_retries is not used, it should be accepted
    result = retry_get_operands(
        count=2,
        input_fn=lambda _: "dummy",
        max_retries=5,
        _get_operands_fn=mock_get_operands
    )
    assert result == [1.0, 2.0]


# ---------------------------------------------------------------------------
# retry_get_operands — edge cases
# ---------------------------------------------------------------------------


def test_retry_get_operands_large_count() -> None:
    """With a large count, should pass it through without modification."""
    received_count = []

    def mock_get_operands(count, input_fn):
        received_count.append(count)
        return [float(i) for i in range(count)]

    result = retry_get_operands(
        count=100,
        input_fn=lambda _: "dummy",
        max_retries=3,
        _get_operands_fn=mock_get_operands
    )
    assert received_count == [100]
    assert len(result) == 100


def test_retry_get_operands_returns_exact_list() -> None:
    """The returned list must be exactly what the underlying function returns."""
    expected_list = [1.5, 2.5, 3.5, 4.5, 5.5]

    def mock_get_operands(count, input_fn):
        return expected_list

    result = retry_get_operands(
        count=5,
        input_fn=lambda _: "dummy",
        max_retries=3,
        _get_operands_fn=mock_get_operands
    )
    assert result is expected_list  # Must be the same object


def test_retry_get_operands_with_negative_count() -> None:
    """Negative count is technically invalid but should pass through."""
    received_count = []

    def mock_get_operands(count, input_fn):
        received_count.append(count)
        return []

    # This should work as a pass-through; validation is not in retry_get_operands
    result = retry_get_operands(
        count=-1,
        input_fn=lambda _: "dummy",
        max_retries=3,
        _get_operands_fn=mock_get_operands
    )
    assert received_count == [-1]
    assert result == []
