"""Tests for retry logic in src/input_handler.py.

Covers:
- MAX_RETRIES constant importability and value
- InputHandler.run() with invalid operation inputs up to MAX_RETRIES
- InputHandler.run() with counter reset on valid operation
- InputHandler._prompt_operands() with invalid operand inputs up to MAX_RETRIES
- Error message content (available operations list, per-attempt error messages)
- Edge cases: exactly MAX_RETRIES, MAX_RETRIES - 1, empty strings, whitespace

All tests use the injectable input_fn parameter; builtins.input is never patched.
"""

import pytest

from src.calculator import Calculator
from src.input_handler import InputHandler, MAX_RETRIES, OPERATIONS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input_fn(responses: list[str]):
    """Return a callable that yields successive strings from *responses*."""
    it = iter(responses)

    def _input_fn(prompt: str = "") -> str:  # noqa: ARG001
        return next(it)

    return _input_fn


@pytest.fixture
def calc() -> Calculator:
    return Calculator()


# ---------------------------------------------------------------------------
# MAX_RETRIES constant
# ---------------------------------------------------------------------------

def test_max_retries_is_importable():
    """MAX_RETRIES must be importable from src.input_handler."""
    from src.input_handler import MAX_RETRIES
    assert isinstance(MAX_RETRIES, int)


def test_max_retries_equals_five():
    """MAX_RETRIES must equal 5 as per the specification."""
    assert MAX_RETRIES == 5


# ---------------------------------------------------------------------------
# run() — invalid operations up to MAX_RETRIES
# ---------------------------------------------------------------------------

def test_run_exactly_max_retries_invalid_ops_terminates(calc, capsys):
    """Exactly MAX_RETRIES (5) invalid operations must terminate with message."""
    invalid_ops = ["badop1", "badop2", "badop3", "badop4", "badop5"]
    handler = InputHandler(calc, make_input_fn(invalid_ops))
    handler.run()
    out = capsys.readouterr().out
    assert "Too many invalid attempts. Ending session." in out


def test_run_max_retries_minus_one_invalid_ops_allows_exit(calc, capsys):
    """MAX_RETRIES - 1 (4) invalid operations followed by exit must NOT terminate."""
    invalid_ops = ["badop1", "badop2", "badop3", "badop4", "exit"]
    handler = InputHandler(calc, make_input_fn(invalid_ops))
    handler.run()
    out = capsys.readouterr().out
    # Should reach exit normally, not the "Too many invalid attempts" message
    assert "Too many invalid attempts. Ending session." not in out
    assert "Goodbye!" in out


def test_run_counter_reset_on_valid_operation(calc, capsys):
    """Valid operation must reset op_attempts counter.

    Scenario: 4 invalid ops, then 1 valid op, then 4 more invalid ops.
    Since the counter resets after the valid op, it should not reach MAX_RETRIES
    again and session should end cleanly with exit.
    """
    sequence = ["bad1", "bad2", "bad3", "bad4", "add", "1", "2", "bad5", "bad6", "bad7", "bad8", "exit"]
    handler = InputHandler(calc, make_input_fn(sequence))
    handler.run()
    out = capsys.readouterr().out
    # Should have completed the 'add' operation
    assert "Result:" in out
    assert "3" in out
    # Should NOT have reached the "Too many invalid attempts" endpoint
    assert "Too many invalid attempts. Ending session." not in out
    assert "Goodbye!" in out


def test_run_invalid_op_error_message_contains_available_ops(calc, capsys):
    """Error message on invalid operation must list available operations."""
    handler = InputHandler(calc, make_input_fn(["unknownop", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    # Should mention that available operations are listed
    assert "Available operations:" in out
    # Should list at least one known operation
    assert "add" in out


def test_run_each_invalid_op_prints_error(calc, capsys):
    """Each invalid operation must print an error message."""
    invalid_ops = ["bad1", "bad2", "bad3", "exit"]
    handler = InputHandler(calc, make_input_fn(invalid_ops))
    handler.run()
    out = capsys.readouterr().out
    # Three invalid ops should produce at least 3 error lines
    assert out.count("Error:") >= 3


def test_run_exactly_max_retries_with_leading_valid(calc, capsys):
    """Valid operation followed by MAX_RETRIES invalid should terminate."""
    sequence = ["add", "1", "2", "bad1", "bad2", "bad3", "bad4", "bad5"]
    handler = InputHandler(calc, make_input_fn(sequence))
    handler.run()
    out = capsys.readouterr().out
    # Should have the valid result first
    assert "Result:" in out
    assert "3" in out
    # Then should hit MAX_RETRIES on the invalid ops
    assert "Too many invalid attempts. Ending session." in out


def test_run_invalid_ops_empty_strings(calc, capsys):
    """Empty string as operation input should count toward retry limit."""
    sequence = ["", "", "", "", "", "exit"]
    handler = InputHandler(calc, make_input_fn(sequence))
    handler.run()
    out = capsys.readouterr().out
    # Five empty strings should trigger the termination
    assert "Too many invalid attempts. Ending session." in out


def test_run_invalid_ops_whitespace_only(calc, capsys):
    """Whitespace-only operation strings should count toward retry limit."""
    sequence = ["   ", "  \t  ", "\t\t", "   ", "   ", "exit"]
    handler = InputHandler(calc, make_input_fn(sequence))
    handler.run()
    out = capsys.readouterr().out
    # Five whitespace-only strings that strip to empty should trigger termination
    # (after .strip().lower(), "   " becomes "")
    assert "Too many invalid attempts. Ending session." in out


# ---------------------------------------------------------------------------
# _prompt_operands() — invalid operands up to MAX_RETRIES
# ---------------------------------------------------------------------------

def test_prompt_operands_exactly_max_retries_invalid_raises(calc):
    """Exactly MAX_RETRIES (5) invalid operand inputs must raise ValueError."""
    invalid_inputs = ["notnum1", "notnum2", "notnum3", "notnum4", "notnum5"]
    handler = InputHandler(calc, make_input_fn(invalid_inputs))
    with pytest.raises(ValueError, match="Too many invalid attempts for operand"):
        handler._prompt_operands(1, float)


def test_prompt_operands_max_retries_minus_one_then_valid(calc):
    """MAX_RETRIES - 1 (4) invalid operands followed by valid should succeed."""
    sequence = ["bad1", "bad2", "bad3", "bad4", "5.5"]
    handler = InputHandler(calc, make_input_fn(sequence))
    result = handler._prompt_operands(1, float)
    assert result == [5.5]


def test_prompt_operands_invalid_error_printed_each_time(calc, capsys):
    """Each invalid operand attempt must print an error before final failure."""
    invalid_inputs = ["x", "y", "z", "a", "b"]
    handler = InputHandler(calc, make_input_fn(invalid_inputs))
    with pytest.raises(ValueError, match="Too many invalid attempts for operand"):
        handler._prompt_operands(1, float)
    out = capsys.readouterr().out
    # Should print error 5 times for 5 failed attempts
    assert out.count("Error:") >= 5


def test_prompt_operands_arity_2_fails_on_first_operand(calc):
    """Failing on first operand (arity 2) should raise after MAX_RETRIES."""
    invalid_first = ["bad1", "bad2", "bad3", "bad4", "bad5"]
    handler = InputHandler(calc, make_input_fn(invalid_first))
    with pytest.raises(ValueError, match="Too many invalid attempts for operand"):
        handler._prompt_operands(2, float)


def test_prompt_operands_arity_2_fails_on_second_operand(calc):
    """Failing on second operand (arity 2) should raise after MAX_RETRIES."""
    sequence = ["1.0"] + ["bad1", "bad2", "bad3", "bad4", "bad5"]
    handler = InputHandler(calc, make_input_fn(sequence))
    with pytest.raises(ValueError, match="Too many invalid attempts for operand"):
        handler._prompt_operands(2, float)


def test_prompt_operands_succeeds_after_some_failures(calc):
    """Valid operand after 2 failures should succeed."""
    sequence = ["invalid1", "invalid2", "3.14"]
    handler = InputHandler(calc, make_input_fn(sequence))
    result = handler._prompt_operands(1, float)
    assert result == [3.14]


def test_prompt_operands_empty_string_counts_as_invalid(calc):
    """Empty string operand should count as invalid attempt."""
    sequence = ["", "", "", "", "", "exit"]
    handler = InputHandler(calc, make_input_fn(sequence))
    with pytest.raises(ValueError, match="Too many invalid attempts for operand"):
        handler._prompt_operands(1, float)


def test_prompt_operands_whitespace_only_string_counts_as_invalid(calc):
    """Whitespace-only operand string should count as invalid attempt."""
    sequence = ["  ", "\t", "   ", "\n", "  ", "exit"]
    handler = InputHandler(calc, make_input_fn(sequence))
    with pytest.raises(ValueError, match="Too many invalid attempts for operand"):
        handler._prompt_operands(1, float)


def test_prompt_operands_int_coerce_max_retries(calc):
    """Exact MAX_RETRIES failures with int coerce should raise."""
    invalid_ints = ["3.5", "1.2", "abc", "12.34", "xyz"]
    handler = InputHandler(calc, make_input_fn(invalid_ints))
    with pytest.raises(ValueError, match="Too many invalid attempts for operand"):
        handler._prompt_operands(1, int)


# ---------------------------------------------------------------------------
# Integration: run() with operand retries
# ---------------------------------------------------------------------------

def test_run_invalid_operands_within_limit_allows_valid(calc, capsys):
    """Invalid operands fewer than MAX_RETRIES should allow continuation."""
    sequence = ["add", "bad1", "bad2", "1", "2", "exit"]
    handler = InputHandler(calc, make_input_fn(sequence))
    handler.run()
    out = capsys.readouterr().out
    # Should recover and complete the operation
    assert "Result:" in out
    assert "3" in out
    assert "Goodbye!" in out


def test_run_invalid_operands_at_max_retries_terminates(calc, capsys):
    """MAX_RETRIES invalid operands should terminate the operation."""
    sequence = ["add", "bad1", "bad2", "bad3", "bad4", "bad5"]
    handler = InputHandler(calc, make_input_fn(sequence))
    handler.run()
    out = capsys.readouterr().out
    # Should print the ValueError message caught in run()
    assert "Too many invalid attempts for operand" in out


def test_run_mixed_invalid_ops_and_operands(calc, capsys):
    """Mix of invalid ops and invalid operands within limits should work."""
    sequence = ["badop", "badop2", "add", "bad_operand", "5", "10", "exit"]
    handler = InputHandler(calc, make_input_fn(sequence))
    handler.run()
    out = capsys.readouterr().out
    # Should recover from both types of errors and complete
    assert "Result:" in out
    assert "15" in out
    assert "Goodbye!" in out


# ---------------------------------------------------------------------------
# Boundary conditions: exactly at the limit
# ---------------------------------------------------------------------------

def test_run_exactly_four_invalid_ops_then_fifth_valid(calc, capsys):
    """Four invalid ops followed by valid operation should succeed."""
    sequence = ["bad1", "bad2", "bad3", "bad4", "add", "7", "8", "exit"]
    handler = InputHandler(calc, make_input_fn(sequence))
    handler.run()
    out = capsys.readouterr().out
    assert "Result:" in out
    assert "15" in out
    assert "Goodbye!" in out


def test_run_exactly_five_invalid_ops_terminates_cleanly(calc, capsys):
    """Exactly five invalid ops should terminate with the specific message."""
    sequence = ["bad1", "bad2", "bad3", "bad4", "bad5"]
    handler = InputHandler(calc, make_input_fn(sequence))
    handler.run()
    out = capsys.readouterr().out
    assert "Too many invalid attempts. Ending session." in out
    # Should NOT contain "Goodbye!" because we break, not proceed to normal exit
    # (Goodbye is only printed on clean exit or StopIteration)


def test_prompt_operands_exactly_four_invalid_then_valid(calc):
    """Four invalid operands followed by valid should succeed."""
    sequence = ["x", "y", "z", "w", "42"]
    handler = InputHandler(calc, make_input_fn(sequence))
    result = handler._prompt_operands(1, float)
    assert result == [42.0]


def test_prompt_operands_exactly_five_invalid_terminates(calc):
    """Five consecutive invalid operands should raise."""
    sequence = ["a", "b", "c", "d", "e"]
    handler = InputHandler(calc, make_input_fn(sequence))
    with pytest.raises(ValueError, match="Too many invalid attempts for operand"):
        handler._prompt_operands(1, float)


# ---------------------------------------------------------------------------
# Error message verification
# ---------------------------------------------------------------------------

def test_invalid_operation_error_message_format(calc, capsys):
    """Error on invalid operation must follow expected format."""
    handler = InputHandler(calc, make_input_fn(["unknown", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    # Must mention the unknown operation and available options
    assert "Error:" in out
    assert "Unknown operation" in out
    assert "Available operations:" in out


def test_invalid_operand_error_message_format(calc, capsys):
    """Error on invalid operand must follow expected format."""
    handler = InputHandler(calc, make_input_fn(["add", "notanumber"]))
    handler.run()
    out = capsys.readouterr().out
    assert "Error:" in out
    # Should mention it's an invalid operand or numeric value issue
    assert "Invalid operand" in out or "numeric" in out


# ---------------------------------------------------------------------------
# Reset counter logic
# ---------------------------------------------------------------------------

def test_valid_op_resets_counter_multiple_times(calc, capsys):
    """Counter must reset on each valid operation."""
    sequence = [
        "bad1", "bad2", "bad3",  # 3 invalid
        "add", "1", "1",          # valid op (counter resets)
        "bad4", "bad5",           # 2 more invalid
        "multiply", "2", "3",     # valid op (counter resets)
        "bad6", "bad7", "bad8", "bad9",  # 4 more invalid
        "exit"                    # Should still work because 4 < 5
    ]
    handler = InputHandler(calc, make_input_fn(sequence))
    handler.run()
    out = capsys.readouterr().out
    # Should complete both operations without hitting MAX_RETRIES
    assert "2" in out  # from add(1,1)
    assert "6" in out  # from multiply(2,3)
    assert "Too many invalid attempts" not in out
    assert "Goodbye!" in out


def test_counter_increments_across_operations_without_reset(calc, capsys):
    """Counter should persist across operations until reset by a valid one."""
    sequence = [
        "bad1",           # 1st invalid
        "badop2",         # 2nd invalid (doesn't reset)
        "bad3",           # 3rd invalid
        "bad4",           # 4th invalid
        "bad5",           # 5th invalid - should terminate
    ]
    handler = InputHandler(calc, make_input_fn(sequence))
    handler.run()
    out = capsys.readouterr().out
    assert "Too many invalid attempts. Ending session." in out


# ---------------------------------------------------------------------------
# StopIteration handling with retries
# ---------------------------------------------------------------------------

def test_prompt_operands_stopiteration_before_max_retries(calc):
    """StopIteration during operand prompt raises last_error if one exists."""
    # Only 2 invalid attempts, then exhausted.
    # The implementation re-raises last_error if one is set when StopIteration occurs.
    handler = InputHandler(calc, make_input_fn(["bad1", "bad2"]))
    with pytest.raises(ValueError, match="Invalid operand"):
        handler._prompt_operands(1, float)


def test_run_stopiteration_at_operation_prompt(calc, capsys):
    """StopIteration at operation prompt should print Goodbye."""
    handler = InputHandler(calc, make_input_fn([]))  # Empty input
    handler.run()
    out = capsys.readouterr().out
    assert "Goodbye!" in out


# ---------------------------------------------------------------------------
# Special characters and edge cases
# ---------------------------------------------------------------------------

def test_invalid_op_with_special_characters(calc, capsys):
    """Special characters as operation should be treated as invalid."""
    sequence = ["@@@", "###", "$$$", "^^^", "~~~", "exit"]
    handler = InputHandler(calc, make_input_fn(sequence))
    handler.run()
    out = capsys.readouterr().out
    assert "Too many invalid attempts. Ending session." in out


def test_invalid_operand_with_special_characters(calc):
    """Special characters as operand should be treated as invalid."""
    sequence = ["@@@", "###", "$$$", "^^^", "~~~"]
    handler = InputHandler(calc, make_input_fn(sequence))
    with pytest.raises(ValueError, match="Too many invalid attempts for operand"):
        handler._prompt_operands(1, float)


def test_invalid_operand_with_leading_zeros(calc):
    """Leading zeros in numeric string should parse correctly."""
    sequence = ["007"]
    handler = InputHandler(calc, make_input_fn(sequence))
    result = handler._prompt_operands(1, float)
    assert result == [7.0]


# ---------------------------------------------------------------------------
# Arity edge cases with retries
# ---------------------------------------------------------------------------

def test_prompt_operands_arity_1_valid_after_failures(calc):
    """Arity 1 should succeed after some failures."""
    sequence = ["bad", "bad", "999"]
    handler = InputHandler(calc, make_input_fn(sequence))
    result = handler._prompt_operands(1, float)
    assert result == [999.0]


def test_prompt_operands_arity_2_both_valid_after_failures(calc):
    """Arity 2 should handle failures on either operand."""
    sequence = ["bad1", "bad2", "10", "bad3", "bad4", "20"]
    handler = InputHandler(calc, make_input_fn(sequence))
    result = handler._prompt_operands(2, float)
    assert result == [10.0, 20.0]
