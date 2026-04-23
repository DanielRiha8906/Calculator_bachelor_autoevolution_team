"""Tests for src.gui.session_adapter module.

Tests the GUISessionAdapter class that bridges CalculatorSession and GUI code.
"""

import pytest
from src.gui.session_adapter import GUISessionAdapter
from src.session import CalculatorSession
from src.core.calculator import Calculator
from src.mode import NORMAL_MODE_OPERATIONS, SCIENTIFIC_MODE_OPERATIONS


@pytest.fixture
def calculator():
    """Fixture providing a Calculator instance."""
    return Calculator()


@pytest.fixture
def session(calculator):
    """Fixture providing a CalculatorSession instance."""
    return CalculatorSession(calculator)


@pytest.fixture
def adapter(session):
    """Fixture providing a GUISessionAdapter instance."""
    return GUISessionAdapter(session)


class TestGUISessionAdapterInitialization:
    """Test suite for GUISessionAdapter initialization."""

    def test_adapter_initialization(self, adapter, session):
        """Test GUISessionAdapter is correctly initialized with a session."""
        assert adapter is not None
        assert isinstance(adapter, GUISessionAdapter)

    def test_adapter_stores_session_reference(self, adapter, session):
        """Test adapter stores the session reference internally."""
        # The session is stored as _session attribute
        assert hasattr(adapter, "_session")


class TestExecuteOperationSafe:
    """Test suite for GUISessionAdapter.execute_operation_safe."""

    def test_execute_operation_safe_add_returns_result_and_empty_error(self, adapter, session):
        """Test execute_operation_safe with 'add' returns result and empty error."""
        session.set_mode("normal")
        result_str, error_msg = adapter.execute_operation_safe("add", [3.0, 4.0])
        assert result_str == "7.0"
        assert error_msg == ""

    def test_execute_operation_safe_subtract(self, adapter, session):
        """Test execute_operation_safe with 'subtract'."""
        session.set_mode("normal")
        result_str, error_msg = adapter.execute_operation_safe("subtract", [10.0, 3.0])
        assert result_str == "7.0"
        assert error_msg == ""

    def test_execute_operation_safe_multiply(self, adapter, session):
        """Test execute_operation_safe with 'multiply'."""
        session.set_mode("normal")
        result_str, error_msg = adapter.execute_operation_safe("multiply", [5.0, 6.0])
        assert result_str == "30.0"
        assert error_msg == ""

    @pytest.mark.parametrize(
        "op_name,operands,expected_result",
        [
            ("square", [5.0], "25.0"),
            ("square_root", [4.0], "2.0"),
            ("cube", [2.0], "8.0"),
        ],
    )
    def test_execute_operation_safe_unary_operations(self, adapter, session, op_name, operands, expected_result):
        """Test execute_operation_safe with various unary operations."""
        session.set_mode("scientific")
        result_str, error_msg = adapter.execute_operation_safe(op_name, operands)
        assert result_str == expected_result
        assert error_msg == ""

    def test_execute_operation_safe_division_by_zero_returns_error(self, adapter, session):
        """Test execute_operation_safe with division by zero returns error."""
        session.set_mode("normal")
        result_str, error_msg = adapter.execute_operation_safe("divide", [1.0, 0.0])
        assert result_str == ""
        assert error_msg != ""
        assert "division" in error_msg.lower() or "zero" in error_msg.lower()

    def test_execute_operation_safe_error_does_not_record_history(self, adapter, session):
        """Test execute_operation_safe does not record history on error."""
        session.set_mode("normal")
        initial_history = adapter.get_history()
        # Attempt division by zero
        adapter.execute_operation_safe("divide", [1.0, 0.0])
        final_history = adapter.get_history()
        # History should not have been updated
        assert len(final_history) == len(initial_history)

    def test_execute_operation_safe_success_records_history(self, adapter, session):
        """Test execute_operation_safe records history on success."""
        session.set_mode("normal")
        initial_history = adapter.get_history()
        adapter.execute_operation_safe("add", [2.0, 3.0])
        final_history = adapter.get_history()
        # History should have grown by one entry
        assert len(final_history) == len(initial_history) + 1

    def test_execute_operation_safe_with_empty_operands_returns_error(self, adapter, session):
        """Test execute_operation_safe with empty operand list returns error."""
        session.set_mode("normal")
        result_str, error_msg = adapter.execute_operation_safe("add", [])
        assert result_str == ""
        assert error_msg != ""

    def test_execute_operation_safe_with_wrong_operand_count_returns_error(self, adapter, session):
        """Test execute_operation_safe with wrong number of operands returns error."""
        session.set_mode("normal")
        # 'add' expects 2 operands, give it 1
        result_str, error_msg = adapter.execute_operation_safe("add", [5.0])
        assert result_str == ""
        assert error_msg != ""

    def test_execute_operation_safe_with_too_many_operands_returns_error(self, adapter, session):
        """Test execute_operation_safe with too many operands returns error."""
        session.set_mode("normal")
        # 'add' expects 2 operands, give it 3
        result_str, error_msg = adapter.execute_operation_safe("add", [1.0, 2.0, 3.0])
        assert result_str == ""
        assert error_msg != ""

    def test_execute_operation_safe_unary_with_two_operands_returns_error(self, adapter, session):
        """Test execute_operation_safe unary op with 2 operands returns error."""
        session.set_mode("scientific")
        result_str, error_msg = adapter.execute_operation_safe("square", [5.0, 6.0])
        assert result_str == ""
        assert error_msg != ""

    def test_execute_operation_safe_multiple_successful_operations(self, adapter, session):
        """Test multiple successful operations record to history sequentially."""
        session.set_mode("normal")
        initial_count = len(adapter.get_history())

        adapter.execute_operation_safe("add", [1.0, 2.0])
        assert len(adapter.get_history()) == initial_count + 1

        adapter.execute_operation_safe("multiply", [3.0, 4.0])
        assert len(adapter.get_history()) == initial_count + 2


class TestSetMode:
    """Test suite for GUISessionAdapter.set_mode."""

    def test_set_mode_normal(self, adapter, session):
        """Test set_mode('normal') switches to normal mode."""
        adapter.set_mode("normal")
        assert session.get_current_mode() == "normal"

    def test_set_mode_scientific(self, adapter, session):
        """Test set_mode('scientific') switches to scientific mode."""
        adapter.set_mode("scientific")
        assert session.get_current_mode() == "scientific"

    def test_set_mode_updates_operation_list(self, adapter, session):
        """Test set_mode updates the available operations."""
        adapter.set_mode("normal")
        normal_ops = adapter.get_operations()

        adapter.set_mode("scientific")
        scientific_ops = adapter.get_operations()

        # Scientific should have more operations
        assert len(scientific_ops) > len(normal_ops)
        assert "sin" not in normal_ops
        assert "sin" in scientific_ops

    def test_set_mode_case_insensitive(self, adapter, session):
        """Test set_mode is case-insensitive."""
        adapter.set_mode("NORMAL")
        assert session.get_current_mode() == "normal"

        adapter.set_mode("ScIeNtIfIc")
        assert session.get_current_mode() == "scientific"


class TestGetOperations:
    """Test suite for GUISessionAdapter.get_operations."""

    def test_get_operations_normal_mode(self, adapter, session):
        """Test get_operations returns normal mode operations."""
        adapter.set_mode("normal")
        ops = adapter.get_operations()
        # Session returns operations in dir() order, not the mode definition order
        assert set(ops) == set(NORMAL_MODE_OPERATIONS)

    def test_get_operations_scientific_mode(self, adapter, session):
        """Test get_operations returns scientific mode operations."""
        adapter.set_mode("scientific")
        ops = adapter.get_operations()
        # Session returns operations in dir() order, not the mode definition order
        assert set(ops) == set(SCIENTIFIC_MODE_OPERATIONS)

    def test_get_operations_returns_list(self, adapter):
        """Test get_operations returns a list."""
        ops = adapter.get_operations()
        assert isinstance(ops, list)

    def test_get_operations_contains_strings(self, adapter):
        """Test get_operations returns list of strings."""
        ops = adapter.get_operations()
        assert all(isinstance(op, str) for op in ops)


class TestGetHistory:
    """Test suite for GUISessionAdapter.get_history."""

    def test_get_history_empty_initially(self, adapter):
        """Test get_history is empty when no operations recorded."""
        history = adapter.get_history()
        assert isinstance(history, list)
        assert len(history) == 0

    def test_get_history_after_operation(self, adapter, session):
        """Test get_history contains entry after successful operation."""
        session.set_mode("normal")
        initial_count = len(adapter.get_history())

        adapter.execute_operation_safe("add", [2.0, 3.0])
        history = adapter.get_history()

        assert len(history) == initial_count + 1

    def test_get_history_returns_formatted_strings(self, adapter, session):
        """Test get_history returns formatted string entries."""
        session.set_mode("normal")
        adapter.execute_operation_safe("add", [2.0, 3.0])

        history = adapter.get_history()
        assert len(history) > 0
        assert all(isinstance(entry, str) for entry in history)

    def test_get_history_maintains_insertion_order(self, adapter, session):
        """Test get_history maintains insertion order of operations."""
        session.set_mode("normal")

        adapter.execute_operation_safe("add", [1.0, 2.0])
        adapter.execute_operation_safe("multiply", [3.0, 4.0])

        history = adapter.get_history()
        # First entry should contain 'add', second should contain 'multiply'
        assert "add" in history[0].lower()
        assert "multiply" in history[1].lower()


class TestClearHistory:
    """Test suite for GUISessionAdapter.clear_history."""

    def test_clear_history_empties_history(self, adapter, session):
        """Test clear_history removes all history entries."""
        session.set_mode("normal")

        adapter.execute_operation_safe("add", [1.0, 2.0])
        assert len(adapter.get_history()) > 0

        adapter.clear_history()
        assert len(adapter.get_history()) == 0

    def test_clear_history_multiple_times(self, adapter, session):
        """Test clear_history can be called multiple times."""
        session.set_mode("normal")

        adapter.execute_operation_safe("add", [1.0, 2.0])
        adapter.clear_history()
        assert len(adapter.get_history()) == 0

        # Clear again should not raise error
        adapter.clear_history()
        assert len(adapter.get_history()) == 0

    def test_clear_history_allows_new_operations(self, adapter, session):
        """Test operations can be recorded after clear_history."""
        session.set_mode("normal")

        adapter.execute_operation_safe("add", [1.0, 2.0])
        adapter.clear_history()

        adapter.execute_operation_safe("multiply", [3.0, 4.0])
        history = adapter.get_history()

        assert len(history) == 1
        assert "multiply" in history[0].lower()


class TestGetArity:
    """Test suite for GUISessionAdapter.get_arity."""

    @pytest.mark.parametrize(
        "op_name,expected_arity",
        [
            ("add", 2),
            ("subtract", 2),
            ("multiply", 2),
            ("divide", 2),
            ("power", 2),
        ],
    )
    def test_get_arity_binary_operations(self, adapter, session, op_name, expected_arity):
        """Test get_arity returns 2 for binary operations."""
        session.set_mode("scientific")
        assert adapter.get_arity(op_name) == expected_arity

    @pytest.mark.parametrize(
        "op_name,expected_arity",
        [
            ("square", 1),
            ("square_root", 1),
            ("cube", 1),
            ("factorial", 1),
            ("sin", 1),
            ("cos", 1),
        ],
    )
    def test_get_arity_unary_operations(self, adapter, session, op_name, expected_arity):
        """Test get_arity returns 1 for unary operations."""
        session.set_mode("scientific")
        assert adapter.get_arity(op_name) == expected_arity

    def test_get_arity_normal_mode_binary(self, adapter, session):
        """Test get_arity in normal mode for binary operations."""
        session.set_mode("normal")
        assert adapter.get_arity("add") == 2
        assert adapter.get_arity("multiply") == 2

    def test_get_arity_normal_mode_unary(self, adapter, session):
        """Test get_arity in normal mode for unary operations."""
        session.set_mode("normal")
        assert adapter.get_arity("square") == 1
        assert adapter.get_arity("square_root") == 1
