"""Test suite for the CalculatorSession class."""

import pytest
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import os

from src.session import CalculatorSession
from src.core.calculator import Calculator


class TestSelectOperation:
    """Test suite for CalculatorSession.select_operation() method."""

    @pytest.fixture
    def session(self):
        """Fixture providing a CalculatorSession instance."""
        calculator = Calculator()
        return CalculatorSession(calculator)

    def test_select_operation_valid_operation_name(self, session):
        """Should resolve valid operation name."""
        op_name, exit_code = session.select_operation("add", "interactive")
        assert op_name == "add"
        assert exit_code == 0

    @pytest.mark.parametrize("op_name", [
        "add", "subtract", "multiply", "divide", "square", "cube",
        "square_root", "cube_root", "factorial", "logarithm",
        "natural_logarithm", "power"
    ])
    def test_select_operation_all_valid_operations(self, session, op_name):
        """Should resolve all valid operation names."""
        result_op, exit_code = session.select_operation(op_name, "interactive")
        assert result_op == op_name
        assert exit_code == 0

    def test_select_operation_case_insensitive_lowercase(self, session):
        """Should resolve operation names case-insensitively (lowercase)."""
        op_name, exit_code = session.select_operation("ADD", "interactive")
        assert op_name == "add"
        assert exit_code == 0

    def test_select_operation_case_insensitive_mixed(self, session):
        """Should resolve operation names case-insensitively (mixed case)."""
        op_name, exit_code = session.select_operation("SqUaRe", "interactive")
        assert op_name == "square"
        assert exit_code == 0

    def test_select_operation_numeric_index_valid_1(self, session):
        """Should resolve numeric index 1 to first operation."""
        op_name, exit_code = session.select_operation("1", "interactive")
        assert op_name is not None
        assert exit_code == 0

    def test_select_operation_numeric_index_valid_2(self, session):
        """Should resolve numeric index 2 to second operation."""
        op_name, exit_code = session.select_operation("2", "interactive")
        assert op_name is not None
        assert exit_code == 0

    def test_select_operation_numeric_index_out_of_range_high(self, session):
        """Should return (None, 2) for numeric index too high."""
        op_name, exit_code = session.select_operation("999", "interactive")
        assert op_name is None
        assert exit_code == 2

    def test_select_operation_numeric_index_out_of_range_zero(self, session):
        """Should return (None, 2) for numeric index 0."""
        op_name, exit_code = session.select_operation("0", "interactive")
        assert op_name is None
        assert exit_code == 2

    def test_select_operation_numeric_index_negative(self, session):
        """Should return (None, 2) for negative numeric index."""
        op_name, exit_code = session.select_operation("-1", "interactive")
        assert op_name is None
        assert exit_code == 2

    def test_select_operation_unknown_name(self, session):
        """Should return (None, 1) for unknown operation name."""
        op_name, exit_code = session.select_operation("unknown_op", "interactive")
        assert op_name is None
        assert exit_code == 1

    def test_select_operation_invalid_name_logs_error(self, session):
        """Should log unsupported operation when name not recognized."""
        # This should log the error but not raise
        op_name, exit_code = session.select_operation("nonexistent", "interactive")
        assert exit_code == 1

    def test_select_operation_mode_cli(self, session):
        """Should work with 'cli' mode."""
        op_name, exit_code = session.select_operation("add", "cli")
        assert op_name == "add"
        assert exit_code == 0

    def test_select_operation_returns_tuple(self, session):
        """Should return a tuple of (op_name, exit_code)."""
        result = session.select_operation("add", "interactive")
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_select_operation_refreshes_operation_list(self, session):
        """Should refresh operation list on each call."""
        # This verifies the internal _get_operation_list() is called
        op_name1, _ = session.select_operation("add", "interactive")
        op_name2, _ = session.select_operation("add", "interactive")
        assert op_name1 == op_name2


class TestCollectOperands:
    """Test suite for CalculatorSession.collect_operands() method."""

    @pytest.fixture
    def session(self):
        """Fixture providing a CalculatorSession instance."""
        calculator = Calculator()
        return CalculatorSession(calculator)

    @patch("builtins.input")
    def test_collect_operands_binary_operation_valid(self, mock_input, session):
        """Should collect two operands for binary operation."""
        mock_input.side_effect = ["3.0", "4.0"]
        operands, exit_code = session.collect_operands(2, "interactive")
        assert operands == [3.0, 4.0]
        assert exit_code == 0

    @patch("builtins.input")
    def test_collect_operands_unary_operation_valid(self, mock_input, session):
        """Should collect one operand for unary operation."""
        mock_input.return_value = "5.0"
        operands, exit_code = session.collect_operands(1, "interactive")
        assert operands == [5.0]
        assert exit_code == 0

    @patch("builtins.input")
    def test_collect_operands_negative_numbers(self, mock_input, session):
        """Should accept negative operands."""
        mock_input.side_effect = ["-3.0", "-4.0"]
        operands, exit_code = session.collect_operands(2, "interactive")
        assert operands == [-3.0, -4.0]
        assert exit_code == 0

    @patch("builtins.input")
    def test_collect_operands_integer_input(self, mock_input, session):
        """Should accept integer input and convert to float."""
        mock_input.side_effect = ["5", "10"]
        operands, exit_code = session.collect_operands(2, "interactive")
        assert operands == [5.0, 10.0]
        assert exit_code == 0

    @patch("builtins.input")
    def test_collect_operands_scientific_notation(self, mock_input, session):
        """Should accept scientific notation."""
        mock_input.side_effect = ["1e3", "2.5e-2"]
        operands, exit_code = session.collect_operands(2, "interactive")
        assert operands == [1000.0, 0.025]
        assert exit_code == 0

    @patch("builtins.input")
    def test_collect_operands_invalid_input_in_interactive_mode(self, mock_input, session):
        """Should retry on invalid input in interactive mode."""
        mock_input.side_effect = ["invalid", "5.0"]
        operands, exit_code = session.collect_operands(1, "interactive")
        assert operands == [5.0]
        assert exit_code == 0

    @patch("builtins.input")
    def test_collect_operands_retry_limit_exceeded(self, mock_input, session):
        """Should return (None, 1) when retry limit exceeded."""
        # 5 invalid inputs should exceed the default retry limit
        mock_input.side_effect = ["a", "b", "c", "d", "e"]
        operands, exit_code = session.collect_operands(1, "interactive")
        assert operands is None
        assert exit_code == 1

    @patch("builtins.input")
    def test_collect_operands_system_exit_in_cli_mode(self, mock_input, session):
        """Should raise SystemExit on invalid input in cli mode."""
        mock_input.return_value = "invalid"
        with pytest.raises(SystemExit):
            session.collect_operands(1, "cli")

    @patch("builtins.input")
    def test_collect_operands_zero(self, mock_input, session):
        """Should accept zero as a valid operand."""
        mock_input.return_value = "0"
        operands, exit_code = session.collect_operands(1, "interactive")
        assert operands == [0.0]
        assert exit_code == 0

    @patch("builtins.input")
    def test_collect_operands_large_numbers(self, mock_input, session):
        """Should accept very large numbers."""
        mock_input.side_effect = ["1e100", "1e50"]
        operands, exit_code = session.collect_operands(2, "interactive")
        assert operands[0] == 1e100
        assert operands[1] == 1e50
        assert exit_code == 0

    @patch("builtins.input")
    def test_collect_operands_small_numbers(self, mock_input, session):
        """Should accept very small numbers."""
        mock_input.side_effect = ["1e-100", "1e-50"]
        operands, exit_code = session.collect_operands(2, "interactive")
        assert operands[0] == 1e-100
        assert operands[1] == 1e-50
        assert exit_code == 0

    @patch("builtins.input")
    def test_collect_operands_returns_tuple(self, mock_input, session):
        """Should return a tuple of (operands, exit_code)."""
        mock_input.return_value = "5.0"
        result = session.collect_operands(1, "interactive")
        assert isinstance(result, tuple)
        assert len(result) == 2

    @patch("builtins.input")
    def test_collect_operands_three_operands(self, mock_input, session):
        """Should collect three operands when arity=3."""
        mock_input.side_effect = ["1.0", "2.0", "3.0"]
        operands, exit_code = session.collect_operands(3, "interactive")
        assert operands == [1.0, 2.0, 3.0]
        assert exit_code == 0


class TestExecuteOperation:
    """Test suite for CalculatorSession.execute_operation() method."""

    @pytest.fixture
    def session(self):
        """Fixture providing a CalculatorSession instance."""
        calculator = Calculator()
        return CalculatorSession(calculator)

    def test_execute_operation_add_success(self, session):
        """Should execute add operation successfully."""
        result, error = session.execute_operation("add", [2.0, 3.0])
        assert result == 5.0
        assert error is None

    def test_execute_operation_subtract_success(self, session):
        """Should execute subtract operation successfully."""
        result, error = session.execute_operation("subtract", [5.0, 3.0])
        assert result == 2.0
        assert error is None

    def test_execute_operation_multiply_success(self, session):
        """Should execute multiply operation successfully."""
        result, error = session.execute_operation("multiply", [4.0, 5.0])
        assert result == 20.0
        assert error is None

    def test_execute_operation_divide_success(self, session):
        """Should execute divide operation successfully."""
        result, error = session.execute_operation("divide", [10.0, 2.0])
        assert result == 5.0
        assert error is None

    def test_execute_operation_square_success(self, session):
        """Should execute square operation successfully."""
        result, error = session.execute_operation("square", [3.0])
        assert result == 9.0
        assert error is None

    def test_execute_operation_divide_by_zero(self, session):
        """Should catch ZeroDivisionError and return error message."""
        result, error = session.execute_operation("divide", [10.0, 0.0])
        assert result is None
        assert error is not None
        assert "division" in error.lower() or "zero" in error.lower()

    def test_execute_operation_square_root_negative(self, session):
        """Should catch ValueError for square root of negative."""
        result, error = session.execute_operation("square_root", [-1.0])
        assert result is None
        assert error is not None

    def test_execute_operation_logarithm_zero(self, session):
        """Should catch ValueError for logarithm of zero."""
        result, error = session.execute_operation("logarithm", [0.0])
        assert result is None
        assert error is not None

    def test_execute_operation_logarithm_negative(self, session):
        """Should catch ValueError for logarithm of negative."""
        result, error = session.execute_operation("logarithm", [-1.0])
        assert result is None
        assert error is not None

    def test_execute_operation_natural_logarithm_zero(self, session):
        """Should catch ValueError for natural logarithm of zero."""
        result, error = session.execute_operation("natural_logarithm", [0.0])
        assert result is None
        assert error is not None

    def test_execute_operation_factorial_with_float(self, session):
        """Should catch TypeError when factorial receives float."""
        result, error = session.execute_operation("factorial", [5.0])
        assert result is None
        assert error is not None

    def test_execute_operation_power_success(self, session):
        """Should execute power operation successfully."""
        result, error = session.execute_operation("power", [2.0, 3.0])
        assert result == 8.0
        assert error is None

    def test_execute_operation_cube_success(self, session):
        """Should execute cube operation successfully."""
        result, error = session.execute_operation("cube", [2.0])
        assert result == 8.0
        assert error is None

    def test_execute_operation_negative_operands(self, session):
        """Should handle negative operands correctly."""
        result, error = session.execute_operation("add", [-5.0, -3.0])
        assert result == -8.0
        assert error is None

    def test_execute_operation_returns_tuple(self, session):
        """Should return a tuple of (result, error)."""
        result = session.execute_operation("add", [2.0, 3.0])
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_execute_operation_zero_result(self, session):
        """Should handle zero result correctly."""
        result, error = session.execute_operation("subtract", [5.0, 5.0])
        assert result == 0.0
        assert error is None


class TestGetArity:
    """Test suite for CalculatorSession.get_arity() method."""

    @pytest.fixture
    def session(self):
        """Fixture providing a CalculatorSession instance."""
        calculator = Calculator()
        return CalculatorSession(calculator)

    @pytest.mark.parametrize("op_name,expected_arity", [
        ("square", 1),
        ("cube", 1),
        ("square_root", 1),
        ("cube_root", 1),
        ("factorial", 1),
        ("logarithm", 1),
        ("natural_logarithm", 1),
    ])
    def test_get_arity_unary_operations(self, session, op_name, expected_arity):
        """Should return arity 1 for unary operations."""
        arity = session.get_arity(op_name)
        assert arity == expected_arity

    @pytest.mark.parametrize("op_name,expected_arity", [
        ("add", 2),
        ("subtract", 2),
        ("multiply", 2),
        ("divide", 2),
        ("power", 2),
    ])
    def test_get_arity_binary_operations(self, session, op_name, expected_arity):
        """Should return arity 2 for binary operations."""
        arity = session.get_arity(op_name)
        assert arity == expected_arity

    def test_get_arity_returns_int(self, session):
        """Should return an integer."""
        arity = session.get_arity("add")
        assert isinstance(arity, int)


class TestRecordAndGetHistory:
    """Test suite for record_history() and get_history() methods."""

    @pytest.fixture
    def session(self):
        """Fixture providing a CalculatorSession instance."""
        calculator = Calculator()
        return CalculatorSession(calculator)

    def test_record_history_single_operation(self, session):
        """Should record a single operation in history."""
        session.record_history("add", [2.0, 3.0], 5.0)
        history = session.get_history()
        assert len(history) == 1
        assert "add(2, 3) = 5" in history[0]

    def test_record_history_multiple_operations(self, session):
        """Should record multiple operations in history."""
        session.record_history("add", [2.0, 3.0], 5.0)
        session.record_history("subtract", [5.0, 3.0], 2.0)
        session.record_history("multiply", [4.0, 5.0], 20.0)
        history = session.get_history()
        assert len(history) == 3

    def test_record_history_preserves_order(self, session):
        """Should preserve insertion order of history."""
        session.record_history("add", [1.0, 1.0], 2.0)
        session.record_history("multiply", [2.0, 2.0], 4.0)
        history = session.get_history()
        assert "add(1, 1)" in history[0]
        assert "multiply(2, 2)" in history[1]

    def test_get_history_empty(self, session):
        """Should return empty list when no operations recorded."""
        history = session.get_history()
        assert history == []

    def test_get_history_returns_list(self, session):
        """Should return a list."""
        session.record_history("add", [2.0, 3.0], 5.0)
        history = session.get_history()
        assert isinstance(history, list)

    def test_get_history_returns_strings(self, session):
        """Should return list of strings."""
        session.record_history("add", [2.0, 3.0], 5.0)
        history = session.get_history()
        assert all(isinstance(entry, str) for entry in history)

    def test_record_history_with_float_result(self, session):
        """Should record operation with float result."""
        session.record_history("divide", [7.0, 2.0], 3.5)
        history = session.get_history()
        assert "3.5" in history[0]

    def test_record_history_with_negative_result(self, session):
        """Should record operation with negative result."""
        session.record_history("subtract", [2.0, 5.0], -3.0)
        history = session.get_history()
        assert "-3" in history[0]


class TestSaveHistory:
    """Test suite for save_history() method."""

    @pytest.fixture
    def session(self):
        """Fixture providing a CalculatorSession instance."""
        calculator = Calculator()
        return CalculatorSession(calculator)

    def test_save_history_to_file(self, session):
        """Should save history to a file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_history.txt")
            session.record_history("add", [2.0, 3.0], 5.0)
            session.save_history(filepath)
            assert os.path.exists(filepath)

    def test_save_history_file_content(self, session):
        """Should write correct content to history file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_history.txt")
            session.record_history("add", [2.0, 3.0], 5.0)
            session.save_history(filepath)
            with open(filepath, "r") as f:
                content = f.read()
            assert "add(2, 3) = 5" in content

    def test_save_history_multiple_entries(self, session):
        """Should save multiple history entries to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_history.txt")
            session.record_history("add", [2.0, 3.0], 5.0)
            session.record_history("multiply", [4.0, 5.0], 20.0)
            session.save_history(filepath)
            with open(filepath, "r") as f:
                lines = f.readlines()
            assert len(lines) == 2
            assert "add(2, 3) = 5" in lines[0]
            assert "multiply(4, 5) = 20" in lines[1]

    def test_save_history_empty_history(self, session):
        """Should handle saving empty history."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_history.txt")
            session.save_history(filepath)
            assert os.path.exists(filepath)
            with open(filepath, "r") as f:
                content = f.read()
            assert content == ""

    def test_save_history_overwrites_existing_file(self, session):
        """Should overwrite existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_history.txt")
            # Write initial content
            with open(filepath, "w") as f:
                f.write("old content\n")
            # Save new history
            session.record_history("add", [2.0, 3.0], 5.0)
            session.save_history(filepath)
            with open(filepath, "r") as f:
                content = f.read()
            assert "old content" not in content
            assert "add(2, 3) = 5" in content


class TestGetOperationList:
    """Test suite for get_operation_list() method."""

    @pytest.fixture
    def session(self):
        """Fixture providing a CalculatorSession instance."""
        calculator = Calculator()
        return CalculatorSession(calculator)

    def test_get_operation_list_returns_list(self, session):
        """Should return a list."""
        ops = session.get_operation_list()
        assert isinstance(ops, list)

    def test_get_operation_list_not_empty(self, session):
        """Should return non-empty list of operations."""
        ops = session.get_operation_list()
        assert len(ops) > 0

    def test_get_operation_list_contains_standard_operations(self, session):
        """Should contain standard calculator operations."""
        ops = session.get_operation_list()
        expected_ops = {"add", "subtract", "multiply", "divide"}
        assert expected_ops.issubset(set(ops))

    def test_get_operation_list_all_strings(self, session):
        """Should return list of strings."""
        ops = session.get_operation_list()
        assert all(isinstance(op, str) for op in ops)

    def test_get_operation_list_no_dunder_names(self, session):
        """Should not include dunder names."""
        ops = session.get_operation_list()
        assert not any(name.startswith("_") for name in ops)

    def test_get_operation_list_all_callable(self, session):
        """All operations should be callable."""
        ops = session.get_operation_list()
        for op in ops:
            method = getattr(session._calculator, op)
            assert callable(method)


class TestMaxRetriesProperty:
    """Test suite for max_retries property."""

    @pytest.fixture
    def session(self):
        """Fixture providing a CalculatorSession instance."""
        calculator = Calculator()
        return CalculatorSession(calculator)

    def test_max_retries_is_positive_integer(self, session):
        """max_retries should be a positive integer."""
        assert isinstance(session.max_retries, int)
        assert session.max_retries > 0

    def test_max_retries_default_value(self, session):
        """max_retries should have a default value of 5."""
        assert session.max_retries == 5
