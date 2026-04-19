"""Tests for the interactive input handler module."""

import pytest
import io
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.calculator import Calculator
from src.input_handler import (
    get_operation_registry,
    display_menu,
    get_operation_choice,
    get_operands,
    run_interactive_session,
)


# ==================== get_operation_registry Tests ====================


def test_registry_contains_all_12_operations():
    """Verify that the registry contains exactly 12 operations."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    assert len(registry) == 12
    expected_ops = {
        "add", "subtract", "multiply", "divide", "power",
        "factorial", "square", "cube", "square_root", "cube_root",
        "log", "ln"
    }
    assert set(registry.keys()) == expected_ops


def test_registry_values_are_tuples_with_arity():
    """Verify each registry value is a 2-tuple with (method, arity)."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    for name, value in registry.items():
        assert isinstance(value, tuple), f"{name} value is not a tuple"
        assert len(value) == 2, f"{name} value is not a 2-tuple"
        method, arity = value
        assert callable(method), f"{name} method is not callable"
        assert isinstance(arity, int), f"{name} arity is not an int"


def test_binary_operations_have_arity_2():
    """Verify binary operations have arity 2."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    binary_ops = {"add", "subtract", "multiply", "divide", "power"}
    for op in binary_ops:
        _, arity = registry[op]
        assert arity == 2, f"{op} should have arity 2, got {arity}"


def test_unary_operations_have_arity_1():
    """Verify unary operations have arity 1."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    unary_ops = {"factorial", "square", "cube", "square_root", "cube_root", "log", "ln"}
    for op in unary_ops:
        _, arity = registry[op]
        assert arity == 1, f"{op} should have arity 1, got {arity}"


def test_registry_methods_are_bound_to_calculator():
    """Verify that each method is bound to the calculator instance."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    # Test that we can call a method
    method, _ = registry["add"]
    result = method(2, 3)
    assert result == 5


def test_registry_with_different_calculator_instances():
    """Verify registry works with multiple calculator instances."""
    calc1 = Calculator()
    calc2 = Calculator()
    reg1 = get_operation_registry(calc1)
    reg2 = get_operation_registry(calc2)
    # Both should have same operations
    assert set(reg1.keys()) == set(reg2.keys())
    # But methods should be different (bound to different instances)
    assert reg1["add"][0] is not reg2["add"][0]


# ==================== display_menu Tests ====================


def test_display_menu_outputs_all_operations():
    """Verify display_menu prints all operation names."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.print") as mock_print:
        display_menu(registry)
        # Get all printed lines
        printed = [call.args[0] for call in mock_print.call_args_list]
        output = "\n".join(str(p) for p in printed)
        # Check all operations are mentioned
        for op_name in registry.keys():
            assert op_name in output


def test_display_menu_contains_quit_option():
    """Verify display_menu includes a quit option."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.print") as mock_print:
        display_menu(registry)
        printed = [call.args[0] for call in mock_print.call_args_list]
        output = "\n".join(str(p) for p in printed)
        assert "quit" in output


def test_display_menu_shows_arity_hints():
    """Verify display_menu displays arity information."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.print") as mock_print:
        display_menu(registry)
        printed = [call.args[0] for call in mock_print.call_args_list]
        output = "\n".join(str(p) for p in printed)
        # Should mention operands
        assert "operand" in output


def test_display_menu_numbered_operations():
    """Verify operations are numbered starting from 1."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.print") as mock_print:
        display_menu(registry)
        printed = [call.args[0] for call in mock_print.call_args_list]
        output = "\n".join(str(p) for p in printed)
        # Check that numbers 1 and 12 are present
        assert "1." in output
        assert "12." in output


# ==================== get_operation_choice Tests ====================


def test_get_operation_choice_by_name():
    """Test selecting operation by name."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", return_value="add"):
        name, method, arity = get_operation_choice(registry)
        assert name == "add"
        assert arity == 2
        assert method(2, 3) == 5


def test_get_operation_choice_by_name_case_insensitive():
    """Test that operation selection is case-insensitive."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", return_value="ADD"):
        name, method, arity = get_operation_choice(registry)
        assert name == "add"
        assert arity == 2
        assert method(2, 3) == 5


def test_get_operation_choice_by_number():
    """Test selecting operation by 1-based number."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", return_value="1"):
        name, method, arity = get_operation_choice(registry)
        assert name == "add"
        assert method(2, 3) == 5  # "1" should be "add"


def test_get_operation_choice_by_number_various():
    """Test selecting various operations by number."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    # Get the 6th operation (should be factorial)
    ops_list = list(registry.keys())
    with patch("builtins.input", return_value="6"):
        name, method, arity = get_operation_choice(registry)
        assert name == "factorial"
        assert arity == 1
        assert method(5) == 120  # factorial(5)


def test_get_operation_choice_quit_with_q():
    """Test quit with 'q' returns None."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", return_value="q"):
        result = get_operation_choice(registry)
        assert result is None


def test_get_operation_choice_quit_with_quit():
    """Test quit with 'quit' returns None."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", return_value="quit"):
        result = get_operation_choice(registry)
        assert result is None


def test_get_operation_choice_quit_with_exit():
    """Test quit with 'exit' returns None."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", return_value="exit"):
        result = get_operation_choice(registry)
        assert result is None


def test_get_operation_choice_quit_case_insensitive():
    """Test that quit commands are case-insensitive."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", return_value="QUIT"):
        result = get_operation_choice(registry)
        assert result is None


def test_get_operation_choice_invalid_then_valid():
    """Test that invalid input triggers reprompt, then valid input succeeds."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", side_effect=["invalid", "add"]):
        with patch("builtins.print") as mock_print:
            name, method, arity = get_operation_choice(registry)
            assert name == "add"
            assert arity == 2
            # Verify that an error message was printed
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "Unknown operation" in output or "Type a name" in output


def test_get_operation_choice_invalid_number_then_valid():
    """Test that invalid number triggers reprompt."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", side_effect=["99", "add"]):
        with patch("builtins.print") as mock_print:
            name, method, arity = get_operation_choice(registry)
            assert name == "add"
            assert arity == 2
            # Verify that an error message was printed
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "Invalid number" in output


def test_get_operation_choice_multiple_invalid_then_valid():
    """Test multiple invalid inputs before a valid one (within limit)."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    # 3 invalid inputs + 1 valid = 4 total, within the 5 limit
    with patch("builtins.input", side_effect=["xyz", "", "123abc", "add"]):
        with patch("builtins.print"):
            name, method, arity = get_operation_choice(registry)
            assert name == "add"
            assert arity == 2


def test_get_operation_choice_empty_string_then_valid():
    """Test that empty string (stripped) triggers reprompt."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", side_effect=["   ", "add"]):
        with patch("builtins.print"):
            name, method, arity = get_operation_choice(registry)
            assert name == "add"
            assert arity == 2


def test_get_operation_choice_whitespace_input():
    """Test that whitespace-only input is handled."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", side_effect=["\t\n", "square"]):
        with patch("builtins.print"):
            name, method, arity = get_operation_choice(registry)
            assert name == "square"
            assert arity == 1


def test_get_operation_choice_zero_number():
    """Test that '0' is an invalid number (1-based indexing)."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", side_effect=["0", "add"]):
        with patch("builtins.print"):
            name, method, arity = get_operation_choice(registry)
            assert name == "add"
            assert arity == 2


def test_get_operation_choice_negative_number():
    """Test that negative numbers are invalid."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", side_effect=["-1", "add"]):
        with patch("builtins.print"):
            name, method, arity = get_operation_choice(registry)
            assert name == "add"
            assert arity == 2


def test_get_operation_choice_max_attempts_reached():
    """Test that 5 consecutive invalid inputs return (None, None, None) sentinel."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    # 5 invalid invalid inputs should trigger max attempts
    with patch("builtins.input", side_effect=["bad1", "bad2", "bad3", "bad4", "bad5"]):
        with patch("builtins.print") as mock_print:
            result = get_operation_choice(registry)
            assert result == (None, None, None)
            # Verify termination message was printed
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "Maximum invalid input attempts reached" in output


def test_get_operation_choice_recovers_before_max():
    """Test that 4 invalid then 1 valid succeeds before hitting limit."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    # 4 invalid + 1 valid = success before the 5th attempt
    with patch("builtins.input", side_effect=["bad1", "bad2", "bad3", "bad4", "add"]):
        with patch("builtins.print"):
            name, method, arity = get_operation_choice(registry)
            assert name == "add"
            assert arity == 2
            assert method(2, 3) == 5


def test_get_operation_choice_displays_operations_on_invalid():
    """Test that error message lists available operations."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", side_effect=["invalid", "add"]):
        with patch("builtins.print") as mock_print:
            get_operation_choice(registry)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            # Should show available operations
            assert "Available operations" in output or "add" in output


def test_get_operation_choice_mixed_invalid_types():
    """Test that mixing bad names and bad numbers shares the counter."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    # Mix bad names and out-of-range numbers: all count toward the same limit
    with patch("builtins.input", side_effect=["badname", "999", "xyz", "888", "badname"]):
        with patch("builtins.print") as mock_print:
            result = get_operation_choice(registry)
            assert result == (None, None, None)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "Maximum invalid input attempts reached" in output


def test_get_operation_choice_attempt_counting():
    """Test attempt counter increments correctly for each invalid input."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    # Should print error message 3 times before valid input
    with patch("builtins.input", side_effect=["bad1", "bad2", "bad3", "add"]):
        with patch("builtins.print") as mock_print:
            name, method, arity = get_operation_choice(registry)
            assert name == "add"
            assert arity == 2
            # Count error messages (should be 3 for the 3 invalid attempts)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            # Each invalid input should trigger an error message
            assert "Unknown operation" in output or "Invalid number" in output


# ==================== get_operands Tests ====================


def test_get_operands_single_integer():
    """Test collecting a single integer operand."""
    with patch("builtins.input", return_value="5"):
        operands = get_operands(1)
        assert operands == [5.0]


def test_get_operands_single_float():
    """Test collecting a single float operand."""
    with patch("builtins.input", return_value="3.14"):
        operands = get_operands(1)
        assert len(operands) == 1
        assert abs(operands[0] - 3.14) < 0.001


def test_get_operands_negative_number():
    """Test collecting negative operands."""
    with patch("builtins.input", return_value="-5"):
        operands = get_operands(1)
        assert operands == [-5.0]


def test_get_operands_two_operands():
    """Test collecting two operands for binary operation."""
    with patch("builtins.input", side_effect=["3", "4"]):
        operands = get_operands(2)
        assert operands == [3.0, 4.0]


def test_get_operands_three_operands():
    """Test collecting three operands."""
    with patch("builtins.input", side_effect=["1", "2", "3"]):
        operands = get_operands(3)
        assert operands == [1.0, 2.0, 3.0]


def test_get_operands_zero_operands():
    """Test collecting zero operands (edge case)."""
    operands = get_operands(0)
    assert operands == []


def test_get_operands_large_number():
    """Test collecting very large numbers."""
    with patch("builtins.input", return_value="999999999999999.5"):
        operands = get_operands(1)
        assert operands[0] == 999999999999999.5


def test_get_operands_scientific_notation():
    """Test collecting numbers in scientific notation."""
    with patch("builtins.input", return_value="1e-5"):
        operands = get_operands(1)
        assert abs(operands[0] - 1e-5) < 1e-10


def test_get_operands_invalid_then_valid():
    """Test that invalid input triggers reprompt."""
    with patch("builtins.input", side_effect=["abc", "5"]):
        with patch("builtins.print") as mock_print:
            operands = get_operands(1)
            assert operands == [5.0]
            # Verify error message was printed
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "not a valid number" in output or "numeric value" in output


def test_get_operands_multiple_invalid_then_valid():
    """Test multiple invalid inputs before valid."""
    with patch("builtins.input", side_effect=["", "xyz", "3.5", "2"]):
        with patch("builtins.print"):
            operands = get_operands(2)
            assert operands == [3.5, 2.0]


def test_get_operands_whitespace_handled():
    """Test that leading/trailing whitespace is handled."""
    with patch("builtins.input", return_value="  3.5  "):
        operands = get_operands(1)
        assert operands == [3.5]


def test_get_operands_empty_string_then_valid():
    """Test that empty string is rejected."""
    with patch("builtins.input", side_effect=["", "5"]):
        with patch("builtins.print"):
            operands = get_operands(1)
            assert operands == [5.0]


def test_get_operands_special_chars_rejected():
    """Test that inputs with special characters are rejected."""
    with patch("builtins.input", side_effect=["5@#$", "5"]):
        with patch("builtins.print"):
            operands = get_operands(1)
            assert operands == [5.0]


def test_get_operands_mixed_valid_types():
    """Test collecting mix of ints and floats."""
    with patch("builtins.input", side_effect=["5", "3.14", "-2"]):
        operands = get_operands(3)
        assert operands == [5.0, 3.14, -2.0]


def test_get_operands_max_attempts_reached():
    """Test that 5 consecutive invalid numeric entries return None."""
    # 5 invalid numeric inputs should trigger max attempts
    with patch("builtins.input", side_effect=["bad1", "bad2", "bad3", "bad4", "bad5"]):
        with patch("builtins.print") as mock_print:
            result = get_operands(1)
            assert result is None
            # Verify termination message was printed
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "Maximum invalid input attempts reached" in output


def test_get_operands_recovers_within_limit():
    """Test that 3 invalid then 1 valid succeeds within 5-attempt limit."""
    # 3 invalid + 1 valid = success before hitting 5
    with patch("builtins.input", side_effect=["bad1", "bad2", "bad3", "5"]):
        with patch("builtins.print"):
            operands = get_operands(1)
            assert operands == [5.0]


def test_get_operands_cross_slot_counting():
    """Test that attempt count is shared across operand slots."""
    # Binary operation: 3 bad on operand 1, 2 bad on operand 2 = 5 total = max
    with patch("builtins.input", side_effect=["bad1", "bad2", "bad3", "bad4", "bad5"]):
        with patch("builtins.print") as mock_print:
            result = get_operands(2)
            assert result is None
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "Maximum invalid input attempts reached" in output


def test_get_operands_cross_slot_no_exceed():
    """Test cross-slot counting when total attempts is below 5."""
    # 2 bad on operand 1, then 1 valid, then 1 bad on operand 2, then 1 valid
    # Total bad = 3, which is < 5, so should succeed
    with patch("builtins.input", side_effect=["bad1", "bad2", "3.5", "bad3", "2.0"]):
        with patch("builtins.print"):
            operands = get_operands(2)
            assert operands == [3.5, 2.0]


def test_get_operands_exactly_at_limit_second_operand():
    """Test that hitting limit on second operand returns None."""
    # First operand: 1 valid
    # Second operand: 4 invalid inputs (brings cumulative to 4)
    # Fifth invalid should trigger max attempts
    with patch("builtins.input", side_effect=["5", "bad1", "bad2", "bad3", "bad4", "bad5"]):
        with patch("builtins.print") as mock_print:
            result = get_operands(2)
            assert result is None
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "Maximum invalid input attempts reached" in output


# ==================== run_interactive_session Tests ====================


def test_run_interactive_session_quit_immediately():
    """Test that session exits on quit command."""
    calc = Calculator()
    with patch("builtins.input", return_value="q"):
        with patch("builtins.print"):
            run_interactive_session(calc)
            # Should not raise


def test_run_interactive_session_binary_operation():
    """Test full session with binary operation (add 3 + 5)."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["add", "3", "5", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "8" in output


def test_run_interactive_session_unary_operation():
    """Test full session with unary operation (square of 4)."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["square", "4", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "16" in output


def test_run_interactive_session_by_number():
    """Test selecting operation by number."""
    calc = Calculator()
    # 2 is subtract
    with patch("builtins.input", side_effect=["2", "10", "3", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "7" in output


def test_run_interactive_session_division_by_zero_error():
    """Test that division by zero is caught and session continues."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["divide", "5", "0", "add", "2", "3", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            # Should show error message
            assert "Error" in output
            # But continue and process the next operation
            assert "5" in output  # result of 2 + 3


def test_run_interactive_session_factorial_with_whole_float():
    """Test that factorial accepts whole-valued floats (e.g., '5.0')."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["factorial", "5.0", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "120" in output


def test_run_interactive_session_factorial_with_non_integer_float():
    """Test that non-integer floats for factorial are caught."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["factorial", "5.5", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            # Should show error message
            assert "Error" in output


def test_run_interactive_session_multiple_operations():
    """Test session with multiple operations in sequence."""
    calc = Calculator()
    with patch("builtins.input", side_effect=[
        "add", "2", "3",
        "multiply", "4", "5",
        "q"
    ]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "5" in output  # 2 + 3
            assert "20" in output  # 4 * 5


def test_run_interactive_session_ln_operation():
    """Test logarithm operation."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["ln", "1", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "0" in output  # ln(1) = 0


def test_run_interactive_session_square_root():
    """Test square root operation."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["square_root", "9", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "3.0" in output  # sqrt(9) = 3.0


def test_run_interactive_session_square_root_negative_error():
    """Test that square root of negative number is caught."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["square_root", "-1", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "Error" in output


def test_run_interactive_session_cube_root():
    """Test cube root operation."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["cube_root", "27", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "3" in output  # cube_root(27) = 3.0


def test_run_interactive_session_power_operation():
    """Test power operation."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["power", "2", "3", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "8" in output  # 2^3 = 8


def test_run_interactive_session_welcome_message():
    """Test that welcome message is displayed."""
    calc = Calculator()
    with patch("builtins.input", return_value="q"):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "Welcome" in output or "welcome" in output.lower()


def test_run_interactive_session_goodbye_message():
    """Test that goodbye message is displayed on quit."""
    calc = Calculator()
    with patch("builtins.input", return_value="q"):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "Goodbye" in output or "goodbye" in output.lower()


def test_run_interactive_session_invalid_operation_then_valid():
    """Test that invalid operation name prompts for retry."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["xyz", "add", "2", "3", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "5" in output  # 2 + 3


def test_run_interactive_session_log_operation():
    """Test base-10 logarithm operation."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["log", "100", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "2" in output  # log10(100) = 2.0


def test_run_interactive_session_cube():
    """Test cube operation."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["cube", "3", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "27" in output  # 3^3 = 27


def test_run_interactive_session_factorial_zero():
    """Test factorial of zero."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["factorial", "0", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "1" in output  # 0! = 1


def test_run_interactive_session_negative_factorial_error():
    """Test that negative factorial is caught."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["factorial", "-1", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "Error" in output


def test_run_interactive_session_ln_negative_error():
    """Test that ln of negative number is caught."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["ln", "-5", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "Error" in output


def test_run_interactive_session_exit_token():
    """Test that 'exit' token works to quit session."""
    calc = Calculator()
    with patch("builtins.input", return_value="exit"):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "Goodbye" in output


def test_run_interactive_session_quit_token():
    """Test that 'quit' token works to quit session."""
    calc = Calculator()
    with patch("builtins.input", return_value="quit"):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "Goodbye" in output


def test_run_interactive_session_operation_max_attempts():
    """Test session exits after 5 invalid operation selections."""
    calc = Calculator()
    # 5 invalid operations should trigger max attempts and exit
    with patch("builtins.input", side_effect=["bad1", "bad2", "bad3", "bad4", "bad5"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            # Should show the termination message
            assert "Maximum invalid input attempts reached" in output
            # Should NOT show "Goodbye." (that's only for explicit quit)
            assert "Goodbye" not in output


def test_run_interactive_session_operand_max_attempts():
    """Test session exits after 5 invalid operand entries."""
    calc = Calculator()
    # 1 valid operation, then 5 invalid operands should exit
    with patch("builtins.input", side_effect=["add", "bad1", "bad2", "bad3", "bad4", "bad5"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            # Should show the termination message
            assert "Maximum invalid input attempts reached" in output
            # Should NOT show "Goodbye."
            assert "Goodbye" not in output


def test_run_interactive_session_terminates_without_goodbye_on_max_attempts():
    """Verify the 'Goodbye.' message does NOT appear on max attempts."""
    calc = Calculator()
    # 5 invalid operations
    with patch("builtins.input", side_effect=["x1", "x2", "x3", "x4", "x5"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            # Verify termination message present
            assert "Maximum invalid input attempts reached" in output
            # Verify Goodbye is NOT present
            goodbye_count = output.count("Goodbye")
            assert goodbye_count == 0, "Goodbye should not appear on max attempts"


def test_run_interactive_session_normal_quit_still_prints_goodbye():
    """Test that explicit quit (q) still prints Goodbye."""
    calc = Calculator()
    with patch("builtins.input", return_value="q"):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            # Explicit quit should show Goodbye
            assert "Goodbye" in output
            # But not the max attempts message
            assert "Maximum invalid input attempts reached" not in output


def test_run_interactive_session_successful_operation_continues():
    """Test that successful operations continue normally without breaking."""
    calc = Calculator()
    # Add, then subtract, then quit
    with patch("builtins.input", side_effect=["add", "2", "3", "subtract", "10", "4", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "5" in output  # 2 + 3
            assert "6" in output  # 10 - 4
            assert "Goodbye" in output


# ==================== Parametrized Tests ====================


@pytest.mark.parametrize("op_name,a,b,expected", [
    ("add", 5, 3, 8),
    ("subtract", 10, 4, 6),
    ("multiply", 4, 7, 28),
    ("divide", 12, 4, 3.0),
])
def test_session_binary_operations(op_name, a, b, expected):
    """Test session with various binary operations."""
    calc = Calculator()
    with patch("builtins.input", side_effect=[op_name, str(a), str(b), "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert str(expected) in output


@pytest.mark.parametrize("op_name,value,expected", [
    ("square", 5, 25),
    ("cube", 2, 8),
    ("factorial", 4, 24),
])
def test_session_unary_operations(op_name, value, expected):
    """Test session with various unary operations."""
    calc = Calculator()
    with patch("builtins.input", side_effect=[op_name, str(value), "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert str(expected) in output


@pytest.mark.parametrize("invalid_input", [
    "nonexistent_op",
    "sqrt",  # wrong name
    "100",  # out of range
    "",  # empty
])
def test_get_operation_choice_invalid_inputs(invalid_input):
    """Test that various invalid inputs are rejected and reprompt occurs."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", side_effect=[invalid_input, "add"]):
        with patch("builtins.print"):
            name, method, arity = get_operation_choice(registry)
            assert name == "add"
            assert arity == 2


@pytest.mark.parametrize("numeric_input", [
    "5",
    "3.14",
    "-2.5",
    "1e3",
])
def test_get_operands_numeric_inputs(numeric_input):
    """Test that various numeric formats are accepted."""
    with patch("builtins.input", return_value=numeric_input):
        operands = get_operands(1)
        assert len(operands) == 1
        assert isinstance(operands[0], float)


# ==================== run_interactive_session with HistoryTracker ====================


def test_run_interactive_session_default_tracker_no_error():
    """Test calling run_interactive_session without history_tracker argument."""
    calc = Calculator()
    with patch("builtins.input", return_value="q"):
        with patch("builtins.print"):
            # Should not raise TypeError
            run_interactive_session(calc)


def test_run_interactive_session_records_history():
    """Test that operations are recorded in history."""
    from src.history import HistoryTracker
    calc = Calculator()
    tracker = HistoryTracker()
    with patch("builtins.input", side_effect=["add", "2", "3", "q"]):
        with patch("builtins.print"):
            run_interactive_session(calc, tracker)
    history = tracker.get_history()
    assert len(history) == 1
    # Operands are converted to floats by get_operands
    assert "add(2.0, 3.0) = 5.0" in history[0]


def test_run_interactive_session_records_multiple_operations():
    """Test recording multiple operations in a session."""
    from src.history import HistoryTracker
    calc = Calculator()
    tracker = HistoryTracker()
    with patch("builtins.input", side_effect=[
        "add", "2", "3",
        "multiply", "4", "5",
        "q"
    ]):
        with patch("builtins.print"):
            run_interactive_session(calc, tracker)
    history = tracker.get_history()
    assert len(history) == 2
    # Operands are converted to floats by get_operands
    assert history[0] == "add(2.0, 3.0) = 5.0"
    assert history[1] == "multiply(4.0, 5.0) = 20.0"


def test_run_interactive_session_history_display():
    """Test that 'h' command displays history."""
    from src.history import HistoryTracker
    calc = Calculator()
    tracker = HistoryTracker()
    with patch("builtins.input", side_effect=[
        "add", "2", "3",
        "h",
        "q"
    ]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc, tracker)
    # Check that history was displayed
    printed = [call.args[0] for call in mock_print.call_args_list]
    output = "\n".join(str(p) for p in printed)
    assert "Session history:" in output
    # Operands are converted to floats by get_operands
    assert "add(2.0, 3.0) = 5.0" in output


def test_run_interactive_session_history_empty_display():
    """Test displaying history when it's empty."""
    from src.history import HistoryTracker
    calc = Calculator()
    tracker = HistoryTracker()
    with patch("builtins.input", side_effect=["h", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc, tracker)
    printed = [call.args[0] for call in mock_print.call_args_list]
    output = "\n".join(str(p) for p in printed)
    assert "No history for this session." in output


def test_run_interactive_session_history_display_multiple_times():
    """Test displaying history multiple times in a session."""
    from src.history import HistoryTracker
    calc = Calculator()
    tracker = HistoryTracker()
    with patch("builtins.input", side_effect=[
        "add", "2", "3",
        "h",
        "multiply", "4", "5",
        "h",
        "q"
    ]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc, tracker)
    printed = [call.args[0] for call in mock_print.call_args_list]
    output = "\n".join(str(p) for p in printed)
    # First history display should have only add
    assert "add(2.0, 3.0) = 5.0" in output
    # Second history display should have both
    assert "multiply(4.0, 5.0) = 20.0" in output


def test_run_interactive_session_saves_on_quit(tmp_path):
    """Test that history is saved to file on quit."""
    from src.history import HistoryTracker
    import os
    calc = Calculator()
    tracker = HistoryTracker()
    filepath = tmp_path / "test_history.txt"
    # Change to temp directory
    original_cwd = os.getcwd()
    try:
        os.chdir(str(tmp_path))
        with patch("builtins.input", side_effect=["add", "2", "3", "q"]):
            with patch("builtins.print"):
                run_interactive_session(calc, tracker)
        # Default filename is "history.txt"
        assert Path(tmp_path / "history.txt").exists()
    finally:
        os.chdir(original_cwd)


def test_run_interactive_session_does_not_record_error_operations():
    """Test that failed operations (errors) are not recorded in history."""
    from src.history import HistoryTracker
    calc = Calculator()
    tracker = HistoryTracker()
    with patch("builtins.input", side_effect=[
        "divide", "5", "0",  # Will error
        "add", "2", "3",  # Will succeed
        "q"
    ]):
        with patch("builtins.print"):
            run_interactive_session(calc, tracker)
    history = tracker.get_history()
    # Only the successful add should be recorded
    assert len(history) == 1
    # Operands are converted to floats by get_operands
    assert "add(2.0, 3.0) = 5.0" in history[0]


def test_run_interactive_session_error_continues_session():
    """Test that errors don't prevent recording subsequent operations."""
    from src.history import HistoryTracker
    calc = Calculator()
    tracker = HistoryTracker()
    with patch("builtins.input", side_effect=[
        "factorial", "5.5",  # Error: float not int
        "add", "2", "3",
        "q"
    ]):
        with patch("builtins.print"):
            run_interactive_session(calc, tracker)
    history = tracker.get_history()
    # Only the successful add should be recorded
    assert len(history) == 1
    # Operands are converted to floats by get_operands
    assert "add(2.0, 3.0) = 5.0" in history[0]


def test_run_interactive_session_h_command_in_menu():
    """Test that 'h' command is recognized in the menu."""
    from src.history import HistoryTracker
    calc = Calculator()
    tracker = HistoryTracker()
    with patch("builtins.input", side_effect=["add", "1", "2", "h", "q"]):
        with patch("builtins.print") as mock_print:
            run_interactive_session(calc, tracker)
    # Verify the menu was displayed and history option shown
    printed = [call.args[0] for call in mock_print.call_args_list]
    output = "\n".join(str(p) for p in printed)
    assert "View history" in output or "history" in output.lower()


def test_run_interactive_session_history_preserves_order():
    """Test that history maintains insertion order of operations."""
    from src.history import HistoryTracker
    calc = Calculator()
    tracker = HistoryTracker()
    with patch("builtins.input", side_effect=[
        "add", "1", "2",
        "multiply", "3", "4",
        "subtract", "10", "5",
        "q"
    ]):
        with patch("builtins.print"):
            run_interactive_session(calc, tracker)
    history = tracker.get_history()
    assert len(history) == 3
    assert "add" in history[0]
    assert "multiply" in history[1]
    assert "subtract" in history[2]


def test_run_interactive_session_factorial_float_conversion_recorded():
    """Test that factorial with float input is recorded with converted int."""
    from src.history import HistoryTracker
    calc = Calculator()
    tracker = HistoryTracker()
    with patch("builtins.input", side_effect=["factorial", "5.0", "q"]):
        with patch("builtins.print"):
            run_interactive_session(calc, tracker)
    history = tracker.get_history()
    assert len(history) == 1
    # The operand is converted from float 5.0 to int 5 for factorial
    assert "factorial(5)" in history[0]
    assert "= 120" in history[0]


def test_run_interactive_session_with_none_tracker_creates_default():
    """Test that passing None for history_tracker creates a default."""
    calc = Calculator()
    with patch("builtins.input", side_effect=["add", "2", "3", "q"]):
        with patch("builtins.print"):
            # Should not raise
            run_interactive_session(calc, None)


def test_run_interactive_session_history_saved_with_custom_path(tmp_path):
    """Test saving history with a custom tracker path."""
    from src.history import HistoryTracker
    calc = Calculator()
    tracker = HistoryTracker()
    # We can't easily test custom save path without modifying run_interactive_session
    # so we test that default behavior works
    import os
    original_cwd = os.getcwd()
    try:
        os.chdir(str(tmp_path))
        with patch("builtins.input", side_effect=["add", "5", "3", "q"]):
            with patch("builtins.print"):
                run_interactive_session(calc, tracker)
        # Check that history.txt was created with expected content
        history_file = tmp_path / "history.txt"
        assert history_file.exists()
        content = history_file.read_text()
        # Operands are converted to floats by get_operands
        assert "add(5.0, 3.0) = 8.0" in content
    finally:
        os.chdir(original_cwd)


def test_get_operation_choice_returns_history_token():
    """Test that get_operation_choice returns history token on 'h'."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", return_value="h"):
        result = get_operation_choice(registry)
        assert result == ("h", None, None)


def test_get_operation_choice_history_token_case_insensitive():
    """Test that 'h' command is case-insensitive."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", return_value="H"):
        result = get_operation_choice(registry)
        # The function converts to lowercase, so "H" becomes "h"
        assert result == ("h", None, None)


def test_display_menu_shows_history_option():
    """Test that display_menu shows the history option."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.print") as mock_print:
        display_menu(registry)
        printed = [call.args[0] for call in mock_print.call_args_list]
        output = "\n".join(str(p) for p in printed)
        assert "history" in output.lower()
        assert "h." in output or "h " in output
