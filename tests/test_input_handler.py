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
