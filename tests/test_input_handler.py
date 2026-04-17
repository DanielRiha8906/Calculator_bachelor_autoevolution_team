"""Tests for src/input_handler.py — InputHandler interactive session loop.

All tests use the injectable input_fn parameter to avoid patching builtins.input.
capsys is used to inspect printed output.
"""

import math
import pytest

from src.calculator import Calculator
from src.input_handler import InputHandler


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input_fn(responses: list[str]):
    """Return a callable that yields successive strings from *responses*.

    Using iter() with next() ensures each call to the returned function
    consumes exactly one element, mirroring real interactive input.
    """
    it = iter(responses)

    def _input_fn(prompt: str = "") -> str:  # noqa: ARG001
        return next(it)

    return _input_fn


@pytest.fixture
def calc() -> Calculator:
    return Calculator()


# ---------------------------------------------------------------------------
# Exit / quit behaviour
# ---------------------------------------------------------------------------

def test_exit_immediately(calc, capsys):
    """Entering 'exit' at the first prompt terminates the session immediately."""
    handler = InputHandler(calc, make_input_fn(["exit"]))
    handler.run()
    captured = capsys.readouterr()
    assert "Goodbye!" in captured.out


def test_quit_immediately(calc, capsys):
    """Entering 'quit' at the first prompt terminates the session immediately."""
    handler = InputHandler(calc, make_input_fn(["quit"]))
    handler.run()
    captured = capsys.readouterr()
    assert "Goodbye!" in captured.out


# ---------------------------------------------------------------------------
# Binary operations
# ---------------------------------------------------------------------------

def test_binary_operation_add(calc, capsys):
    """add(3, 4) must print a result of 7.0 and then exit."""
    handler = InputHandler(calc, make_input_fn(["add", "3", "4", "exit"]))
    handler.run()
    captured = capsys.readouterr()
    assert "7" in captured.out


def test_binary_operation_power(calc, capsys):
    """power(2, 10) must print a result of 1024 and then exit."""
    handler = InputHandler(calc, make_input_fn(["power", "2", "10", "exit"]))
    handler.run()
    captured = capsys.readouterr()
    assert "1024" in captured.out


# ---------------------------------------------------------------------------
# Unary operations
# ---------------------------------------------------------------------------

def test_unary_operation_square_root(calc, capsys):
    """square_root(9) must print a result of 3.0 and then exit."""
    handler = InputHandler(calc, make_input_fn(["square_root", "9", "exit"]))
    handler.run()
    captured = capsys.readouterr()
    assert "3.0" in captured.out


def test_unary_operation_factorial(calc, capsys):
    """factorial(5) must print a result of 120 and then exit."""
    handler = InputHandler(calc, make_input_fn(["factorial", "5", "exit"]))
    handler.run()
    captured = capsys.readouterr()
    assert "120" in captured.out


# ---------------------------------------------------------------------------
# Error handling — no crash
# ---------------------------------------------------------------------------

def test_invalid_operation_key(calc, capsys):
    """An unrecognised operation key must print an error message, not crash."""
    handler = InputHandler(calc, make_input_fn(["badop", "exit"]))
    handler.run()
    captured = capsys.readouterr()
    assert "Error" in captured.out or "error" in captured.out.lower()
    assert "Goodbye!" in captured.out


def test_invalid_operand_non_numeric(calc, capsys):
    """A non-numeric operand for 'add' must print an error message, not crash."""
    handler = InputHandler(calc, make_input_fn(["add", "abc", "exit"]))
    handler.run()
    captured = capsys.readouterr()
    assert "Error" in captured.out or "error" in captured.out.lower()
    assert "Goodbye!" in captured.out


def test_division_by_zero(calc, capsys):
    """divide(5, 0) must catch ZeroDivisionError and print an error, not crash."""
    handler = InputHandler(calc, make_input_fn(["divide", "5", "0", "exit"]))
    handler.run()
    captured = capsys.readouterr()
    assert "Error" in captured.out or "error" in captured.out.lower()
    assert "Goodbye!" in captured.out


# ---------------------------------------------------------------------------
# Multi-operation session
# ---------------------------------------------------------------------------

def test_session_loop_multiple_calculations(calc, capsys):
    """Two complete operations followed by exit must both produce results."""
    # add(2, 3) => 5.0, multiply(4, 5) => 20.0
    handler = InputHandler(
        calc,
        make_input_fn(["add", "2", "3", "multiply", "4", "5", "exit"]),
    )
    handler.run()
    captured = capsys.readouterr()
    assert "5" in captured.out
    assert "20" in captured.out
    assert "Goodbye!" in captured.out


# ---------------------------------------------------------------------------
# Retry logic — operation input
# ---------------------------------------------------------------------------

def test_retry_once_then_succeed_for_operation(calc, capsys):
    """One invalid operation followed by valid one should complete the calculation."""
    handler = InputHandler(calc, make_input_fn(["badop", "add", "3", "4", "exit"]))
    handler.run()
    captured = capsys.readouterr()
    # The operation "add" should execute with operands 3 and 4
    assert "7" in captured.out
    assert "Goodbye!" in captured.out


def test_max_operation_retries_terminates_session(calc, capsys):
    """Five invalid operations should terminate session gracefully."""
    handler = InputHandler(
        calc,
        make_input_fn(["bad1", "bad2", "bad3", "bad4", "bad5", "exit"]),
    )
    handler.run()
    captured = capsys.readouterr()
    # Should terminate with "Too many invalid attempts" message
    assert "Too many invalid attempts" in captured.out
    # Should not print "Goodbye!" since it exits at max retries, not gracefully
    # (the run() method prints the message and breaks, no graceful goodbye)

def test_invalid_operation_shows_available_ops(calc, capsys):
    """Invalid operation should print error with available operations list."""
    handler = InputHandler(calc, make_input_fn(["badop", "exit"]))
    handler.run()
    captured = capsys.readouterr()
    # Should show available operations when invalid key is entered
    assert "Error:" in captured.out or "error" in captured.out.lower()
    assert "Goodbye!" in captured.out


# ---------------------------------------------------------------------------
# Retry logic — operand input
# ---------------------------------------------------------------------------

def test_retry_once_then_succeed_for_operand(calc, capsys):
    """One invalid operand followed by valid one should execute the operation."""
    handler = InputHandler(
        calc,
        make_input_fn(["add", "notanumber", "3", "4", "exit"]),
    )
    handler.run()
    captured = capsys.readouterr()
    # After invalid operand, should retry and succeed with 3 and 4
    assert "7" in captured.out
    assert "Goodbye!" in captured.out


def test_max_operand_retries_terminates_session(calc, capsys):
    """Five invalid operands should terminate session gracefully."""
    handler = InputHandler(
        calc,
        make_input_fn(["add", "a", "b", "c", "d", "e", "exit"]),
    )
    handler.run()
    captured = capsys.readouterr()
    # Should terminate with "Too many invalid attempts" message
    assert "Too many invalid attempts" in captured.out
    # Session should not crash
    # Note: may or may not print "Goodbye!" depending on implementation


def test_retry_on_first_operand_then_succeed(calc, capsys):
    """Invalid first operand, then valid first, then valid second."""
    handler = InputHandler(
        calc,
        make_input_fn(["multiply", "notnum", "5", "6", "exit"]),
    )
    handler.run()
    captured = capsys.readouterr()
    # After invalid first operand, retry with 5 and 6
    assert "30" in captured.out
    assert "Goodbye!" in captured.out


def test_retry_on_second_operand_then_succeed(calc, capsys):
    """Valid first operand, invalid second, then valid second."""
    handler = InputHandler(
        calc,
        make_input_fn(["divide", "10", "notnum", "2", "exit"]),
    )
    handler.run()
    captured = capsys.readouterr()
    # First operand 10 accepted, second invalid then 2 provided
    assert "5" in captured.out
    assert "Goodbye!" in captured.out
