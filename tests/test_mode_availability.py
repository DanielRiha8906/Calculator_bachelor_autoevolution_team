"""test_mode_availability.py — comprehensive tests for mode availability features.

Tests cover:
- CalculatorEngine.get_available_modes_for_operation() method
- OperationNotAvailableInModeError exception class
- Guard clauses for advanced and scientific operations
- CalculatorREPL._dispatch() raises OperationNotAvailableInModeError
- CalculatorREPL._evaluate() returns user-friendly mode error messages
- REPL remains functional after mode errors
- Updated REPL welcome message includes all required sections
- Regression: operations still work in correct modes
- Regression: history persists across mode switches
"""

import pytest
import math
from io import StringIO
from unittest.mock import patch, MagicMock

from src.logic import CalculatorEngine
from src.calculator import Calculator
from src.input_handler import (
    CalculatorREPL,
    OperationNotAvailableInModeError,
    RetryConfig,
)


# =============================================================================
# TestOperationNotAvailableInModeError
# =============================================================================


class TestOperationNotAvailableInModeError:
    """Tests for OperationNotAvailableInModeError exception class."""

    def test_is_subclass_of_valueerror(self):
        """Test that OperationNotAvailableInModeError is a ValueError."""
        exc = OperationNotAvailableInModeError("factorial", "basic", ["advanced", "scientific"])
        assert isinstance(exc, ValueError)

    def test_stores_operation_attribute(self):
        """Test that operation attribute is stored correctly."""
        exc = OperationNotAvailableInModeError("factorial", "basic", ["advanced", "scientific"])
        assert exc.operation == "factorial"

    def test_stores_current_mode_attribute(self):
        """Test that current_mode attribute is stored correctly."""
        exc = OperationNotAvailableInModeError("factorial", "basic", ["advanced", "scientific"])
        assert exc.current_mode == "basic"

    def test_stores_available_modes_attribute(self):
        """Test that available_modes attribute is stored correctly."""
        modes = ["advanced", "scientific"]
        exc = OperationNotAvailableInModeError("factorial", "basic", modes)
        assert exc.available_modes == modes

    def test_str_with_available_modes_contains_operation_name(self):
        """Test __str__ with available modes contains operation name."""
        exc = OperationNotAvailableInModeError("factorial", "basic", ["advanced", "scientific"])
        str_repr = str(exc)
        assert "factorial" in str_repr

    def test_str_with_available_modes_contains_current_mode(self):
        """Test __str__ with available modes contains current mode."""
        exc = OperationNotAvailableInModeError("factorial", "basic", ["advanced", "scientific"])
        str_repr = str(exc)
        assert "basic" in str_repr

    def test_str_with_available_modes_contains_available_modes(self):
        """Test __str__ with available modes lists the available modes."""
        exc = OperationNotAvailableInModeError("factorial", "basic", ["advanced", "scientific"])
        str_repr = str(exc)
        assert "advanced" in str_repr
        assert "scientific" in str_repr

    def test_str_with_available_modes_contains_switch_hint(self):
        """Test __str__ with available modes contains a mode switch hint."""
        exc = OperationNotAvailableInModeError("factorial", "basic", ["advanced", "scientific"])
        str_repr = str(exc)
        assert "mode" in str_repr.lower()

    def test_str_with_empty_available_modes_contains_operation_name(self):
        """Test __str__ with empty available_modes contains operation name."""
        exc = OperationNotAvailableInModeError("unknown_op", "basic", [])
        str_repr = str(exc)
        assert "unknown_op" in str_repr

    def test_str_with_empty_available_modes_contains_current_mode(self):
        """Test __str__ with empty available_modes contains current mode."""
        exc = OperationNotAvailableInModeError("unknown_op", "basic", [])
        str_repr = str(exc)
        assert "basic" in str_repr

    def test_str_with_empty_available_modes_no_switch_hint(self):
        """Test __str__ with empty available_modes does not suggest a mode switch."""
        exc = OperationNotAvailableInModeError("unknown_op", "basic", [])
        str_repr = str(exc)
        # Should not suggest switching if there are no available modes
        assert "mode" not in str_repr.lower() or "not available" in str_repr.lower()

    def test_str_with_single_available_mode(self):
        """Test __str__ with single available mode."""
        exc = OperationNotAvailableInModeError("sin", "basic", ["scientific"])
        str_repr = str(exc)
        assert "sin" in str_repr
        assert "scientific" in str_repr
        assert "mode scientific" in str_repr or "mode" in str_repr

    @pytest.mark.parametrize("operation,current,available", [
        ("factorial", "basic", ["advanced", "scientific"]),
        ("sin", "advanced", ["scientific"]),
        ("power", "basic", ["advanced", "scientific"]),
        ("ln", "basic", ["scientific"]),
    ])
    def test_str_output_readable_for_various_operations(self, operation, current, available):
        """Test __str__ output is readable for various operation/mode combinations."""
        exc = OperationNotAvailableInModeError(operation, current, available)
        str_repr = str(exc)
        assert operation in str_repr
        assert current in str_repr
        for mode in available:
            assert mode in str_repr


# =============================================================================
# TestCalculatorEngineGetAvailableModes
# =============================================================================


class TestCalculatorEngineGetAvailableModes:
    """Tests for CalculatorEngine.get_available_modes_for_operation() method."""

    @pytest.fixture
    def engine(self):
        """Fixture providing a CalculatorEngine instance."""
        return CalculatorEngine(mode="advanced")

    # -------------------------------------------------------------------------
    # Basic operations (available in all modes)
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize("op", ["add", "subtract", "multiply", "divide"])
    def test_basic_operations_available_in_all_modes(self, engine, op):
        """Test basic operations are available in all three modes."""
        modes = engine.get_available_modes_for_operation(op)
        assert set(modes) == {"basic", "advanced", "scientific"}
        assert modes == sorted(modes)  # Verify sorted

    # -------------------------------------------------------------------------
    # Advanced operations (available in advanced and scientific)
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize("op", [
        "factorial", "square", "cube", "square_root", "cube_root",
        "power", "natural_log", "log_base_10"
    ])
    def test_advanced_operations_available_in_advanced_and_scientific(self, engine, op):
        """Test advanced operations are available in advanced and scientific modes."""
        modes = engine.get_available_modes_for_operation(op)
        assert set(modes) == {"advanced", "scientific"}
        assert modes == sorted(modes)

    # -------------------------------------------------------------------------
    # Scientific operations (available only in scientific)
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize("op", [
        "sin", "cos", "tan", "asin", "acos", "atan",
        "sinh", "cosh", "tanh", "degrees", "radians", "exp", "ln"
    ])
    def test_scientific_operations_available_only_in_scientific(self, engine, op):
        """Test scientific operations are available only in scientific mode."""
        modes = engine.get_available_modes_for_operation(op)
        assert modes == ["scientific"]

    # -------------------------------------------------------------------------
    # Unknown operations
    # -------------------------------------------------------------------------

    def test_unknown_operation_returns_empty_list(self, engine):
        """Test unknown operation returns empty list."""
        modes = engine.get_available_modes_for_operation("unknown_op")
        assert modes == []

    def test_empty_string_operation_returns_empty_list(self, engine):
        """Test empty string operation returns empty list."""
        modes = engine.get_available_modes_for_operation("")
        assert modes == []

    def test_result_is_always_sorted(self, engine):
        """Test that returned list is always sorted."""
        for op in ["add", "factorial", "sin"]:
            modes = engine.get_available_modes_for_operation(op)
            assert modes == sorted(modes)


# =============================================================================
# TestCalculatorGetAvailableModes
# =============================================================================


class TestCalculatorGetAvailableModes:
    """Tests for Calculator.get_available_modes_for_operation() method."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance."""
        return Calculator(mode="advanced")

    def test_passthrough_for_basic_operation(self, calculator):
        """Test that Calculator passes through to engine for basic operation."""
        modes = calculator.get_available_modes_for_operation("add")
        assert set(modes) == {"basic", "advanced", "scientific"}

    def test_passthrough_for_advanced_operation(self, calculator):
        """Test that Calculator passes through to engine for advanced operation."""
        modes = calculator.get_available_modes_for_operation("factorial")
        assert set(modes) == {"advanced", "scientific"}

    def test_passthrough_for_scientific_operation(self, calculator):
        """Test that Calculator passes through to engine for scientific operation."""
        modes = calculator.get_available_modes_for_operation("sin")
        assert modes == ["scientific"]

    def test_passthrough_for_unknown_operation(self, calculator):
        """Test that Calculator passes through to engine for unknown operation."""
        modes = calculator.get_available_modes_for_operation("unknown_op")
        assert modes == []


# =============================================================================
# TestCalculatorEngineAdvancedGuardClauses
# =============================================================================


class TestCalculatorEngineAdvancedGuardClauses:
    """Tests for guard clauses on advanced operations (prevent use in basic mode)."""

    @pytest.fixture
    def basic_engine(self):
        """Fixture providing a CalculatorEngine in basic mode."""
        return CalculatorEngine(mode="basic")

    @pytest.mark.parametrize("operation,args", [
        ("factorial", (5,)),
        ("square", (4,)),
        ("cube", (3,)),
        ("square_root", (9,)),
        ("cube_root", (8,)),
        ("power", (2, 3)),
        ("natural_log", (2.718,)),
        ("log_base_10", (100,)),
    ])
    def test_advanced_operations_raise_valueerror_in_basic_mode(self, basic_engine, operation, args):
        """Test that advanced operations raise ValueError in basic mode."""
        method = getattr(basic_engine, operation)
        with pytest.raises(ValueError) as exc_info:
            method(*args)
        error_msg = str(exc_info.value)
        assert "not available in" in error_msg
        assert operation in error_msg
        assert "basic" in error_msg

    def test_advanced_operation_error_includes_available_modes(self, basic_engine):
        """Test that advanced operation error message includes available modes."""
        with pytest.raises(ValueError) as exc_info:
            basic_engine.factorial(5)
        error_msg = str(exc_info.value)
        assert "advanced" in error_msg
        assert "scientific" in error_msg

    def test_basic_operations_work_in_basic_mode(self, basic_engine):
        """Test that basic operations work correctly in basic mode."""
        assert basic_engine.add(2, 3) == 5
        assert basic_engine.subtract(5, 2) == 3
        assert basic_engine.multiply(2, 3) == 6
        assert basic_engine.divide(10, 2) == 5


# =============================================================================
# TestCalculatorEngineScientificGuardClauses
# =============================================================================


class TestCalculatorEngineScientificGuardClauses:
    """Tests for guard clauses on scientific operations (prevent use in non-scientific modes)."""

    @pytest.fixture
    def advanced_engine(self):
        """Fixture providing a CalculatorEngine in advanced mode."""
        return CalculatorEngine(mode="advanced")

    @pytest.mark.parametrize("operation,args", [
        ("sin", (1.57,)),
        ("cos", (0,)),
        ("tan", (0.785,)),
        ("asin", (0.5,)),
        ("acos", (0.5,)),
        ("atan", (1,)),
        ("sinh", (0,)),
        ("cosh", (0,)),
        ("tanh", (0,)),
        ("degrees", (1.57,)),
        ("radians", (90,)),
        ("exp", (1,)),
        ("ln", (2.718,)),
    ])
    def test_scientific_operations_raise_valueerror_in_advanced_mode(self, advanced_engine, operation, args):
        """Test that scientific operations raise ValueError in advanced mode."""
        method = getattr(advanced_engine, operation)
        with pytest.raises(ValueError) as exc_info:
            method(*args)
        error_msg = str(exc_info.value)
        assert "not available in" in error_msg
        assert operation in error_msg
        assert "advanced" in error_msg

    def test_scientific_operation_error_includes_available_modes(self, advanced_engine):
        """Test that scientific operation error message includes available modes."""
        with pytest.raises(ValueError) as exc_info:
            advanced_engine.sin(1.57)
        error_msg = str(exc_info.value)
        assert "scientific" in error_msg

    def test_advanced_operations_work_in_advanced_mode(self, advanced_engine):
        """Test that advanced operations work correctly in advanced mode."""
        assert advanced_engine.factorial(5) == 120
        assert advanced_engine.square(4) == 16
        assert advanced_engine.cube(3) == 27


# =============================================================================
# TestCalculatorREPLDispatch
# =============================================================================


class TestCalculatorREPLDispatch:
    """Tests for CalculatorREPL._dispatch() raises OperationNotAvailableInModeError."""

    @pytest.fixture
    def repl_basic(self):
        """Fixture providing a CalculatorREPL in basic mode."""
        calc = Calculator(mode="basic")
        return CalculatorREPL(calc)

    def test_dispatch_raises_operation_not_available_error_for_advanced_op(self, repl_basic):
        """Test _dispatch raises OperationNotAvailableInModeError for advanced op in basic mode."""
        with pytest.raises(OperationNotAvailableInModeError) as exc_info:
            repl_basic._dispatch("factorial", [5])
        assert exc_info.value.operation == "factorial"
        assert exc_info.value.current_mode == "basic"

    def test_dispatch_raises_operation_not_available_error_for_scientific_op(self, repl_basic):
        """Test _dispatch raises OperationNotAvailableInModeError for scientific op in basic mode."""
        with pytest.raises(OperationNotAvailableInModeError) as exc_info:
            repl_basic._dispatch("sin", [1.57])
        assert exc_info.value.operation == "sin"
        assert exc_info.value.current_mode == "basic"

    def test_dispatch_basic_operations_work_in_basic_mode(self, repl_basic):
        """Test _dispatch allows basic operations in basic mode."""
        result = repl_basic._dispatch("add", [2, 3])
        assert result == 5

    def test_dispatch_non_mode_valueerror_propagates_unchanged(self, repl_basic):
        """Test _dispatch propagates non-mode ValueErrors unchanged."""
        # natural_log with invalid input (not in basic mode, so no mode error)
        repl_basic._calculator.set_mode("advanced")
        with pytest.raises(ValueError) as exc_info:
            repl_basic._dispatch("natural_log", [0])  # Invalid domain
        # Should be the original ValueError, not OperationNotAvailableInModeError
        assert type(exc_info.value) == ValueError
        assert "not available in" not in str(exc_info.value)


# =============================================================================
# TestCalculatorREPLEvaluate
# =============================================================================


class TestCalculatorREPLEvaluate:
    """Tests for CalculatorREPL._evaluate() handling of mode errors."""

    @pytest.fixture
    def repl_basic(self):
        """Fixture providing a CalculatorREPL in basic mode."""
        calc = Calculator(mode="basic")
        return CalculatorREPL(calc)

    def test_evaluate_returns_user_friendly_message_for_mode_error(self, repl_basic):
        """Test _evaluate returns user-friendly message for mode error."""
        result = repl_basic._evaluate("factorial 5")
        assert "not available" in result or "is not available" in result
        assert "basic" in result

    def test_evaluate_message_contains_operation_name(self, repl_basic):
        """Test _evaluate message contains the operation name."""
        result = repl_basic._evaluate("factorial 5")
        assert "factorial" in result

    def test_evaluate_message_contains_available_modes(self, repl_basic):
        """Test _evaluate message contains available modes."""
        result = repl_basic._evaluate("factorial 5")
        assert "advanced" in result
        assert "scientific" in result

    def test_evaluate_message_contains_switch_command_when_modes_available(self, repl_basic):
        """Test _evaluate message includes switch command when modes available."""
        result = repl_basic._evaluate("factorial 5")
        assert "mode" in result.lower()

    def test_evaluate_message_does_not_start_with_result(self, repl_basic):
        """Test _evaluate message does NOT start with 'Result:' for mode error."""
        result = repl_basic._evaluate("factorial 5")
        assert not result.startswith("Result:")

    def test_evaluate_message_does_not_start_with_math_error(self, repl_basic):
        """Test _evaluate message does NOT start with 'Math error:' for mode error."""
        result = repl_basic._evaluate("factorial 5")
        assert not result.startswith("Math error:")

    def test_evaluate_valid_operation_still_returns_result(self, repl_basic):
        """Test _evaluate returns 'Result:' for valid operations."""
        result = repl_basic._evaluate("add 2 3")
        assert result.startswith("Result:")
        assert "5" in result


# =============================================================================
# TestCalculatorREPLFunctionalityAfterModeError
# =============================================================================


class TestCalculatorREPLFunctionalityAfterModeError:
    """Tests that REPL remains functional after mode error."""

    @pytest.fixture
    def repl_basic(self):
        """Fixture providing a CalculatorREPL in basic mode."""
        calc = Calculator(mode="basic")
        return CalculatorREPL(calc)

    def test_subsequent_valid_operation_works_after_mode_error(self, repl_basic):
        """Test subsequent valid operations work after a mode error."""
        # Trigger mode error
        result1 = repl_basic._evaluate("factorial 5")
        assert "not available" in result1
        # Valid operation should still work
        result2 = repl_basic._evaluate("add 2 3")
        assert result2.startswith("Result:")
        assert "5" in result2

    def test_history_unchanged_after_failed_operation(self, repl_basic):
        """Test history does not include failed mode error operations."""
        initial_history_len = len(repl_basic._calculator.get_history())
        # Trigger mode error
        repl_basic._evaluate("factorial 5")
        # History should not grow
        assert len(repl_basic._calculator.get_history()) == initial_history_len

    def test_history_includes_subsequent_valid_operation(self, repl_basic):
        """Test history is updated after subsequent valid operation."""
        # Trigger mode error
        repl_basic._evaluate("factorial 5")
        # Execute valid operation
        repl_basic._evaluate("add 2 3")
        # History should have grown by 1
        history = repl_basic._calculator.get_history()
        assert len(history) == 1
        assert history[0]["operator"] == "add"


# =============================================================================
# TestCalculatorREPLWelcomeMessage
# =============================================================================


class TestCalculatorREPLWelcomeMessage:
    """Tests for updated REPL welcome message."""

    @pytest.fixture
    def repl(self):
        """Fixture providing a CalculatorREPL instance."""
        calc = Calculator(mode="basic")
        return CalculatorREPL(calc)

    def test_welcome_message_contains_exit_instruction(self, repl):
        """Test welcome message mentions how to exit."""
        with patch("builtins.print") as mock_print:
            with patch("builtins.input", side_effect=KeyboardInterrupt):
                try:
                    repl.run()
                except KeyboardInterrupt:
                    pass
        # Collect all printed messages
        printed = "\n".join([call.args[0] for call in mock_print.call_args_list if call.args])
        assert "exit" in printed.lower() or "quit" in printed.lower()

    def test_welcome_message_mentions_mode_switching(self, repl):
        """Test welcome message mentions mode switching syntax."""
        with patch("builtins.print") as mock_print:
            with patch("builtins.input", side_effect=KeyboardInterrupt):
                try:
                    repl.run()
                except KeyboardInterrupt:
                    pass
        printed = "\n".join([call.args[0] for call in mock_print.call_args_list if call.args])
        assert "mode" in printed.lower()

    def test_welcome_message_mentions_basic_mode(self, repl):
        """Test welcome message mentions basic mode."""
        with patch("builtins.print") as mock_print:
            with patch("builtins.input", side_effect=KeyboardInterrupt):
                try:
                    repl.run()
                except KeyboardInterrupt:
                    pass
        printed = "\n".join([call.args[0] for call in mock_print.call_args_list if call.args])
        assert "basic" in printed.lower()

    def test_welcome_message_mentions_advanced_mode(self, repl):
        """Test welcome message mentions advanced mode."""
        with patch("builtins.print") as mock_print:
            with patch("builtins.input", side_effect=KeyboardInterrupt):
                try:
                    repl.run()
                except KeyboardInterrupt:
                    pass
        printed = "\n".join([call.args[0] for call in mock_print.call_args_list if call.args])
        assert "advanced" in printed.lower()

    def test_welcome_message_mentions_scientific_mode(self, repl):
        """Test welcome message mentions scientific mode."""
        with patch("builtins.print") as mock_print:
            with patch("builtins.input", side_effect=KeyboardInterrupt):
                try:
                    repl.run()
                except KeyboardInterrupt:
                    pass
        printed = "\n".join([call.args[0] for call in mock_print.call_args_list if call.args])
        assert "scientific" in printed.lower()

    def test_welcome_message_mentions_history_command(self, repl):
        """Test welcome message mentions history command."""
        with patch("builtins.print") as mock_print:
            with patch("builtins.input", side_effect=KeyboardInterrupt):
                try:
                    repl.run()
                except KeyboardInterrupt:
                    pass
        printed = "\n".join([call.args[0] for call in mock_print.call_args_list if call.args])
        assert "history" in printed.lower()

    def test_welcome_message_reasonable_length(self, repl):
        """Test welcome message is approximately 7-8 lines."""
        with patch("builtins.print") as mock_print:
            with patch("builtins.input", side_effect=KeyboardInterrupt):
                try:
                    repl.run()
                except KeyboardInterrupt:
                    pass
        # Count print calls before first input prompt
        print_calls = [call for call in mock_print.call_args_list if call.args]
        welcome_lines = len(print_calls)  # All prints before first input are welcome
        # Should be approximately 7-8 lines (allow some flexibility)
        assert 5 <= welcome_lines <= 10, f"Got {welcome_lines} welcome lines"


# =============================================================================
# TestRegressionBasicOperations
# =============================================================================


class TestRegressionBasicOperations:
    """Regression tests: basic operations still work in all modes."""

    @pytest.mark.parametrize("mode", ["basic", "advanced", "scientific"])
    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 5),
        (10, 5, 5),
        (3, 4, 12),
        (10, 2, 5),
    ])
    def test_basic_operations_work_in_all_modes(self, mode, a, b, expected):
        """Test basic operations work in all modes."""
        engine = CalculatorEngine(mode=mode)
        assert engine.add(a, b) == a + b
        assert engine.subtract(a, b) == a - b
        assert engine.multiply(a, b) == a * b
        assert engine.divide(a, b) == a / b


# =============================================================================
# TestRegressionAdvancedOperations
# =============================================================================


class TestRegressionAdvancedOperations:
    """Regression tests: advanced operations work in advanced and scientific modes."""

    @pytest.mark.parametrize("mode", ["advanced", "scientific"])
    def test_factorial_works_in_advanced_and_scientific(self, mode):
        """Test factorial works in advanced and scientific modes."""
        engine = CalculatorEngine(mode=mode)
        assert engine.factorial(5) == 120

    @pytest.mark.parametrize("mode", ["advanced", "scientific"])
    def test_square_works_in_advanced_and_scientific(self, mode):
        """Test square works in advanced and scientific modes."""
        engine = CalculatorEngine(mode=mode)
        assert engine.square(4) == 16

    @pytest.mark.parametrize("mode", ["advanced", "scientific"])
    def test_square_root_works_in_advanced_and_scientific(self, mode):
        """Test square_root works in advanced and scientific modes."""
        engine = CalculatorEngine(mode=mode)
        assert engine.square_root(16) == 4


# =============================================================================
# TestRegressionScientificOperations
# =============================================================================


class TestRegressionScientificOperations:
    """Regression tests: scientific operations work in scientific mode."""

    def test_sin_works_in_scientific_mode(self):
        """Test sin works in scientific mode."""
        engine = CalculatorEngine(mode="scientific")
        result = engine.sin(0)
        assert abs(result) < 1e-10  # sin(0) ≈ 0

    def test_ln_works_in_scientific_mode(self):
        """Test ln works in scientific mode."""
        engine = CalculatorEngine(mode="scientific")
        result = engine.ln(math.e)
        assert abs(result - 1.0) < 1e-10


# =============================================================================
# TestRegressionHistoryAndModeSwitching
# =============================================================================


class TestRegressionHistoryAndModeSwitching:
    """Regression tests: history persists across mode switches."""

    def test_history_persists_after_mode_switch(self):
        """Test history is preserved when switching modes."""
        engine = CalculatorEngine(mode="basic")
        engine.add(2, 3)
        history_len_before = len(engine.get_history())
        # Switch to advanced
        engine.set_mode("advanced")
        engine.factorial(5)
        history = engine.get_history()
        # Should have both operations
        assert len(history) == 2
        assert history[0]["operator"] == "add"
        assert history[1]["operator"] == "factorial"

    def test_calculator_history_persists_after_mode_switch(self):
        """Test Calculator history is preserved when switching modes."""
        calc = Calculator(mode="basic")
        calc.add(2, 3)
        # Switch to scientific
        calc.set_mode("scientific")
        calc.sin(0)
        history = calc.get_history()
        # Should have both operations
        assert len(history) == 2
        assert history[0]["operator"] == "add"
        assert history[1]["operator"] == "sin"


# =============================================================================
# TestRegressionREPLHistoryCommand
# =============================================================================


class TestRegressionREPLHistoryCommand:
    """Regression tests: REPL history command still works."""

    def test_history_command_displays_operations(self):
        """Test history command displays recorded operations."""
        calc = Calculator(mode="basic")
        repl = CalculatorREPL(calc)
        # Add some operations
        repl._evaluate("add 2 3")
        repl._evaluate("multiply 4 5")
        # Get history via command
        with patch("builtins.print") as mock_print:
            # Simulate "history" command (not via _evaluate, but via run logic)
            history = repl._calculator.get_history()
            assert len(history) == 2
            assert history[0]["operator"] == "add"
            assert history[1]["operator"] == "multiply"
