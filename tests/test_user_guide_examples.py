"""Test examples and usage patterns documented in USER_GUIDE.md.

Verifies that the calculator can perform all documented operations
with expected results and that session features work as documented.
"""

import pytest
import tempfile
import os
from pathlib import Path

from src.session import CalculatorSession
from src.core.calculator import Calculator
from src.history import OperationHistory


class TestUserGuideExamples:
    """Test examples from USER_GUIDE.md."""

    @pytest.fixture
    def session(self):
        """Create a calculator session."""
        calc = Calculator()
        return CalculatorSession(calc)

    def test_basic_add_example(self, session):
        """Test basic addition example: add(2, 3) = 5."""
        calc = session._calculator
        result = calc.add(2, 3)
        assert result == 5

    def test_basic_add_with_floats(self, session):
        """Test addition with float operands."""
        calc = session._calculator
        result = calc.add(2.5, 3.5)
        assert result == 6.0

    def test_basic_subtract_example(self, session):
        """Test subtraction: subtract(10, 3) = 7."""
        calc = session._calculator
        result = calc.subtract(10, 3)
        assert result == 7

    def test_basic_multiply_example(self, session):
        """Test multiplication: multiply(4, 5) = 20."""
        calc = session._calculator
        result = calc.multiply(4, 5)
        assert result == 20

    def test_basic_divide_example(self, session):
        """Test division example: divide(10, 2) = 5.0."""
        calc = session._calculator
        result = calc.divide(10, 2)
        assert result == 5.0

    def test_divide_with_remainder(self, session):
        """Test division with non-whole result: divide(7, 2) = 3.5."""
        calc = session._calculator
        result = calc.divide(7, 2)
        assert result == 3.5

    def test_square_example(self, session):
        """Test square operation: square(5) = 25.0."""
        calc = session._calculator
        result = calc.square(5)
        assert result == 25.0

    def test_square_with_decimal(self, session):
        """Test square with decimal input: square(2.5) = 6.25."""
        calc = session._calculator
        result = calc.square(2.5)
        assert result == 6.25

    def test_cube_example(self, session):
        """Test cube operation: cube(3) = 27.0."""
        calc = session._calculator
        result = calc.cube(3)
        assert result == 27.0

    def test_square_root_example(self, session):
        """Test square root: square_root(9) = 3.0."""
        calc = session._calculator
        result = calc.square_root(9)
        assert result == 3.0

    def test_square_root_non_perfect(self, session):
        """Test square root of non-perfect square."""
        calc = session._calculator
        result = calc.square_root(2)
        assert abs(result - 1.414213562) < 0.0001

    def test_history_saving(self, session):
        """Test that history can be saved to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "history.txt")

            # Perform some operations
            session.record_history("add", [2.0, 3.0], 5)
            session.record_history("multiply", [4.0, 5.0], 20)

            # Save history
            session.save_history(history_file)

            # Verify file exists and contains operations
            assert Path(history_file).exists()
            content = Path(history_file).read_text()
            assert "add(2, 3) = 5" in content
            assert "multiply(4, 5) = 20" in content

    def test_session_independence(self):
        """Test that two sessions have separate operation histories."""
        calc1 = Calculator()
        session1 = CalculatorSession(calc1)

        calc2 = Calculator()
        session2 = CalculatorSession(calc2)

        # Perform operations in session 1
        session1.record_history("add", [1.0, 2.0], 3)
        session1.record_history("subtract", [5.0, 2.0], 3)

        # Perform operations in session 2
        session2.record_history("multiply", [3.0, 4.0], 12)

        # Verify histories are separate
        history1 = session1.get_history()
        history2 = session2.get_history()

        assert len(history1) == 2
        assert len(history2) == 1
        assert any("add" in entry for entry in history1)
        assert any("multiply" in entry for entry in history2)
        assert not any("multiply" in entry for entry in history1)

    def test_history_ordering(self, session):
        """Test that history entries are in the order they were recorded."""
        session.record_history("add", [1.0, 2.0], 3)
        session.record_history("subtract", [5.0, 2.0], 3)
        session.record_history("multiply", [2.0, 3.0], 6)

        history = session.get_history()
        assert len(history) == 3
        assert "add" in history[0]
        assert "subtract" in history[1]
        assert "multiply" in history[2]

    def test_whole_number_float_formatting(self, session):
        """Test that whole-number floats are displayed as integers in history."""
        session.record_history("add", [2.0, 3.0], 5.0)
        history = session.get_history()

        assert "add(2, 3) = 5" in history[0]
        # Should not contain decimal point for whole number
        assert "5.0" not in history[0]

    def test_non_whole_float_formatting(self, session):
        """Test that non-whole floats keep decimal points in history."""
        session.record_history("divide", [7.0, 2.0], 3.5)
        history = session.get_history()

        assert "divide(7, 2) = 3.5" in history[0]
        # Should preserve the decimal part
        assert "3.5" in history[0]

    def test_operation_list_available(self, session):
        """Test that all operations are available in the session."""
        operations = session.get_operation_list()

        # Should contain basic operations
        assert "add" in operations
        assert "subtract" in operations
        assert "multiply" in operations
        assert "divide" in operations

        # Should contain advanced operations
        assert "square" in operations
        assert "cube" in operations
        assert "square_root" in operations

    def test_operation_arity_retrieval(self, session):
        """Test that arity can be retrieved for operations."""
        # Binary operations
        arity_add = session.get_arity("add")
        assert arity_add == 2

        arity_subtract = session.get_arity("subtract")
        assert arity_subtract == 2

        # Unary operations
        arity_square = session.get_arity("square")
        assert arity_square == 1

        arity_cube = session.get_arity("cube")
        assert arity_cube == 1

    def test_factorial_example(self, session):
        """Test factorial operation: factorial(5) = 120."""
        calc = session._calculator
        result = calc.factorial(5)
        assert result == 120

    def test_factorial_edge_case_zero(self, session):
        """Test factorial(0) = 1."""
        calc = session._calculator
        result = calc.factorial(0)
        assert result == 1

    def test_logarithm_example(self, session):
        """Test logarithm: logarithm(100) = 2.0."""
        calc = session._calculator
        result = calc.logarithm(100)
        assert result == 2.0

    def test_natural_logarithm_example(self, session):
        """Test natural logarithm."""
        calc = session._calculator
        result = calc.natural_logarithm(1.0)
        assert result == 0.0

    def test_power_example(self, session):
        """Test power operation: power(2, 3) = 8.0."""
        calc = session._calculator
        result = calc.power(2, 3)
        assert result == 8.0

    def test_cube_root_example(self, session):
        """Test cube root: cube_root(8) = 2.0."""
        calc = session._calculator
        result = calc.cube_root(8)
        assert result == 2.0

    def test_cube_root_negative(self, session):
        """Test cube root of negative number."""
        calc = session._calculator
        result = calc.cube_root(-8)
        assert result == -2.0

    def test_multiple_sessions_separate_histories(self):
        """Test that running multiple sessions produces separate histories."""
        # Session 1
        calc1 = Calculator()
        session1 = CalculatorSession(calc1)
        session1.record_history("add", [1.0, 2.0], 3)

        # Session 2
        calc2 = Calculator()
        session2 = CalculatorSession(calc2)
        session2.record_history("subtract", [5.0, 2.0], 3)

        # Histories should be separate
        assert session1.get_history() != session2.get_history()

    def test_history_file_write_overwrites_previous(self):
        """Test that saving history to file overwrites previous content."""
        session = CalculatorSession(Calculator())

        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "history.txt")

            # First save
            session.record_history("add", [1.0, 2.0], 3)
            session.save_history(history_file)

            content1 = Path(history_file).read_text()
            assert "add(1, 2) = 3" in content1

            # Clear history and save again
            session._history.clear()
            session.record_history("multiply", [4.0, 5.0], 20)
            session.save_history(history_file)

            content2 = Path(history_file).read_text()
            # Should only contain the second operation
            assert "multiply(4, 5) = 20" in content2
            assert "add" not in content2
