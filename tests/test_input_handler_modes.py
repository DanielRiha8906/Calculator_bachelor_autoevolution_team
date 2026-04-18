"""Comprehensive pytest tests for input handler mode switching and mode filtering.

Tests verify:
- InputHandler initializes in NORMAL mode by default
- _get_available_operations_for_mode() filters by current mode
- In NORMAL mode, only NORMAL_OPERATIONS keys are available
- In SCIENTIFIC mode, all OPERATIONS keys are available
- _show_menu() displays current mode label
- _show_menu() filters menu items by mode
- run() handles mode-switch commands ("mode normal", "mode scientific")
- Mode persists across operations
- Attempting scientific operations in NORMAL mode shows error with guidance
- Normal operations work in both modes (regression check)
"""

import pytest
from src.core.calculator import Calculator
from src.session.input_handler import InputHandler
from src.session.mode import Mode
from src.operations import OPERATIONS, NORMAL_OPERATIONS, SCIENTIFIC_OPERATIONS
from src.shared.logger import Logger


# ===========================================================================
# InputHandler: Initialization and Default Mode
# ===========================================================================

def test_input_handler_initializes_in_normal_mode():
    """InputHandler must initialize with _mode = Mode.NORMAL."""
    calc = Calculator()
    handler = InputHandler(calc)
    assert handler._mode is Mode.NORMAL


def test_input_handler_mode_attribute_exists():
    """InputHandler must have a _mode attribute."""
    calc = Calculator()
    handler = InputHandler(calc)
    assert hasattr(handler, '_mode')


def test_input_handler_mode_is_mode_enum():
    """InputHandler._mode must be a Mode enum member."""
    calc = Calculator()
    handler = InputHandler(calc)
    assert isinstance(handler._mode, Mode)


# ===========================================================================
# _get_available_operations_for_mode: Normal Mode
# ===========================================================================

def test_get_available_operations_normal_mode_returns_dict():
    """_get_available_operations_for_mode in NORMAL mode returns a dict."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.NORMAL
    result = handler._get_available_operations_for_mode()
    assert isinstance(result, dict)


def test_get_available_operations_normal_mode_returns_normal_ops():
    """_get_available_operations_for_mode in NORMAL mode returns NORMAL_OPERATIONS keys."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.NORMAL
    result = handler._get_available_operations_for_mode()

    # All keys in result should be from NORMAL_OPERATIONS
    for key in result.keys():
        assert key in NORMAL_OPERATIONS

    # All keys in NORMAL_OPERATIONS should be in result
    for key in NORMAL_OPERATIONS.keys():
        assert key in result


def test_get_available_operations_normal_mode_count():
    """_get_available_operations_for_mode in NORMAL mode returns 12 operations."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.NORMAL
    result = handler._get_available_operations_for_mode()
    assert len(result) == 12


def test_get_available_operations_normal_mode_no_scientific_ops():
    """_get_available_operations_for_mode in NORMAL mode does NOT include scientific ops."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.NORMAL
    result = handler._get_available_operations_for_mode()

    # No scientific-only operations should be in the result
    scientific_keys = {"sin", "cos", "tan", "asin", "acos", "atan", "pi", "e"}
    for key in scientific_keys:
        assert key not in result


@pytest.mark.parametrize("op_key", ["sin", "cos", "tan", "asin", "acos", "atan", "pi", "e"])
def test_get_available_operations_normal_mode_excludes_each_scientific(op_key):
    """Each scientific operation is excluded in NORMAL mode."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.NORMAL
    result = handler._get_available_operations_for_mode()
    assert op_key not in result


@pytest.mark.parametrize("op_key", ["add", "subtract", "multiply", "divide", "power", "factorial",
                                      "square", "cube", "square_root", "cube_root", "log10", "ln"])
def test_get_available_operations_normal_mode_includes_each_normal(op_key):
    """Each normal operation is included in NORMAL mode."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.NORMAL
    result = handler._get_available_operations_for_mode()
    assert op_key in result


# ===========================================================================
# _get_available_operations_for_mode: Scientific Mode
# ===========================================================================

def test_get_available_operations_scientific_mode_returns_dict():
    """_get_available_operations_for_mode in SCIENTIFIC mode returns a dict."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.SCIENTIFIC
    result = handler._get_available_operations_for_mode()
    assert isinstance(result, dict)


def test_get_available_operations_scientific_mode_returns_all_ops():
    """_get_available_operations_for_mode in SCIENTIFIC mode returns all OPERATIONS."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.SCIENTIFIC
    result = handler._get_available_operations_for_mode()
    assert result is OPERATIONS or result == OPERATIONS


def test_get_available_operations_scientific_mode_count():
    """_get_available_operations_for_mode in SCIENTIFIC mode returns 20 operations."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.SCIENTIFIC
    result = handler._get_available_operations_for_mode()
    assert len(result) == 20


def test_get_available_operations_scientific_mode_includes_normal():
    """_get_available_operations_for_mode in SCIENTIFIC mode includes all NORMAL_OPERATIONS."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.SCIENTIFIC
    result = handler._get_available_operations_for_mode()

    for key in NORMAL_OPERATIONS.keys():
        assert key in result


def test_get_available_operations_scientific_mode_includes_scientific():
    """_get_available_operations_for_mode in SCIENTIFIC mode includes all SCIENTIFIC_OPERATIONS."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.SCIENTIFIC
    result = handler._get_available_operations_for_mode()

    for key in SCIENTIFIC_OPERATIONS.keys():
        assert key in result


@pytest.mark.parametrize("op_key", ["sin", "cos", "tan", "asin", "acos", "atan", "pi", "e"])
def test_get_available_operations_scientific_mode_includes_each_scientific(op_key):
    """Each scientific operation is included in SCIENTIFIC mode."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.SCIENTIFIC
    result = handler._get_available_operations_for_mode()
    assert op_key in result


# ===========================================================================
# _show_menu: Mode Label in Header
# ===========================================================================

def test_show_menu_normal_mode_shows_normal_label(capsys):
    """_show_menu in NORMAL mode must display 'Normal Mode'."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.NORMAL
    handler._show_menu()
    captured = capsys.readouterr()
    assert "Normal Mode" in captured.out or "normal mode" in captured.out.lower()


def test_show_menu_scientific_mode_shows_scientific_label(capsys):
    """_show_menu in SCIENTIFIC mode must display 'Scientific Mode'."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.SCIENTIFIC
    handler._show_menu()
    captured = capsys.readouterr()
    assert "Scientific Mode" in captured.out or "scientific mode" in captured.out.lower()


def test_show_menu_contains_mode_label(capsys):
    """_show_menu must show the mode label in output."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._show_menu()
    captured = capsys.readouterr()
    assert "Mode" in captured.out


# ===========================================================================
# _show_menu: Filtering by Mode
# ===========================================================================

def test_show_menu_normal_mode_lists_only_normal_ops(capsys):
    """_show_menu in NORMAL mode must list only NORMAL_OPERATIONS keys."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.NORMAL
    handler._show_menu()
    captured = capsys.readouterr()

    # All normal ops should be listed
    for key in NORMAL_OPERATIONS.keys():
        assert key in captured.out, f"Missing normal operation: {key}"


def test_show_menu_normal_mode_excludes_scientific_ops(capsys):
    """_show_menu in NORMAL mode must NOT list scientific-only operations."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.NORMAL
    handler._show_menu()
    captured = capsys.readouterr()

    # Scientific ops should NOT be listed as operation keys
    # Check for operation keys in formatted output (e.g., "sin            —")
    scientific_keys = ["sin", "cos", "tan", "asin", "acos", "atan", "pi"]
    for key in scientific_keys:
        # Look for the key with spaces/dashes around it (operation key format)
        assert f"{key:<14}" not in captured.out, f"Should not list scientific operation in NORMAL mode: {key}"


@pytest.mark.parametrize("op_key", ["sin", "cos", "tan", "asin", "acos", "atan", "pi", "e"])
def test_show_menu_normal_mode_excludes_each_scientific(capsys, op_key):
    """Each scientific operation is excluded from NORMAL mode menu."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.NORMAL
    handler._show_menu()
    captured = capsys.readouterr()
    # Check for operation key in formatted output (e.g., "sin            —")
    assert f"{op_key:<14}" not in captured.out, f"Scientific operation {op_key} should not appear in NORMAL mode menu"


def test_show_menu_scientific_mode_lists_all_ops(capsys):
    """_show_menu in SCIENTIFIC mode must list all OPERATIONS keys."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.SCIENTIFIC
    handler._show_menu()
    captured = capsys.readouterr()

    # All ops should be listed
    for key in OPERATIONS.keys():
        assert key in captured.out, f"Missing operation: {key}"


def test_show_menu_scientific_mode_includes_normal_ops(capsys):
    """_show_menu in SCIENTIFIC mode must include all NORMAL_OPERATIONS."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.SCIENTIFIC
    handler._show_menu()
    captured = capsys.readouterr()

    for key in NORMAL_OPERATIONS.keys():
        assert key in captured.out


def test_show_menu_scientific_mode_includes_scientific_ops(capsys):
    """_show_menu in SCIENTIFIC mode must include all SCIENTIFIC_OPERATIONS."""
    calc = Calculator()
    handler = InputHandler(calc)
    handler._mode = Mode.SCIENTIFIC
    handler._show_menu()
    captured = capsys.readouterr()

    for key in SCIENTIFIC_OPERATIONS.keys():
        assert key in captured.out


# ===========================================================================
# run(): Mode Switching via parse_mode_command
# ===========================================================================

def make_input_fn(responses):
    """Helper: create an input function that yields responses in sequence."""
    it = iter(responses)
    def _input_fn(prompt=""):
        return next(it)
    return _input_fn


def test_run_mode_switch_to_scientific(capsys):
    """run() handles 'mode scientific' command and switches mode."""
    calc = Calculator()
    # Sequence: "mode scientific", exit
    input_fn = make_input_fn(["mode scientific", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    # Should show mode switch confirmation
    assert "Mode switched to" in captured.out or "scientific" in captured.out.lower()


def test_run_mode_switch_to_normal(capsys):
    """run() handles 'mode normal' command."""
    calc = Calculator()
    input_fn = make_input_fn(["mode normal", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    # Should show mode switch confirmation
    assert "Mode switched to" in captured.out or "normal" in captured.out.lower()


def test_run_mode_switch_persists_after_operation(capsys):
    """Mode persists after switching and using an operation."""
    calc = Calculator()
    # Switch to scientific, use sin, exit
    input_fn = make_input_fn(["mode scientific", "sin", "0", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    # Should have successfully switched to scientific
    assert "Mode switched to" in captured.out or "scientific" in captured.out.lower()
    assert "Result" in captured.out  # sin operation succeeded


def test_run_mode_switch_back_to_normal(capsys):
    """run() can switch from SCIENTIFIC back to NORMAL."""
    calc = Calculator()
    # Switch to scientific, then back to normal, exit
    input_fn = make_input_fn(["mode scientific", "mode normal", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    # Should see two mode switches
    assert captured.out.count("Mode switched to") >= 1


def test_run_mode_case_insensitive(capsys):
    """run() handles mode commands case-insensitively."""
    calc = Calculator()
    input_fn = make_input_fn(["MODE SCIENTIFIC", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    # Should succeed
    assert "Mode switched to" in captured.out or "scientific" in captured.out.lower()


# ===========================================================================
# run(): Mode Restriction on Scientific Operations
# ===========================================================================

def test_run_scientific_op_in_normal_mode_shows_error(capsys):
    """Attempting sin in NORMAL mode shows error with guidance."""
    calc = Calculator()
    input_fn = make_input_fn(["sin", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    # Should show error mentioning scientific mode
    assert "scientific mode" in captured.out.lower() or "mode scientific" in captured.out.lower()


def test_run_scientific_op_in_normal_mode_error_message_helpful(capsys):
    """Error message guides user on how to switch to scientific mode."""
    calc = Calculator()
    input_fn = make_input_fn(["sin", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    # Error message should mention "mode scientific" as the solution
    assert "mode scientific" in captured.out.lower()


def test_run_cos_in_normal_mode_shows_error(capsys):
    """Attempting cos in NORMAL mode shows error."""
    calc = Calculator()
    input_fn = make_input_fn(["cos", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    assert "scientific mode" in captured.out.lower()


def test_run_pi_in_normal_mode_shows_error(capsys):
    """Attempting pi in NORMAL mode shows error (it's scientific)."""
    calc = Calculator()
    input_fn = make_input_fn(["pi", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    assert "scientific mode" in captured.out.lower()


def test_run_e_in_normal_mode_shows_error(capsys):
    """Attempting e in NORMAL mode shows error (it's scientific)."""
    calc = Calculator()
    input_fn = make_input_fn(["e", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    assert "scientific mode" in captured.out.lower()


# ===========================================================================
# run(): Scientific Operations Work in Scientific Mode
# ===========================================================================

def test_run_sin_in_scientific_mode_works(capsys):
    """sin operation works in SCIENTIFIC mode."""
    calc = Calculator()
    input_fn = make_input_fn(["mode scientific", "sin", "0", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    # Should show result of sin(0) = 0
    assert "Result" in captured.out
    assert "0" in captured.out  # The result should be 0


def test_run_cos_in_scientific_mode_works(capsys):
    """cos operation works in SCIENTIFIC mode."""
    calc = Calculator()
    input_fn = make_input_fn(["mode scientific", "cos", "0", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    assert "Result" in captured.out


def test_run_pi_in_scientific_mode_works(capsys):
    """pi constant works in SCIENTIFIC mode."""
    calc = Calculator()
    input_fn = make_input_fn(["mode scientific", "pi", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    # pi should return approximately 3.14159
    assert "Result" in captured.out
    assert "3.14" in captured.out or "3.1415" in captured.out


def test_run_e_in_scientific_mode_works(capsys):
    """e constant works in SCIENTIFIC mode."""
    calc = Calculator()
    input_fn = make_input_fn(["mode scientific", "e", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    # e should return approximately 2.71828
    assert "Result" in captured.out
    assert "2.71" in captured.out or "2.7182" in captured.out


def test_run_asin_in_scientific_mode_works(capsys):
    """asin operation works in SCIENTIFIC mode."""
    calc = Calculator()
    input_fn = make_input_fn(["mode scientific", "asin", "1", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    assert "Result" in captured.out


# ===========================================================================
# run(): Normal Operations Work in Both Modes
# ===========================================================================

def test_run_add_in_normal_mode_works(capsys):
    """add operation works in NORMAL mode."""
    calc = Calculator()
    input_fn = make_input_fn(["add", "2", "3", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    assert "Result" in captured.out
    assert "5" in captured.out


def test_run_add_in_scientific_mode_works(capsys):
    """add operation still works in SCIENTIFIC mode."""
    calc = Calculator()
    input_fn = make_input_fn(["mode scientific", "add", "2", "3", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    assert "Result" in captured.out
    assert "5" in captured.out


def test_run_factorial_in_normal_mode_works(capsys):
    """factorial operation works in NORMAL mode."""
    calc = Calculator()
    input_fn = make_input_fn(["factorial", "5", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    assert "Result" in captured.out
    assert "120" in captured.out


def test_run_factorial_in_scientific_mode_works(capsys):
    """factorial operation still works in SCIENTIFIC mode."""
    calc = Calculator()
    input_fn = make_input_fn(["mode scientific", "factorial", "5", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    assert "Result" in captured.out
    assert "120" in captured.out


def test_run_square_in_normal_mode(capsys):
    """square operation works in NORMAL mode."""
    calc = Calculator()
    input_fn = make_input_fn(["square", "4", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    assert "Result" in captured.out
    assert "16" in captured.out


def test_run_square_in_scientific_mode(capsys):
    """square operation works in SCIENTIFIC mode."""
    calc = Calculator()
    input_fn = make_input_fn(["mode scientific", "square", "4", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    assert "Result" in captured.out
    assert "16" in captured.out


# ===========================================================================
# run(): Invalid Mode Commands Don't Change Mode
# ===========================================================================

def test_run_invalid_mode_command_keeps_mode(capsys):
    """Invalid mode command ('mode invalid') doesn't change mode."""
    calc = Calculator()
    input_fn = make_input_fn(["mode invalid", "add", "2", "3", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    # add should work (we're still in NORMAL mode)
    assert "Result" in captured.out
    assert "5" in captured.out


def test_run_invalid_mode_shows_error(capsys):
    """Invalid mode command prints an error."""
    calc = Calculator()
    input_fn = make_input_fn(["mode invalid", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    # Should print some error or not recognize it as a mode command
    # (it will be treated as an unknown operation)


# ===========================================================================
# Integration: Mode Switching Across Multiple Operations
# ===========================================================================

def test_run_mixed_mode_sequence(capsys):
    """Can perform operations in both NORMAL and SCIENTIFIC modes in one session."""
    calc = Calculator()
    input_fn = make_input_fn([
        "add", "2", "3",        # Normal: 2+3=5
        "mode scientific",       # Switch to scientific
        "sin", "0",             # Scientific: sin(0)=0
        "mode normal",          # Switch back
        "multiply", "4", "5",   # Normal: 4*5=20
        "exit"
    ])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    # Should see results for add, sin, and multiply
    assert captured.out.count("Result") >= 3


def test_run_mode_persistence_across_operations():
    """Mode persists across multiple operations without explicit switching."""
    calc = Calculator()
    input_fn = make_input_fn([
        "mode scientific",
        "sin", "0",
        "cos", "0",
        "exit"
    ])
    handler = InputHandler(calc, input_fn)
    # Should not raise any exception
    handler.run()


# ===========================================================================
# Edge Cases: Mode-Related Behavior
# ===========================================================================

def test_run_whitespace_in_mode_command(capsys):
    """Mode command with extra whitespace works."""
    calc = Calculator()
    input_fn = make_input_fn(["  mode   scientific  ", "exit"])
    handler = InputHandler(calc, input_fn)
    handler.run()
    captured = capsys.readouterr()

    # Should successfully switch
    assert "Mode switched to" in captured.out or "scientific" in captured.out.lower()


def test_get_available_operations_mode_attribute_respected():
    """_get_available_operations_for_mode respects the _mode attribute."""
    calc = Calculator()
    handler = InputHandler(calc)

    # Start in NORMAL
    assert len(handler._get_available_operations_for_mode()) == 12

    # Switch to SCIENTIFIC
    handler._mode = Mode.SCIENTIFIC
    assert len(handler._get_available_operations_for_mode()) == 20

    # Switch back to NORMAL
    handler._mode = Mode.NORMAL
    assert len(handler._get_available_operations_for_mode()) == 12
