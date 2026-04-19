"""Tests for the interactive input handler module."""

import pytest
import io
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
        method, arity = get_operation_choice(registry)
        assert arity == 2
        assert method(2, 3) == 5


def test_get_operation_choice_by_name_case_insensitive():
    """Test that operation selection is case-insensitive."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", return_value="ADD"):
        method, arity = get_operation_choice(registry)
        assert arity == 2
        assert method(2, 3) == 5


def test_get_operation_choice_by_number():
    """Test selecting operation by 1-based number."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", return_value="1"):
        method, arity = get_operation_choice(registry)
        assert method(2, 3) == 5  # "1" should be "add"


def test_get_operation_choice_by_number_various():
    """Test selecting various operations by number."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    # Get the 6th operation (should be factorial)
    ops_list = list(registry.keys())
    with patch("builtins.input", return_value="6"):
        method, arity = get_operation_choice(registry)
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
            method, arity = get_operation_choice(registry)
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
            method, arity = get_operation_choice(registry)
            assert arity == 2
            # Verify that an error message was printed
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "Invalid number" in output


def test_get_operation_choice_multiple_invalid_then_valid():
    """Test multiple invalid inputs before a valid one."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", side_effect=["xyz", "", "123abc", "add"]):
        with patch("builtins.print"):
            method, arity = get_operation_choice(registry)
            assert arity == 2


def test_get_operation_choice_empty_string_then_valid():
    """Test that empty string (stripped) triggers reprompt."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", side_effect=["   ", "add"]):
        with patch("builtins.print"):
            method, arity = get_operation_choice(registry)
            assert arity == 2


def test_get_operation_choice_whitespace_input():
    """Test that whitespace-only input is handled."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", side_effect=["\t\n", "square"]):
        with patch("builtins.print"):
            method, arity = get_operation_choice(registry)
            assert arity == 1


def test_get_operation_choice_zero_number():
    """Test that '0' is an invalid number (1-based indexing)."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", side_effect=["0", "add"]):
        with patch("builtins.print"):
            method, arity = get_operation_choice(registry)
            assert arity == 2


def test_get_operation_choice_negative_number():
    """Test that negative numbers are invalid."""
    calc = Calculator()
    registry = get_operation_registry(calc)
    with patch("builtins.input", side_effect=["-1", "add"]):
        with patch("builtins.print"):
            method, arity = get_operation_choice(registry)
            assert arity == 2


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
            method, arity = get_operation_choice(registry)
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
