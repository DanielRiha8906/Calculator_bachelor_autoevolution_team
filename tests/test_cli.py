"""Tests for the CLI interface provided by src/cli.py.

Covers valid invocations for every operation, argument-parsing failures,
operand-count mismatches, non-numeric operands, and domain errors (e.g.
division by zero).
"""

from __future__ import annotations

import pytest

from src.cli import run_cli
from src.input_loop import OPERATIONS


# ---------------------------------------------------------------------------
# Valid invocations — one test per operation
# ---------------------------------------------------------------------------

# Each entry: (operation, argv_operands, expected_result_or_substr)
# expected_result_or_substr is a string that should appear in stdout.
_VALID_CASES: list[tuple[str, list[str], str]] = [
    ("add",         ["3", "4"],  "7"),
    ("subtract",    ["9", "3"],  "6"),
    ("multiply",    ["3", "4"],  "12"),
    ("divide",      ["9", "3"],  "3"),
    ("power",       ["2", "3"],  "8"),
    ("factorial",   ["5"],       "120"),
    ("square",      ["4"],       "16"),
    ("cube",        ["3"],       "27"),
    ("square_root", ["9"],       "3"),
    ("cube_root",   ["8"],       "2"),
    ("log",         ["100"],     "2"),
    ("ln",          ["1"],       "0"),
]


@pytest.mark.parametrize("operation,operands,expected_substr", _VALID_CASES)
def test_valid_invocation(
    operation: str,
    operands: list[str],
    expected_substr: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """run_cli should print a result containing the expected numeric value."""
    run_cli(argv=[operation, *operands])
    captured = capsys.readouterr()
    assert expected_substr in captured.out, (
        f"Expected '{expected_substr}' in stdout for '{operation}' with operands {operands}, "
        f"got: {captured.out!r}"
    )


# ---------------------------------------------------------------------------
# Invalid operation name — argparse exits with code 2
# ---------------------------------------------------------------------------

def test_invalid_operation_name() -> None:
    """An unrecognised operation name should cause argparse to exit with code 2."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["nonexistent_operation", "1", "2"])
    assert exc_info.value.code == 2


# ---------------------------------------------------------------------------
# Wrong operand count — exits with code 1
# ---------------------------------------------------------------------------

def test_wrong_operand_count() -> None:
    """A binary operation called with only one operand should exit with code 1."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["add", "3"])
    assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# Non-numeric operand — exits with code 1
# ---------------------------------------------------------------------------

def test_non_numeric_operand() -> None:
    """Passing a non-numeric string as an operand should exit with code 1."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["add", "abc", "4"])
    assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# Domain error: division by zero — exits with code 1
# ---------------------------------------------------------------------------

def test_division_by_zero_via_cli() -> None:
    """Dividing by zero should be caught and exit with code 1."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["divide", "5", "0"])
    assert exc_info.value.code == 1
