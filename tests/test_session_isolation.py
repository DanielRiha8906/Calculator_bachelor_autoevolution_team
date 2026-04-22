"""Test session isolation and independence.

Verifies that each session has independent state including history,
error logs, and calculator instances.
"""

import pytest
from src.session import CalculatorSession
from src.core.calculator import Calculator
from src.history import OperationHistory
from src.error_logger import ErrorLogger
import tempfile
import os


class TestSessionIsolation:
    """Test that sessions are isolated from one another."""

    @pytest.fixture
    def session_a(self):
        """Create the first calculator session."""
        calc = Calculator()
        return CalculatorSession(calc)

    @pytest.fixture
    def session_b(self):
        """Create a second calculator session."""
        calc = Calculator()
        return CalculatorSession(calc)

    def test_each_session_has_empty_history_on_creation(self, session_a):
        """Test that a new session has empty history."""
        history = session_a.get_history()
        assert isinstance(history, list)
        assert len(history) == 0

    def test_history_not_shared_between_sessions(self, session_a, session_b):
        """Test that history from one session doesn't appear in another."""
        # Add operation to session A
        session_a.record_history("add", [2.0, 3.0], 5)
        history_a = session_a.get_history()
        assert len(history_a) == 1
        assert "add(2, 3) = 5" in history_a[0]

        # Session B should still have empty history
        history_b = session_b.get_history()
        assert len(history_b) == 0

    def test_independent_histories_multiple_operations(self, session_a, session_b):
        """Test that multiple operations in sessions remain isolated."""
        # Session A: add, subtract
        session_a.record_history("add", [2.0, 3.0], 5)
        session_a.record_history("subtract", [10.0, 3.0], 7)

        # Session B: multiply
        session_b.record_history("multiply", [4.0, 5.0], 20)

        history_a = session_a.get_history()
        history_b = session_b.get_history()

        assert len(history_a) == 2
        assert len(history_b) == 1
        assert any("add" in entry for entry in history_a)
        assert any("subtract" in entry for entry in history_a)
        assert any("multiply" in entry for entry in history_b)

    def test_error_log_is_append_only(self):
        """Test that error logs accumulate across sessions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = os.path.join(tmpdir, "error.log")

            # First session: log an error
            logger1 = ErrorLogger(log_path)
            logger1.log_unsupported_operation("fake_op_1")

            # Read first log
            with open(log_path, "r") as f:
                content_after_first = f.read()
            assert "fake_op_1" in content_after_first
            lines_after_first = len([l for l in content_after_first.strip().split("\n") if l])

            # Second session: log another error to same file (append mode)
            logger2 = ErrorLogger(log_path)
            logger2.log_invalid_operand("abc", "not a number")

            # Read second log
            with open(log_path, "r") as f:
                content_after_second = f.read()

            # Both errors should be in the log now
            assert "fake_op_1" in content_after_second
            assert "abc" in content_after_second
            lines_after_second = len(
                [l for l in content_after_second.strip().split("\n") if l]
            )

            # Second read should have more lines (append mode)
            assert lines_after_second > lines_after_first

    def test_calculator_instance_scoped_to_session(self, session_a, session_b):
        """Test that each session owns its calculator instance."""
        # Get the calculator instances
        calc_a = session_a._calculator
        calc_b = session_b._calculator

        # They should be different instances
        assert calc_a is not calc_b

        # Both should work independently
        result_a = calc_a.add(2, 3)
        result_b = calc_b.add(5, 5)

        assert result_a == 5
        assert result_b == 10

    def test_operation_list_independent_per_session(self, session_a, session_b):
        """Test that operation lists are independent per session."""
        ops_a = session_a.get_operation_list()
        ops_b = session_b.get_operation_list()

        # Both should have the same operations (from the same Calculator class)
        assert ops_a == ops_b

        # But they should be separate list objects
        assert ops_a is not ops_b

    def test_session_history_cleared_on_new_session(self):
        """Test that a new session starts with cleared history."""
        session1 = CalculatorSession(Calculator())
        session1.record_history("add", [1.0, 2.0], 3)

        # Create new session
        session2 = CalculatorSession(Calculator())

        # Session 2 should have no history
        assert len(session2.get_history()) == 0
        # Session 1 should still have history
        assert len(session1.get_history()) == 1

    def test_multiple_error_loggers_independent(self):
        """Test that multiple ErrorLogger instances log to their own files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log1_path = os.path.join(tmpdir, "error1.log")
            log2_path = os.path.join(tmpdir, "error2.log")

            logger1 = ErrorLogger(log1_path)
            logger2 = ErrorLogger(log2_path)

            logger1.log_unsupported_operation("op1")
            logger2.log_invalid_operand("xyz", "reason")

            with open(log1_path, "r") as f:
                content1 = f.read()
            with open(log2_path, "r") as f:
                content2 = f.read()

            assert "op1" in content1
            assert "UNSUPPORTED_OPERATION" in content1
            assert "xyz" not in content1

            assert "xyz" in content2
            assert "INVALID_OPERAND" in content2
            assert "op1" not in content2

    def test_session_max_retries_property_consistent(self, session_a, session_b):
        """Test that max_retries property is consistent across sessions."""
        retries_a = session_a.max_retries
        retries_b = session_b.max_retries

        assert retries_a == retries_b
        assert retries_a == 5  # Default is 5

    def test_session_get_history_returns_copy(self, session_a):
        """Test that get_history returns a copy, not the internal list."""
        session_a.record_history("add", [1.0, 2.0], 3)

        history1 = session_a.get_history()
        history2 = session_a.get_history()

        # Should be equal but not the same object
        assert history1 == history2
        assert history1 is not history2

    def test_history_isolation_after_clear(self):
        """Test that clearing history in one session doesn't affect another."""
        session_a = CalculatorSession(Calculator())
        session_b = CalculatorSession(Calculator())

        session_a.record_history("add", [1.0, 2.0], 3)
        session_b.record_history("subtract", [5.0, 2.0], 3)

        assert len(session_a.get_history()) == 1
        assert len(session_b.get_history()) == 1

        # Clear session A's history internally
        session_a._history.clear()

        # Session A should be empty, session B unchanged
        assert len(session_a.get_history()) == 0
        assert len(session_b.get_history()) == 1
