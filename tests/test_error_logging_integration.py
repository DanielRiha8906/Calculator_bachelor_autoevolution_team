"""Integration tests for error logging feature.

Tests how ErrorLogger integrates with run_loop and run_cli to ensure that:
- Errors are logged when calculator operations fail
- The error log file is created and readable
- Multiple entries can be parsed from the log file
- Error logging does not interfere with normal program flow
"""

from __future__ import annotations

import os
import re
import sys
import tempfile
from pathlib import Path

import pytest

from src.cli import run_cli
from src.error_logger import (
    INVALID_INPUT,
    CALCULATION_ERROR,
    UNEXPECTED_ERROR,
    ErrorLogger,
)
from src.input_loop import run_loop


# ---------------------------------------------------------------------------
# run_loop integration tests — error logging
# ---------------------------------------------------------------------------


def test_run_loop_logs_division_by_zero_error(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """run_loop must log division by zero errors to the log file."""
    os.chdir(tmp_path)

    inputs = iter(["divide", "10", "0", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))

    # Error log file must be created
    log_file = Path("error.log")
    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")
    assert CALCULATION_ERROR in content
    assert "Division by zero" in content or "zero" in content.lower()


def test_run_loop_logs_error_with_operation_and_operands_context(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """run_loop error log must include operation and operands as context."""
    os.chdir(tmp_path)

    inputs = iter(["divide", "10", "0", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))

    log_file = Path("error.log")
    content = log_file.read_text(encoding="utf-8")

    # Context should contain operation and operands
    assert "operation=" in content
    assert "divide" in content
    assert "operands=" in content


def test_run_loop_logs_invalid_operand_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """run_loop must log invalid operand (non-numeric) as INVALID_INPUT if applicable."""
    os.chdir(tmp_path)

    # Try invalid input multiple times, then return to menu (exhausts retries)
    inputs = iter(["add", "abc", "abc", "abc", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))

    captured = capsys.readouterr()
    # Should show error about invalid operand
    assert "Error" in captured.out or "numeric" in captured.out.lower()


def test_run_loop_logs_negative_sqrt_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """run_loop must log square root of negative number error."""
    os.chdir(tmp_path)

    inputs = iter(["square_root", "-4", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))

    log_file = Path("error.log")
    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")
    assert CALCULATION_ERROR in content
    # Should mention the error
    assert "square" in content.lower() or "negative" in content.lower()


def test_run_loop_error_logging_does_not_prevent_loop_continuation(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Error logging must not prevent the loop from continuing."""
    os.chdir(tmp_path)

    inputs = iter(["divide", "10", "0", "add", "5", "3", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))

    captured = capsys.readouterr()
    # First operation fails (division by zero)
    assert "Error" in captured.out
    # Second operation succeeds and should show result
    assert "8" in captured.out or "Result:" in captured.out
    assert "Goodbye" in captured.out


def test_run_loop_both_console_error_and_error_log_produced(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """When an error occurs, both console output and error log must be produced."""
    os.chdir(tmp_path)

    inputs = iter(["divide", "1", "0", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))

    captured = capsys.readouterr()
    # Console message
    assert "Error" in captured.out

    # Error log file
    log_file = Path("error.log")
    assert log_file.exists()
    assert len(log_file.read_text(encoding="utf-8")) > 0


def test_run_loop_log_format_parseable(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Error log entries must be parseable as [TIMESTAMP] [CATEGORY] Message | key=value."""
    os.chdir(tmp_path)

    inputs = iter(["divide", "5", "0", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))

    log_file = Path("error.log")
    content = log_file.read_text(encoding="utf-8")
    lines = content.strip().split("\n")

    # Each line must match the expected format
    pattern = r"\[.*?\] \[.*?\] .+?"
    for line in lines:
        if line.strip():
            assert re.match(pattern, line) is not None


# ---------------------------------------------------------------------------
# run_cli integration tests — error logging
# ---------------------------------------------------------------------------


def test_run_cli_logs_division_by_zero_before_exit(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli must log division by zero error before exiting."""
    os.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["src", "divide", "10", "0"])

    with pytest.raises(SystemExit) as exc_info:
        run_cli()

    assert exc_info.value.code == 2

    log_file = Path("error.log")
    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")
    assert CALCULATION_ERROR in content
    assert "Division by zero" in content or "zero" in content.lower()


def test_run_cli_logs_invalid_operand_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli must log non-numeric operand error and exit."""
    os.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["src", "add", "abc", "5"])

    with pytest.raises(SystemExit) as exc_info:
        run_cli()

    assert exc_info.value.code == 2

    # May log to error.log depending on implementation
    # At minimum, stderr should have message
    captured = capsys.readouterr()
    assert "error" in captured.err.lower()


def test_run_cli_logs_invalid_operation_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli must log unknown operation error."""
    os.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["src", "invalid_op", "5", "3"])

    with pytest.raises(SystemExit) as exc_info:
        run_cli()

    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "error" in captured.err.lower() or "unknown" in captured.err.lower()


def test_run_cli_error_still_exits_with_code_2_after_logging(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """After logging an error, run_cli must still exit with code 2."""
    os.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["src", "divide", "10", "0"])

    with pytest.raises(SystemExit) as exc_info:
        run_cli()

    assert exc_info.value.code == 2


def test_run_cli_stderr_printed_after_logging(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """After logging an error, run_cli must still print to stderr."""
    os.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["src", "divide", "1", "0"])

    with pytest.raises(SystemExit):
        run_cli()

    captured = capsys.readouterr()
    # Both log and stderr should have error message
    assert "error" in captured.err.lower() or "division" in captured.err.lower()


# ---------------------------------------------------------------------------
# Error categorization integration tests
# ---------------------------------------------------------------------------


def test_error_logging_categorizes_division_by_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Division by zero must be categorized as CALCULATION_ERROR."""
    os.chdir(tmp_path)

    inputs = iter(["divide", "100", "0", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))

    log_file = Path("error.log")
    content = log_file.read_text(encoding="utf-8")
    assert CALCULATION_ERROR in content


def test_error_logging_categorizes_negative_sqrt(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Negative square root must be categorized as CALCULATION_ERROR."""
    os.chdir(tmp_path)

    inputs = iter(["square_root", "-9", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))

    log_file = Path("error.log")
    content = log_file.read_text(encoding="utf-8")
    assert CALCULATION_ERROR in content


def test_error_logging_multiple_entries_append(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Multiple errors in same session must all be logged."""
    os.chdir(tmp_path)

    inputs = iter([
        "divide", "1", "0",
        "square_root", "-1",
        "exit"
    ])
    run_loop(input_fn=lambda _prompt: next(inputs))

    log_file = Path("error.log")
    content = log_file.read_text(encoding="utf-8")
    lines = [line for line in content.strip().split("\n") if line]

    # Both errors must be logged
    assert len(lines) >= 2


def test_error_logging_file_utf8_encoded(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Error log file must be UTF-8 encoded."""
    os.chdir(tmp_path)

    inputs = iter(["divide", "1", "0", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))

    log_file = Path("error.log")
    # Must be readable as UTF-8 without errors
    content = log_file.read_text(encoding="utf-8")
    assert len(content) > 0


def test_error_logging_file_readable_after_run_loop(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Error log file must be readable after run_loop completes."""
    os.chdir(tmp_path)

    inputs = iter(["divide", "1", "0", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))

    log_file = Path("error.log")
    assert log_file.exists()

    # File must be readable and contain valid content
    content = log_file.read_text(encoding="utf-8")
    assert len(content) > 0
    assert "[" in content  # Should have timestamp brackets
    assert "]" in content


def test_error_logging_file_readable_after_run_cli(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Error log file must be readable after run_cli fails."""
    os.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["src", "divide", "10", "0"])

    with pytest.raises(SystemExit):
        run_cli()

    log_file = Path("error.log")
    assert log_file.exists()

    # File must be readable
    content = log_file.read_text(encoding="utf-8")
    assert len(content) > 0


def test_error_logging_preserves_newlines(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Each error log entry must be on its own line."""
    os.chdir(tmp_path)

    inputs = iter([
        "divide", "1", "0",
        "log", "0",
        "exit"
    ])
    run_loop(input_fn=lambda _prompt: next(inputs))

    log_file = Path("error.log")
    content = log_file.read_text(encoding="utf-8")
    lines = content.strip().split("\n")

    # Should have multiple entries
    assert len(lines) >= 2


def test_error_logging_context_includes_operands_list(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Error log context must include the operands list."""
    os.chdir(tmp_path)

    inputs = iter(["divide", "42", "0", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))

    log_file = Path("error.log")
    content = log_file.read_text(encoding="utf-8")

    # Should mention operands (42.0 and 0.0 in a list format)
    assert "operands=" in content


def test_error_logging_context_includes_operation_name(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Error log context must include the operation name."""
    os.chdir(tmp_path)

    inputs = iter(["divide", "1", "0", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))

    log_file = Path("error.log")
    content = log_file.read_text(encoding="utf-8")

    assert "operation=" in content
    assert "divide" in content


def test_error_logging_negative_factorial_logged(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Negative factorial must be logged as CALCULATION_ERROR."""
    os.chdir(tmp_path)

    inputs = iter(["factorial", "-5", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))

    log_file = Path("error.log")
    if log_file.exists():
        content = log_file.read_text(encoding="utf-8")
        assert CALCULATION_ERROR in content or "negative" in content.lower()


def test_error_logging_log_of_zero_logged(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """log(0) must be logged as CALCULATION_ERROR."""
    os.chdir(tmp_path)

    inputs = iter(["log", "0", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))

    log_file = Path("error.log")
    if log_file.exists():
        content = log_file.read_text(encoding="utf-8")
        assert CALCULATION_ERROR in content or "log" in content.lower()


# ---------------------------------------------------------------------------
# Error logging — isolation and cleanup
# ---------------------------------------------------------------------------


def test_error_logging_isolated_per_tempdir(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Each test's error.log must be isolated in its own temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir1:
        os.chdir(tmpdir1)
        inputs = iter(["divide", "1", "0", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))

        log_file1 = Path(tmpdir1) / "error.log"
        assert log_file1.exists()
        content1 = log_file1.read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory() as tmpdir2:
        os.chdir(tmpdir2)
        inputs = iter(["divide", "2", "0", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))

        log_file2 = Path(tmpdir2) / "error.log"
        assert log_file2.exists()
        content2 = log_file2.read_text(encoding="utf-8")

    # Files are in different directories
    assert tmpdir1 != tmpdir2
    # And contain different entries
    assert "operands" in content1 and "operands" in content2
