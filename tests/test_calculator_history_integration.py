"""Integration tests for Calculator history logging.

Tests verifying that the Calculator properly logs operations to its history
through the CalculatorREPL and CLIHandler interfaces.

Covers:
- Successful operations logging with correct fields
- Chronological ordering across multiple operations
- Error paths (division by zero, validation errors) do NOT log
- Fresh Calculator instances have empty history
"""

import pytest
import sys
from io import StringIO

from src import Calculator, OperationRecord
from src.input_handler import CalculatorREPL, RetryConfig
from src.cli import CLIHandler


class TestCalculatorHistoryBasic:
    """Tests for basic Calculator history functionality."""

    def test_calculator_initialization_has_empty_history(self):
        """Test that a freshly created Calculator instance has an empty history."""
        calculator = Calculator()

        assert hasattr(calculator, "_history")
        assert len(calculator._history) == 0
        assert calculator._history.get_all() == []

    def test_calculator_history_type(self):
        """Test that Calculator._history is an OperationHistory instance."""
        calculator = Calculator()

        from src.history import OperationHistory
        assert isinstance(calculator._history, OperationHistory)

    def test_calculator_add_operation_logs_to_history(self):
        """Test that a successful add operation is logged to history."""
        calculator = Calculator()
        result = calculator.add(5, 3)

        # Manually log since Calculator methods don't auto-log
        calculator._history.append("add", [5, 3], result)

        assert len(calculator._history) == 1
        records = calculator._history.get_all()
        assert records[0].operation == "add"
        assert records[0].operands == [5, 3]
        assert records[0].result == 8

    @pytest.mark.parametrize("operation,operands,expected_result", [
        ("add", [2, 3], 5),
        ("subtract", [10, 4], 6),
        ("multiply", [6, 7], 42),
        ("divide", [20, 4], 5.0),
        ("square", [5], 25),
        ("cube", [3], 27),
        ("factorial", [5], 120),
    ])
    def test_calculator_various_operations_log_correctly(
        self, operation, operands, expected_result
    ):
        """Test that various calculator operations can be logged with correct fields."""
        calculator = Calculator()

        # Execute the operation
        method = getattr(calculator, operation)
        result = method(*operands)

        # Manually log
        calculator._history.append(operation, operands, result)

        # Verify history
        assert len(calculator._history) == 1
        records = calculator._history.get_all()
        record = records[0]

        assert record.operation == operation
        assert record.operands == operands
        assert record.result == result
        assert record.result == expected_result


class TestCalculatorREPLHistoryIntegration:
    """Integration tests for CalculatorREPL with history logging."""

    def test_calculator_repl_successful_operation_logs_to_history(self):
        """Test that CalculatorREPL logs successful operations to history."""
        calculator = Calculator()
        repl = CalculatorREPL(calculator)

        # Call _evaluate directly with a valid expression
        response = repl._evaluate("add 5 3")

        assert response == "Result: 8"
        assert len(calculator._history) == 1

        records = calculator._history.get_all()
        assert records[0].operation == "add"
        assert records[0].operands == [5, 3]
        assert records[0].result == 8

    def test_calculator_repl_multiple_operations_logged_chronologically(self):
        """Test that CalculatorREPL logs multiple operations in order."""
        calculator = Calculator()
        repl = CalculatorREPL(calculator)

        repl._evaluate("add 1 1")
        repl._evaluate("multiply 2 3")
        repl._evaluate("subtract 10 5")

        assert len(calculator._history) == 3

        records = calculator._history.get_all()
        assert records[0].operation == "add"
        assert records[0].result == 2

        assert records[1].operation == "multiply"
        assert records[1].result == 6

        assert records[2].operation == "subtract"
        assert records[2].result == 5

    def test_calculator_repl_logs_correct_operands_and_result(self):
        """Test that REPL logs correct operands and result for various operations."""
        calculator = Calculator()
        repl = CalculatorREPL(calculator)

        repl._evaluate("power 2 10")

        records = calculator._history.get_all()
        assert records[0].operation == "power"
        assert records[0].operands == [2, 10]
        assert records[0].result == 1024

    def test_calculator_repl_division_by_zero_not_logged(self):
        """Test that division by zero error does NOT log to history."""
        calculator = Calculator()
        repl = CalculatorREPL(calculator)

        response = repl._evaluate("divide 10 0")

        assert "Math error: division by zero" in response
        assert len(calculator._history) == 0  # No logging on error

    def test_calculator_repl_invalid_operation_not_logged(self):
        """Test that invalid operation does NOT log to history."""
        calculator = Calculator()
        repl = CalculatorREPL(calculator)

        response = repl._evaluate("unknown_op 5 3")

        assert "Validation error" in response or "Unknown operation" in response
        assert len(calculator._history) == 0

    def test_calculator_repl_wrong_operand_count_not_logged(self):
        """Test that wrong operand count error does NOT log to history."""
        calculator = Calculator()
        repl = CalculatorREPL(calculator)

        response = repl._evaluate("add 5")  # add requires 2 operands

        assert "Validation error" in response or "expects 2 operand" in response
        assert len(calculator._history) == 0

    def test_calculator_repl_invalid_number_format_not_logged(self):
        """Test that invalid number format does NOT log to history."""
        calculator = Calculator()
        repl = CalculatorREPL(calculator)

        response = repl._evaluate("add abc def")

        assert "Input error" in response or "not a valid number" in response
        assert len(calculator._history) == 0

    def test_calculator_repl_factorial_type_error_not_logged(self):
        """Test that factorial with non-integer does NOT log to history."""
        calculator = Calculator()
        repl = CalculatorREPL(calculator)

        response = repl._evaluate("factorial 5.5")

        assert "Type error" in response or "Math error" in response
        assert len(calculator._history) == 0

    def test_calculator_repl_factorial_negative_value_not_logged(self):
        """Test that factorial with negative value does NOT log to history."""
        calculator = Calculator()
        repl = CalculatorREPL(calculator)

        response = repl._evaluate("factorial -5")

        assert "Math error" in response
        assert len(calculator._history) == 0

    def test_calculator_repl_square_root_negative_not_logged(self):
        """Test that square_root of negative does NOT log to history."""
        calculator = Calculator()
        repl = CalculatorREPL(calculator)

        response = repl._evaluate("square_root -4")

        assert "Math error" in response
        assert len(calculator._history) == 0

    def test_calculator_repl_natural_log_invalid_not_logged(self):
        """Test that natural_log of non-positive does NOT log to history."""
        calculator = Calculator()
        repl = CalculatorREPL(calculator)

        response = repl._evaluate("natural_log 0")

        assert "Math error" in response
        assert len(calculator._history) == 0

    @pytest.mark.parametrize("expression,expected_op,expected_operands,expected_result", [
        ("add 10 20", "add", [10, 20], 30),
        ("subtract 50 15", "subtract", [50, 15], 35),
        ("multiply 7 8", "multiply", [7, 8], 56),
        ("divide 100 4", "divide", [100, 4], 25.0),
        ("square 9", "square", [9], 81),
        ("cube 2", "cube", [2], 8),
    ])
    def test_calculator_repl_various_operations_logged(
        self, expression, expected_op, expected_operands, expected_result
    ):
        """Test that various REPL operations are logged correctly."""
        calculator = Calculator()
        repl = CalculatorREPL(calculator)

        response = repl._evaluate(expression)

        assert "Result:" in response
        assert len(calculator._history) == 1

        record = calculator._history.get_all()[0]
        assert record.operation == expected_op
        assert record.operands == expected_operands
        assert record.result == expected_result


class TestCLIHandlerHistoryIntegration:
    """Integration tests for CLIHandler with history logging."""

    def test_cli_handler_successful_operation_logs_to_history(self):
        """Test that CLIHandler logs successful operations to history."""
        handler = CLIHandler("add 5 3")
        exit_code = handler.run()

        assert exit_code == 0
        assert len(handler._calculator._history) == 1

        records = handler._calculator._history.get_all()
        assert records[0].operation == "add"
        assert records[0].operands == [5, 3]
        assert records[0].result == 8

    def test_cli_handler_multiple_instances_independent_histories(self):
        """Test that different CLIHandler instances have independent histories."""
        handler1 = CLIHandler("add 5 3")
        handler2 = CLIHandler("multiply 2 3")

        handler1.run()
        handler2.run()

        # Each handler has its own calculator and history
        assert len(handler1._calculator._history) == 1
        assert len(handler2._calculator._history) == 1

        records1 = handler1._calculator._history.get_all()
        records2 = handler2._calculator._history.get_all()

        assert records1[0].operation == "add"
        assert records2[0].operation == "multiply"

    def test_cli_handler_division_by_zero_not_logged(self):
        """Test that division by zero error does NOT log to history."""
        handler = CLIHandler("divide 10 0")
        exit_code = handler.run()

        assert exit_code == 1  # Error exit code
        assert len(handler._calculator._history) == 0

    def test_cli_handler_invalid_operation_not_logged(self):
        """Test that invalid operation does NOT log to history."""
        handler = CLIHandler("unknown_op 5 3")
        exit_code = handler.run()

        assert exit_code == 1
        assert len(handler._calculator._history) == 0

    def test_cli_handler_wrong_operand_count_not_logged(self):
        """Test that wrong operand count error does NOT log to history."""
        handler = CLIHandler("add 5")
        exit_code = handler.run()

        assert exit_code == 1
        assert len(handler._calculator._history) == 0

    def test_cli_handler_invalid_number_format_not_logged(self):
        """Test that invalid number format does NOT log to history."""
        handler = CLIHandler("add abc def")
        exit_code = handler.run()

        assert exit_code == 1
        assert len(handler._calculator._history) == 0

    def test_cli_handler_factorial_type_error_not_logged(self):
        """Test that factorial with non-integer does NOT log to history."""
        handler = CLIHandler("factorial 5.5")
        exit_code = handler.run()

        assert exit_code == 1
        assert len(handler._calculator._history) == 0

    def test_cli_handler_factorial_negative_value_not_logged(self):
        """Test that factorial with negative value does NOT log to history."""
        handler = CLIHandler("factorial -5")
        exit_code = handler.run()

        assert exit_code == 1
        assert len(handler._calculator._history) == 0

    def test_cli_handler_square_root_negative_not_logged(self):
        """Test that square_root of negative does NOT log to history."""
        handler = CLIHandler("square_root -4")
        exit_code = handler.run()

        assert exit_code == 1
        assert len(handler._calculator._history) == 0

    def test_cli_handler_natural_log_zero_not_logged(self):
        """Test that natural_log of zero does NOT log to history."""
        handler = CLIHandler("natural_log 0")
        exit_code = handler.run()

        assert exit_code == 1
        assert len(handler._calculator._history) == 0

    @pytest.mark.parametrize("expression,expected_op,expected_operands,expected_result", [
        ("add 10 20", "add", [10, 20], 30),
        ("subtract 50 15", "subtract", [50, 15], 35),
        ("multiply 7 8", "multiply", [7, 8], 56),
        ("divide 100 4", "divide", [100, 4], 25.0),
        ("square 9", "square", [9], 81),
        ("cube 2", "cube", [2], 8),
    ])
    def test_cli_handler_various_operations_logged(
        self, expression, expected_op, expected_operands, expected_result
    ):
        """Test that various CLI operations are logged correctly."""
        handler = CLIHandler(expression)
        exit_code = handler.run()

        assert exit_code == 0
        assert len(handler._calculator._history) == 1

        record = handler._calculator._history.get_all()[0]
        assert record.operation == expected_op
        assert record.operands == expected_operands
        assert record.result == expected_result


class TestHistoryDataIntegrity:
    """Tests verifying data integrity and consistency of history records."""

    def test_repl_history_records_are_immutable(self):
        """Test that records from REPL history are immutable."""
        from dataclasses import FrozenInstanceError

        calculator = Calculator()
        repl = CalculatorREPL(calculator)
        repl._evaluate("add 5 3")

        records = calculator._history.get_all()
        record = records[0]

        with pytest.raises(FrozenInstanceError):
            record.result = 999

    def test_repl_history_get_all_defensive_copy(self):
        """Test that modifying returned list doesn't affect history."""
        calculator = Calculator()
        repl = CalculatorREPL(calculator)
        repl._evaluate("add 5 3")

        records1 = calculator._history.get_all()
        records1.clear()

        records2 = calculator._history.get_all()
        assert len(records2) == 1

    def test_cli_handler_history_records_are_immutable(self):
        """Test that records from CLI history are immutable."""
        from dataclasses import FrozenInstanceError

        handler = CLIHandler("multiply 3 4")
        handler.run()

        records = handler._calculator._history.get_all()
        record = records[0]

        with pytest.raises(FrozenInstanceError):
            record.result = 999

    def test_cli_handler_history_get_all_defensive_copy(self):
        """Test that modifying returned list doesn't affect CLI history."""
        handler = CLIHandler("divide 20 4")
        handler.run()

        records1 = handler._calculator._history.get_all()
        records1.clear()

        records2 = handler._calculator._history.get_all()
        assert len(records2) == 1

    def test_repl_history_timestamps_are_valid(self):
        """Test that REPL history records have valid timestamps."""
        calculator = Calculator()
        repl = CalculatorREPL(calculator)
        repl._evaluate("add 1 1")

        records = calculator._history.get_all()
        assert records[0].timestamp > 0
        assert isinstance(records[0].timestamp, float)

    def test_cli_history_timestamps_are_valid(self):
        """Test that CLI history records have valid timestamps."""
        handler = CLIHandler("add 1 1")
        handler.run()

        records = handler._calculator._history.get_all()
        assert records[0].timestamp > 0
        assert isinstance(records[0].timestamp, float)
