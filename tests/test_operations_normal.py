"""Test suite for NormalOperations class."""

import pytest
from src.core.operations.normal import NormalOperations


class TestNormalOperationsAdd:
    """Test suite for NormalOperations.add() method."""

    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (0, 5, 5),
        (5, 0, 5),
        (-1, -2, -3),
        (-5, 5, 0),
        (2.5, 3.5, 6.0),
        (0.1, 0.2, pytest.approx(0.3)),
    ])
    def test_add_happy_path(self, a, b, expected):
        """Test add with various valid inputs."""
        result = NormalOperations.add(a, b)
        assert result == expected

    @pytest.mark.parametrize("a,b", [
        ("1", 2),
        (1, "2"),
        (None, 2),
        (2, None),
    ])
    def test_add_type_error(self, a, b):
        """Test add raises TypeError with invalid input types."""
        with pytest.raises(TypeError):
            NormalOperations.add(a, b)


class TestNormalOperationsSubtract:
    """Test suite for NormalOperations.subtract() method."""

    @pytest.mark.parametrize("a,b,expected", [
        (5, 2, 3),
        (0, 5, -5),
        (5, 0, 5),
        (-1, -2, 1),
        (-5, 5, -10),
        (2.5, 1.5, 1.0),
        (0.3, 0.2, pytest.approx(0.1)),
    ])
    def test_subtract_happy_path(self, a, b, expected):
        """Test subtract with various valid inputs."""
        result = NormalOperations.subtract(a, b)
        assert result == expected

    @pytest.mark.parametrize("a,b", [
        ("5", 2),
        (5, "2"),
        (None, 2),
        (5, None),
    ])
    def test_subtract_type_error(self, a, b):
        """Test subtract raises TypeError with invalid input types."""
        with pytest.raises(TypeError):
            NormalOperations.subtract(a, b)


class TestNormalOperationsMultiply:
    """Test suite for NormalOperations.multiply() method."""

    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 6),
        (0, 5, 0),
        (5, 0, 0),
        (-2, 3, -6),
        (-2, -3, 6),
        (2.5, 4, 10.0),
        (0.5, 0.5, 0.25),
    ])
    def test_multiply_happy_path(self, a, b, expected):
        """Test multiply with various valid inputs."""
        result = NormalOperations.multiply(a, b)
        assert result == expected

    @pytest.mark.parametrize("a,b", [
        ("2", None),
        (None, 3),
        (None, None),
    ])
    def test_multiply_type_error(self, a, b):
        """Test multiply raises TypeError with invalid input types."""
        with pytest.raises(TypeError):
            NormalOperations.multiply(a, b)


class TestNormalOperationsDivide:
    """Test suite for NormalOperations.divide() method."""

    @pytest.mark.parametrize("a,b,expected", [
        (10, 2, 5.0),
        (7, 2, 3.5),
        (0, 5, 0.0),
        (-10, 2, -5.0),
        (10, -2, -5.0),
        (-10, -2, 5.0),
        (2.5, 5, 0.5),
    ])
    def test_divide_happy_path(self, a, b, expected):
        """Test divide with various valid inputs."""
        result = NormalOperations.divide(a, b)
        assert result == expected

    def test_divide_by_zero(self):
        """Test divide by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            NormalOperations.divide(10, 0)

    def test_divide_zero_by_zero(self):
        """Test zero divided by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            NormalOperations.divide(0, 0)

    @pytest.mark.parametrize("a,b", [
        ("10", 2),
        (10, "2"),
        (None, 5),
        (10, None),
    ])
    def test_divide_type_error(self, a, b):
        """Test divide raises TypeError with invalid input types."""
        with pytest.raises(TypeError):
            NormalOperations.divide(a, b)
