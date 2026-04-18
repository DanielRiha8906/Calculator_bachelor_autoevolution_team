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
# History feature — recording operations
# ---------------------------------------------------------------------------

def test_history_tracks_single_operation(calc, capsys, tmp_path):
    """A single operation should be recorded in the history."""
    import os
    # Save current directory and change to tmp_path to avoid cluttering repo
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        handler = InputHandler(calc, make_input_fn(["add", "2", "3", "exit"]))
        handler.run()

        # Verify history file was created with the operation
        history_file = tmp_path / "history.txt"
        assert history_file.exists()
        content = history_file.read_text(encoding="utf-8")
        # Operands are coerced to float, so they appear as 2.0 and 3.0
        assert "add(2.0, 3.0) = 5.0" in content
    finally:
        os.chdir(old_cwd)


def test_history_tracks_multiple_operations(calc, capsys, tmp_path):
    """Multiple operations should be recorded in history in order."""
    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        handler = InputHandler(
            calc,
            make_input_fn(["add", "1", "2", "multiply", "3", "4", "exit"]),
        )
        handler.run()

        history_file = tmp_path / "history.txt"
        assert history_file.exists()
        content = history_file.read_text(encoding="utf-8")
        lines = content.strip().split("\n")

        assert len(lines) == 2
        assert "add(1.0, 2.0) = 3.0" in lines[0]
        assert "multiply(3.0, 4.0) = 12.0" in lines[1]
    finally:
        os.chdir(old_cwd)


def test_history_display_command_empty(calc, capsys, tmp_path):
    """The 'history' command should show 'No history yet.' when no operations recorded."""
    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        handler = InputHandler(calc, make_input_fn(["history", "exit"]))
        handler.run()

        captured = capsys.readouterr()
        assert "No history yet." in captured.out
    finally:
        os.chdir(old_cwd)


def test_history_display_command_with_entries(calc, capsys, tmp_path):
    """The 'history' command should display recorded entries."""
    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        handler = InputHandler(
            calc,
            make_input_fn(["add", "2", "3", "history", "exit"]),
        )
        handler.run()

        captured = capsys.readouterr()
        assert "add(2.0, 3.0) = 5.0" in captured.out
    finally:
        os.chdir(old_cwd)


def test_history_display_multiple_entries(calc, capsys, tmp_path):
    """The 'history' command should display all recorded entries."""
    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        handler = InputHandler(
            calc,
            make_input_fn(
                ["add", "1", "2", "multiply", "5", "6", "history", "exit"]
            ),
        )
        handler.run()

        captured = capsys.readouterr()
        assert "add(1.0, 2.0) = 3.0" in captured.out
        assert "multiply(5.0, 6.0) = 30.0" in captured.out
    finally:
        os.chdir(old_cwd)


def test_history_display_continues_session(calc, capsys, tmp_path):
    """After 'history' command, the session should continue normally."""
    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        handler = InputHandler(
            calc,
            make_input_fn(["add", "1", "1", "history", "add", "2", "2", "exit"]),
        )
        handler.run()

        # Check that both results are printed
        captured = capsys.readouterr()
        assert "Result: 2.0" in captured.out  # First add result
        assert "Result: 4.0" in captured.out  # Second add result

        # Check that history file contains both operations
        history_file = tmp_path / "history.txt"
        content = history_file.read_text(encoding="utf-8")
        assert "add(1.0, 1.0) = 2.0" in content
        assert "add(2.0, 2.0) = 4.0" in content
    finally:
        os.chdir(old_cwd)


def test_history_saved_to_file_on_exit(calc, capsys, tmp_path):
    """history.txt should be created with correct content when session exits normally."""
    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        handler = InputHandler(
            calc,
            make_input_fn(["add", "5", "5", "subtract", "10", "3", "exit"]),
        )
        handler.run()

        history_file = tmp_path / "history.txt"
        assert history_file.exists()
        content = history_file.read_text(encoding="utf-8")

        assert "add(5.0, 5.0) = 10.0" in content
        assert "subtract(10.0, 3.0) = 7.0" in content
    finally:
        os.chdir(old_cwd)


def test_history_saved_to_file_on_quit(calc, capsys, tmp_path):
    """history.txt should be created when session ends with 'quit'."""
    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        handler = InputHandler(
            calc,
            make_input_fn(["multiply", "3", "7", "quit"]),
        )
        handler.run()

        history_file = tmp_path / "history.txt"
        assert history_file.exists()
        content = history_file.read_text(encoding="utf-8")
        assert "multiply(3.0, 7.0) = 21.0" in content
    finally:
        os.chdir(old_cwd)


def test_history_saved_to_file_empty_session(calc, capsys, tmp_path):
    """history.txt should be created (empty) even if no operations performed."""
    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        handler = InputHandler(calc, make_input_fn(["exit"]))
        handler.run()

        history_file = tmp_path / "history.txt"
        assert history_file.exists()
        content = history_file.read_text(encoding="utf-8")
        assert content == ""
    finally:
        os.chdir(old_cwd)


def test_history_unary_operation_recorded(calc, capsys, tmp_path):
    """Unary operations should be recorded correctly in history."""
    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        handler = InputHandler(
            calc,
            make_input_fn(["square", "8", "exit"]),
        )
        handler.run()

        history_file = tmp_path / "history.txt"
        content = history_file.read_text(encoding="utf-8")
        assert "square(8) = 64" in content or "square(8.0) = 64" in content
    finally:
        os.chdir(old_cwd)


def test_history_recorded_before_error_in_next_op(calc, capsys, tmp_path):
    """Valid operations should be recorded even if a subsequent operation fails."""
    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        handler = InputHandler(
            calc,
            make_input_fn(["add", "1", "1", "divide", "5", "0", "exit"]),
        )
        handler.run()

        history_file = tmp_path / "history.txt"
        content = history_file.read_text(encoding="utf-8")
        # Only the successful operation should be recorded (operands coerced to float)
        assert "add(1.0, 1.0) = 2.0" in content
        # Division by zero should not be recorded
        assert "divide" not in content
    finally:
        os.chdir(old_cwd)


def test_history_recorded_after_invalid_operand_retry(calc, capsys, tmp_path):
    """Operations should be recorded only after valid operands are provided."""
    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        handler = InputHandler(
            calc,
            make_input_fn(["add", "not_a_number", "5", "5", "exit"]),
        )
        handler.run()

        history_file = tmp_path / "history.txt"
        content = history_file.read_text(encoding="utf-8")
        # The successful retry should be recorded (operands coerced to float)
        assert "add(5.0, 5.0) = 10.0" in content
    finally:
        os.chdir(old_cwd)


def test_history_persisted_across_multiple_sessions_file(calc, capsys, tmp_path):
    """Each session should overwrite history.txt (not append)."""
    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        # First session
        handler1 = InputHandler(calc, make_input_fn(["add", "1", "1", "exit"]))
        handler1.run()

        history_file = tmp_path / "history.txt"
        content1 = history_file.read_text(encoding="utf-8")
        assert "add(1.0, 1.0) = 2.0" in content1

        # Second session
        handler2 = InputHandler(calc, make_input_fn(["multiply", "2", "2", "exit"]))
        handler2.run()

        content2 = history_file.read_text(encoding="utf-8")
        # Second session should have overwritten the file (operands coerced to float)
        assert "multiply(2.0, 2.0) = 4.0" in content2
        assert "add(1.0, 1.0) = 2.0" not in content2
    finally:
        os.chdir(old_cwd)


def test_history_file_utf8_encoding(calc, capsys, tmp_path):
    """history.txt should be written with UTF-8 encoding."""
    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        handler = InputHandler(
            calc,
            make_input_fn(["add", "1.5", "2.5", "exit"]),
        )
        handler.run()

        history_file = tmp_path / "history.txt"
        # Should be readable as UTF-8
        content = history_file.read_text(encoding="utf-8")
        assert "add(1.5, 2.5) = 4.0" in content
    finally:
        os.chdir(old_cwd)


def test_history_does_not_crash_on_invalid_operation(calc, capsys, tmp_path):
    """Invalid operations should not be recorded; session should continue."""
    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        handler = InputHandler(
            calc,
            make_input_fn(["invalid_op", "add", "3", "3", "exit"]),
        )
        handler.run()

        history_file = tmp_path / "history.txt"
        content = history_file.read_text(encoding="utf-8")
        assert "add(3.0, 3.0) = 6.0" in content
        assert "invalid_op" not in content
    finally:
        os.chdir(old_cwd)
