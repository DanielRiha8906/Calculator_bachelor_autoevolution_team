"""Comprehensive tests for CalculatorSession class."""

import pytest
import tempfile
from pathlib import Path

from src.session import CalculatorSession


class TestCalculatorSessionInitialization:
    """Test suite for CalculatorSession initialization."""

    def test_session_creates_with_empty_history(self):
        """Test that a fresh session has empty history."""
        session = CalculatorSession()
        assert session.get_history() == []

    def test_session_default_history_file(self):
        """Test that default history file is 'history.txt'."""
        session = CalculatorSession()
        assert session._history_file == "history.txt"

    def test_session_custom_history_file(self):
        """Test that custom history file path is stored correctly."""
        custom_path = "/custom/path/to/history.txt"
        session = CalculatorSession(history_file=custom_path)
        assert session._history_file == custom_path

    def test_session_has_calculator(self):
        """Test that session has a wrapped calculator."""
        session = CalculatorSession()
        calc = session.get_calculator()
        assert calc is not None

    def test_multiple_sessions_have_independent_histories(self):
        """Test that two sessions don't share history."""
        session1 = CalculatorSession()
        session2 = CalculatorSession()
        assert session1.get_history() == session2.get_history()
        # This is trivial (both empty), but verifies they are different objects
        assert session1._history is not session2._history


class TestCalculatorSessionWrapper:
    """Test suite for wrapped calculator operations and history recording."""

    @pytest.fixture
    def session(self):
        """Fixture providing a fresh CalculatorSession."""
        return CalculatorSession()

    def test_get_calculator_returns_wrapped_instance(self, session):
        """Test that get_calculator returns a usable object."""
        calc = session.get_calculator()
        assert calc is not None
        # Verify it has callable methods
        assert callable(getattr(calc, "add", None))

    def test_wrapped_add_records_to_history(self, session):
        """Test that add operation is recorded to history."""
        calc = session.get_calculator()
        result = calc.add(2, 3)
        assert result == 5
        entries = session.get_history()
        assert len(entries) == 1
        assert entries[0] == "add(2, 3) = 5"

    def test_wrapped_subtract_records_to_history(self, session):
        """Test that subtract operation is recorded."""
        calc = session.get_calculator()
        result = calc.subtract(10, 4)
        assert result == 6
        entries = session.get_history()
        assert len(entries) == 1
        assert entries[0] == "subtract(10, 4) = 6"

    def test_wrapped_multiply_records_to_history(self, session):
        """Test that multiply operation is recorded."""
        calc = session.get_calculator()
        result = calc.multiply(3, 4)
        assert result == 12
        entries = session.get_history()
        assert len(entries) == 1
        assert entries[0] == "multiply(3, 4) = 12"

    def test_wrapped_divide_records_to_history(self, session):
        """Test that divide operation is recorded."""
        calc = session.get_calculator()
        result = calc.divide(10, 2)
        assert result == 5.0
        entries = session.get_history()
        assert len(entries) == 1
        # Result should be 5 not 5.0 (whole-number float formatting)
        assert entries[0] == "divide(10, 2) = 5"

    def test_wrapped_square_records_to_history(self, session):
        """Test that unary square operation is recorded."""
        calc = session.get_calculator()
        result = calc.square(4)
        assert result == 16.0
        entries = session.get_history()
        assert len(entries) == 1
        assert entries[0] == "square(4) = 16"

    def test_wrapped_factorial_records_to_history(self, session):
        """Test that factorial operation is recorded."""
        calc = session.get_calculator()
        result = calc.factorial(5)
        assert result == 120
        entries = session.get_history()
        assert len(entries) == 1
        assert entries[0] == "factorial(5) = 120"

    def test_wrapped_power_records_to_history(self, session):
        """Test that power operation is recorded."""
        calc = session.get_calculator()
        result = calc.power(2, 10)
        assert result == 1024.0
        entries = session.get_history()
        assert len(entries) == 1
        assert entries[0] == "power(2, 10) = 1024"

    def test_wrapped_cube_records_to_history(self, session):
        """Test that cube operation is recorded."""
        calc = session.get_calculator()
        result = calc.cube(3)
        assert result == 27.0
        entries = session.get_history()
        assert len(entries) == 1
        assert entries[0] == "cube(3) = 27"

    def test_wrapped_square_root_records_to_history(self, session):
        """Test that square_root operation is recorded."""
        calc = session.get_calculator()
        result = calc.square_root(9)
        assert result == 3.0
        entries = session.get_history()
        assert len(entries) == 1
        assert entries[0] == "square_root(9) = 3"

    def test_wrapped_cube_root_records_to_history(self, session):
        """Test that cube_root operation is recorded."""
        calc = session.get_calculator()
        result = calc.cube_root(8)
        assert result == 2.0
        entries = session.get_history()
        assert len(entries) == 1
        assert entries[0] == "cube_root(8) = 2"

    def test_wrapped_calculator_result_unchanged(self, session):
        """Test that wrapper returns same result as direct calculator."""
        from src.calculator import Calculator
        calc_direct = Calculator()
        calc_wrapped = session.get_calculator()

        test_cases = [
            ("add", [2, 3]),
            ("subtract", [10, 4]),
            ("multiply", [3, 4]),
            ("divide", [10, 2]),
            ("square", [5]),
            ("factorial", [4]),
        ]

        for method_name, args in test_cases:
            direct_result = getattr(calc_direct, method_name)(*args)
            wrapped_result = getattr(calc_wrapped, method_name)(*args)
            assert direct_result == wrapped_result

    def test_wrapped_non_callable_attributes_pass_through(self, session):
        """Test that non-callable attributes pass through without wrapping."""
        calc = session.get_calculator()
        # __class__ should be accessible without modification
        assert calc.__class__ is not None


class TestCalculatorSessionPersistence:
    """Test suite for save_and_close file persistence."""

    @pytest.fixture
    def session(self):
        """Fixture providing a fresh CalculatorSession."""
        def _make_session(history_file=None):
            if history_file:
                return CalculatorSession(history_file=history_file)
            return CalculatorSession()
        return _make_session

    def test_save_and_close_writes_file(self, session, tmp_path):
        """Test that save_and_close creates the history file."""
        filepath = tmp_path / "session_history.txt"
        s = session(history_file=str(filepath))
        calc = s.get_calculator()
        calc.add(1, 1)
        s.save_and_close()
        assert filepath.exists()

    def test_save_and_close_file_content(self, session, tmp_path):
        """Test that file content matches expected entries."""
        filepath = tmp_path / "session_history.txt"
        s = session(history_file=str(filepath))
        calc = s.get_calculator()
        calc.add(2, 3)
        calc.multiply(4, 5)
        s.save_and_close()
        content = filepath.read_text(encoding="utf-8")
        lines = content.strip().split("\n")
        assert len(lines) == 2
        assert lines[0] == "add(2, 3) = 5"
        assert lines[1] == "multiply(4, 5) = 20"

    def test_save_and_close_empty_session(self, session, tmp_path):
        """Test that save_and_close with no operations creates empty file."""
        filepath = tmp_path / "empty_history.txt"
        s = session(history_file=str(filepath))
        s.save_and_close()
        assert filepath.exists()
        content = filepath.read_text(encoding="utf-8")
        assert content == ""

    def test_save_and_close_with_float_results(self, session, tmp_path):
        """Test that save_and_close preserves float results correctly."""
        filepath = tmp_path / "float_history.txt"
        s = session(history_file=str(filepath))
        calc = s.get_calculator()
        calc.divide(7, 2)
        s.save_and_close()
        content = filepath.read_text(encoding="utf-8")
        assert "divide(7, 2) = 3.5" in content


class TestCalculatorSessionHistory:
    """Test suite for history accumulation and retrieval."""

    @pytest.fixture
    def session(self):
        """Fixture providing a fresh CalculatorSession."""
        return CalculatorSession()

    def test_history_accumulates_across_operations(self, session):
        """Test that multiple operations accumulate in history."""
        calc = session.get_calculator()
        assert len(session.get_history()) == 0
        calc.add(1, 2)
        assert len(session.get_history()) == 1
        calc.multiply(3, 4)
        assert len(session.get_history()) == 2
        calc.subtract(10, 5)
        assert len(session.get_history()) == 3

    def test_history_initially_empty(self, session):
        """Test that fresh session has no history."""
        assert session.get_history() == []

    def test_history_entries_in_order(self, session):
        """Test that history entries maintain insertion order."""
        calc = session.get_calculator()
        calc.add(1, 1)
        calc.multiply(2, 2)
        calc.divide(10, 2)
        entries = session.get_history()
        assert entries[0] == "add(1, 1) = 2"
        assert entries[1] == "multiply(2, 2) = 4"
        assert entries[2] == "divide(10, 2) = 5"

    def test_get_history_returns_copy(self, session):
        """Test that get_history returns a copy, not the internal list."""
        calc = session.get_calculator()
        calc.add(1, 1)
        hist1 = session.get_history()
        hist2 = session.get_history()
        assert hist1 == hist2
        # Verify they are different objects
        hist1.append("fake entry")
        assert len(session.get_history()) == 1

    def test_history_with_negative_arguments(self, session):
        """Test that history records negative arguments correctly."""
        calc = session.get_calculator()
        calc.add(-5, 3)
        calc.subtract(-10, -4)
        entries = session.get_history()
        assert entries[0] == "add(-5, 3) = -2"
        assert entries[1] == "subtract(-10, -4) = -6"
