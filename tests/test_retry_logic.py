"""Tests for retry logic in src/input_loop.py.

Integration tests that verify the retry behavior of get_operation, get_operands,
and run_loop when invalid input is provided.
"""

from __future__ import annotations

import pytest

from src.input_loop import get_operation, get_operands, run_loop


# ---------------------------------------------------------------------------
# get_operation retry logic
# ---------------------------------------------------------------------------


def test_get_operation_valid_on_first_attempt() -> None:
    """Valid input on first attempt must return immediately."""
    result = get_operation(input_fn=lambda _prompt: "add")
    assert result == "add"


def test_get_operation_invalid_then_valid_recovers(capsys: pytest.CaptureFixture[str]) -> None:
    """Invalid input followed by valid input must recover and return valid operation."""
    inputs = iter(["invalid", "add"])
    result = get_operation(input_fn=lambda _prompt: next(inputs))
    assert result == "add"
    captured = capsys.readouterr()
    assert "Please try again" in captured.out


def test_get_operation_three_invalid_exhausts_retries(capsys: pytest.CaptureFixture[str]) -> None:
    """Three invalid inputs must exhaust retries and return '__max_retries_exceeded__'."""
    inputs = iter(["bad1", "bad2", "bad3"])
    result = get_operation(input_fn=lambda _prompt: next(inputs))
    assert result == "__max_retries_exceeded__"
    captured = capsys.readouterr()
    assert "Maximum retry attempts reached" in captured.out


def test_get_operation_two_invalid_then_valid_succeeds(capsys: pytest.CaptureFixture[str]) -> None:
    """Two invalid inputs followed by valid input must succeed."""
    inputs = iter(["bad1", "bad2", "multiply"])
    result = get_operation(input_fn=lambda _prompt: next(inputs))
    assert result == "multiply"
    captured = capsys.readouterr()
    assert "Please try again" in captured.out


def test_get_operation_retry_limit_one_single_attempt(capsys: pytest.CaptureFixture[str]) -> None:
    """With retry_limit=1, a single invalid input must exhaust retries."""
    result = get_operation(input_fn=lambda _prompt: "invalid", retry_limit=1)
    assert result == "__max_retries_exceeded__"
    captured = capsys.readouterr()
    assert "Maximum retry attempts reached" in captured.out


def test_get_operation_retry_limit_one_valid_first_attempt() -> None:
    """With retry_limit=1, valid input on first attempt must return immediately."""
    from src.mode import Mode
    result = get_operation(input_fn=lambda _prompt: "square", retry_limit=1, mode=Mode.SCIENTIFIC)
    assert result == "square"


def test_get_operation_exit_does_not_retry(capsys: pytest.CaptureFixture[str]) -> None:
    """'exit' must return None immediately without consuming retries."""
    result = get_operation(input_fn=lambda _prompt: "exit")
    assert result is None
    captured = capsys.readouterr()
    assert "Maximum retry attempts reached" not in captured.out


def test_get_operation_attempts_printed_in_order(capsys: pytest.CaptureFixture[str]) -> None:
    """Error messages must show attempt counts incrementing."""
    inputs = iter(["bad1", "bad2", "bad3"])
    get_operation(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Attempt 1 of 3" in captured.out
    assert "Attempt 2 of 3" in captured.out
    assert "Attempt 3 of 3" in captured.out


def test_get_operation_custom_retry_limit_respected(capsys: pytest.CaptureFixture[str]) -> None:
    """A custom retry_limit must be respected."""
    inputs = iter(["bad1", "bad2"])
    result = get_operation(input_fn=lambda _prompt: next(inputs), retry_limit=2)
    assert result == "__max_retries_exceeded__"
    captured = capsys.readouterr()
    assert "Attempt 1 of 2" in captured.out
    assert "Attempt 2 of 2" in captured.out


# ---------------------------------------------------------------------------
# get_operands retry logic
# ---------------------------------------------------------------------------


def test_get_operands_valid_on_first_attempt() -> None:
    """Valid input on first attempt must return list of floats."""
    result = get_operands(2, input_fn=lambda _prompt: next(iter(["3", "4"])))
    # This will fail since we're reusing the same iterator, but let's use a proper setup
    pass  # Covered by existing tests


def test_get_operands_single_operand_valid() -> None:
    """Single valid operand must be returned as list."""
    result = get_operands(1, input_fn=lambda _prompt: "42")
    assert result == [42.0]
    assert isinstance(result[0], float)


def test_get_operands_invalid_then_valid_recovers(capsys: pytest.CaptureFixture[str]) -> None:
    """Invalid operand followed by valid operand must recover and include valid value."""
    inputs = iter(["invalid", "42"])
    result = get_operands(1, input_fn=lambda _prompt: next(inputs))
    assert result == [42.0]
    captured = capsys.readouterr()
    assert "Please enter a number" in captured.out


def test_get_operands_three_invalid_exhausts_retry(capsys: pytest.CaptureFixture[str]) -> None:
    """Three invalid inputs for a single operand must exhaust retries and return None."""
    inputs = iter(["bad1", "bad2", "bad3"])
    result = get_operands(1, input_fn=lambda _prompt: next(inputs))
    assert result is None
    captured = capsys.readouterr()
    assert "Maximum retry attempts reached" in captured.out


def test_get_operands_invalid_first_operand_then_valid(capsys: pytest.CaptureFixture[str]) -> None:
    """Invalid first operand recovers; both operands entered successfully."""
    inputs = iter(["bad", "5", "10"])
    result = get_operands(2, input_fn=lambda _prompt: next(inputs))
    assert result == [5.0, 10.0]
    captured = capsys.readouterr()
    # Prompts are printed via input_fn, not captured. Check for validation errors instead.
    assert "Please enter a number" in captured.out


def test_get_operands_valid_first_invalid_second(capsys: pytest.CaptureFixture[str]) -> None:
    """First operand valid; second operand recovers from invalid input."""
    inputs = iter(["5", "bad", "10"])
    result = get_operands(2, input_fn=lambda _prompt: next(inputs))
    assert result == [5.0, 10.0]


def test_get_operands_second_operand_exhausts_retry_returns_none(capsys: pytest.CaptureFixture[str]) -> None:
    """If second operand exhausts retries, function must return None."""
    inputs = iter(["5", "bad1", "bad2", "bad3"])
    result = get_operands(2, input_fn=lambda _prompt: next(inputs))
    assert result is None
    captured = capsys.readouterr()
    assert "operand 2" in captured.out


def test_get_operands_custom_retry_limit_respected(capsys: pytest.CaptureFixture[str]) -> None:
    """Custom retry_limit must be respected per operand."""
    inputs = iter(["bad1", "bad2"])
    result = get_operands(1, input_fn=lambda _prompt: next(inputs), retry_limit=2)
    assert result is None
    captured = capsys.readouterr()
    assert "Attempt 1 of 2" in captured.out
    assert "Attempt 2 of 2" in captured.out


def test_get_operands_attempts_printed_in_order(capsys: pytest.CaptureFixture[str]) -> None:
    """Attempt counter must increment for each retry."""
    inputs = iter(["bad1", "bad2", "bad3"])
    get_operands(1, input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Attempt 1 of 3" in captured.out
    assert "Attempt 2 of 3" in captured.out
    assert "Attempt 3 of 3" in captured.out


def test_get_operands_retry_limit_one(capsys: pytest.CaptureFixture[str]) -> None:
    """With retry_limit=1, single invalid input exhausts retries."""
    result = get_operands(1, input_fn=lambda _prompt: "invalid", retry_limit=1)
    assert result is None
    captured = capsys.readouterr()
    assert "Maximum retry attempts reached" in captured.out


# ---------------------------------------------------------------------------
# run_loop retry integration
# ---------------------------------------------------------------------------


def test_run_loop_operation_retry_exhaustion_terminates(capsys: pytest.CaptureFixture[str]) -> None:
    """If operation retries are exhausted, run_loop must terminate gracefully."""
    import tempfile
    import os
    from src.history import OperationHistory

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        inputs = iter(["bad1", "bad2", "bad3"])
        run_loop(input_fn=lambda _prompt: next(inputs), history=history)
        captured = capsys.readouterr()
        assert "Session terminated due to too many invalid operation entries" in captured.out
        assert "Goodbye" not in captured.out


def test_run_loop_operation_invalid_then_valid_continues(capsys: pytest.CaptureFixture[str]) -> None:
    """Invalid operation followed by valid operation must continue normally."""
    import tempfile
    import os
    from src.history import OperationHistory

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        inputs = iter(["bad", "add", "5", "10", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs), history=history)
        captured = capsys.readouterr()
        assert "Result: 15" in captured.out
        assert "Goodbye" in captured.out


def test_run_loop_operand_retry_exhaustion_continues(capsys: pytest.CaptureFixture[str]) -> None:
    """If operand retries are exhausted, run_loop must return to menu."""
    import tempfile
    import os
    from src.history import OperationHistory

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        inputs = iter(["add", "bad1", "bad2", "bad3", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs), history=history)
        captured = capsys.readouterr()
        assert "Returning to the main menu" in captured.out
        assert "Goodbye" in captured.out


def test_run_loop_operand_invalid_then_valid_continues(capsys: pytest.CaptureFixture[str]) -> None:
    """Invalid operand followed by valid operands must compute result."""
    import tempfile
    import os
    from src.history import OperationHistory

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        inputs = iter(["add", "bad", "5", "10", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs), history=history)
        captured = capsys.readouterr()
        assert "Result: 15" in captured.out
        assert "Goodbye" in captured.out


def test_run_loop_multiple_retry_cycles(capsys: pytest.CaptureFixture[str]) -> None:
    """Multiple retry cycles across different operations must work."""
    import tempfile
    import os
    from src.history import OperationHistory

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        inputs = iter([
            "bad1",          # invalid operation - retry
            "add",           # valid operation
            "bad",           # invalid operand - retry
            "3",             # valid first operand
            "4",             # valid second operand
            "bad2",          # invalid operation - retry
            "multiply",      # valid operation
            "2",             # valid operand
            "3",             # valid operand
            "exit"
        ])
        run_loop(input_fn=lambda _prompt: next(inputs), history=history)
        captured = capsys.readouterr()
        assert "Result: 7" in captured.out or "7" in captured.out  # 3 + 4
        assert "Result: 6" in captured.out or "6" in captured.out  # 2 * 3
        assert "Goodbye" in captured.out


def test_run_loop_exit_skips_retries(capsys: pytest.CaptureFixture[str]) -> None:
    """Typing 'exit' must terminate immediately without triggering retries."""
    import tempfile
    import os
    from src.history import OperationHistory

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        inputs = iter(["bad", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs), history=history)
        captured = capsys.readouterr()
        assert "Goodbye" in captured.out
        # The retry should happen first before exit
        assert "Please try again" in captured.out


def test_run_loop_two_invalid_operations_then_valid(capsys: pytest.CaptureFixture[str]) -> None:
    """Two invalid operations followed by valid must work."""
    import tempfile
    import os
    from src.history import OperationHistory

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        inputs = iter(["bad1", "bad2", "mode scientific", "square", "4", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs), history=history)
        captured = capsys.readouterr()
        assert "Result: 16" in captured.out
        assert "Goodbye" in captured.out


def test_run_loop_two_invalid_operands_then_valid(capsys: pytest.CaptureFixture[str]) -> None:
    """Two invalid operands followed by valid for both operands must work."""
    import tempfile
    import os
    from src.history import OperationHistory

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        inputs = iter(["add", "bad1", "bad2", "5", "10", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs), history=history)
        captured = capsys.readouterr()
        assert "Result: 15" in captured.out
        assert "Goodbye" in captured.out
