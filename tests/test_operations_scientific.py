"""Test suite for ScientificOperations class."""

import pytest
import math
from src.core.operations.scientific import ScientificOperations


class TestScientificOperationsFactorial:
    """Test suite for ScientificOperations.factorial() method."""

    @pytest.mark.parametrize("n,expected", [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (5, 120),
        (10, 3628800),
    ])
    def test_factorial_happy_path(self, n, expected):
        """Test factorial with valid non-negative integers."""
        result = ScientificOperations.factorial(n)
        assert result == expected

    @pytest.mark.parametrize("n", [-1, -5, -100])
    def test_factorial_negative_raises_valueerror(self, n):
        """Test factorial with negative numbers raises ValueError."""
        with pytest.raises(ValueError, match="n must be >= 0"):
            ScientificOperations.factorial(n)

    @pytest.mark.parametrize("n", [2.5, "5", 3.14, [5], None])
    def test_factorial_non_int_raises_typeerror(self, n):
        """Test factorial with non-integer types raises TypeError."""
        with pytest.raises(TypeError, match="n must be an int"):
            ScientificOperations.factorial(n)

    def test_factorial_bool_raises_typeerror(self):
        """Test factorial with bool raises TypeError (bool is excluded)."""
        with pytest.raises(TypeError, match="n must be an int"):
            ScientificOperations.factorial(True)


class TestScientificOperationsSquare:
    """Test suite for ScientificOperations.square() method."""

    @pytest.mark.parametrize("x,expected", [
        (2, 4.0),
        (3, 9.0),
        (0, 0.0),
        (-2, 4.0),
        (-3, 9.0),
        (2.5, 6.25),
        (-2.5, 6.25),
        (1e10, 1e20),
    ])
    def test_square_happy_path(self, x, expected):
        """Test square with valid numeric inputs."""
        result = ScientificOperations.square(x)
        assert result == expected or result == pytest.approx(expected)

    @pytest.mark.parametrize("x", ["2", "hello", [2], None, {"x": 2}])
    def test_square_invalid_type_raises_typeerror(self, x):
        """Test square with invalid types raises TypeError."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.square(x)

    def test_square_bool_raises_typeerror(self):
        """Test square with bool raises TypeError (bool is excluded)."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.square(True)


class TestScientificOperationsCube:
    """Test suite for ScientificOperations.cube() method."""

    @pytest.mark.parametrize("x,expected", [
        (2, 8.0),
        (3, 27.0),
        (0, 0.0),
        (-2, -8.0),
        (-3, -27.0),
        (2.5, 15.625),
        (-2.5, -15.625),
    ])
    def test_cube_happy_path(self, x, expected):
        """Test cube with valid numeric inputs."""
        result = ScientificOperations.cube(x)
        assert result == expected or result == pytest.approx(expected)

    @pytest.mark.parametrize("x", ["2", "hello", [2], None])
    def test_cube_invalid_type_raises_typeerror(self, x):
        """Test cube with invalid types raises TypeError."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.cube(x)

    def test_cube_bool_raises_typeerror(self):
        """Test cube with bool raises TypeError (bool is excluded)."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.cube(True)


class TestScientificOperationsSquareRoot:
    """Test suite for ScientificOperations.square_root() method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0.0),
        (1, 1.0),
        (4, 2.0),
        (9, 3.0),
        (2, pytest.approx(1.414213562)),
        (100, 10.0),
    ])
    def test_square_root_happy_path(self, x, expected):
        """Test square_root with valid non-negative inputs."""
        result = ScientificOperations.square_root(x)
        assert result == expected or result == pytest.approx(expected)

    @pytest.mark.parametrize("x", [-1, -5, -100, -2.5])
    def test_square_root_negative_raises_valueerror(self, x):
        """Test square_root with negative numbers raises ValueError."""
        with pytest.raises(ValueError, match="x must be non-negative for square root"):
            ScientificOperations.square_root(x)

    @pytest.mark.parametrize("x", ["4", "hello", [4], None])
    def test_square_root_invalid_type_raises_typeerror(self, x):
        """Test square_root with invalid types raises TypeError."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.square_root(x)

    def test_square_root_bool_raises_typeerror(self):
        """Test square_root with bool raises TypeError (bool is excluded)."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.square_root(True)


class TestScientificOperationsCubeRoot:
    """Test suite for ScientificOperations.cube_root() method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0.0),
        (1, 1.0),
        (8, 2.0),
        (27, 3.0),
        (-8, -2.0),
        (-27, -3.0),
        (2, pytest.approx(1.2599210498948731)),
    ])
    def test_cube_root_happy_path(self, x, expected):
        """Test cube_root with valid numeric inputs, including negative."""
        result = ScientificOperations.cube_root(x)
        assert result == expected or result == pytest.approx(expected)

    @pytest.mark.parametrize("x", ["8", "hello", [8], None])
    def test_cube_root_invalid_type_raises_typeerror(self, x):
        """Test cube_root with invalid types raises TypeError."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.cube_root(x)

    def test_cube_root_bool_raises_typeerror(self):
        """Test cube_root with bool raises TypeError (bool is excluded)."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.cube_root(True)


class TestScientificOperationsLogarithm:
    """Test suite for ScientificOperations.logarithm() method."""

    @pytest.mark.parametrize("x,expected", [
        (1, 0.0),
        (10, 1.0),
        (100, 2.0),
        (0.1, -1.0),
    ])
    def test_logarithm_happy_path(self, x, expected):
        """Test logarithm with valid positive inputs."""
        result = ScientificOperations.logarithm(x)
        assert result == expected or result == pytest.approx(expected)

    @pytest.mark.parametrize("x", [0, -1, -5, -100, -2.5])
    def test_logarithm_non_positive_raises_valueerror(self, x):
        """Test logarithm with zero or negative raises ValueError."""
        with pytest.raises(ValueError, match="x must be positive for logarithm"):
            ScientificOperations.logarithm(x)

    @pytest.mark.parametrize("x", ["10", "hello", [10], None])
    def test_logarithm_invalid_type_raises_typeerror(self, x):
        """Test logarithm with invalid types raises TypeError."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.logarithm(x)

    def test_logarithm_bool_raises_typeerror(self):
        """Test logarithm with bool raises TypeError (bool is excluded)."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.logarithm(True)


class TestScientificOperationsNaturalLogarithm:
    """Test suite for ScientificOperations.natural_logarithm() method."""

    @pytest.mark.parametrize("x,expected", [
        (1, 0.0),
        (math.e, pytest.approx(1.0)),
        (2, pytest.approx(0.693147180559945)),
        (10, pytest.approx(2.302585092994046)),
    ])
    def test_natural_logarithm_happy_path(self, x, expected):
        """Test natural_logarithm with valid positive inputs."""
        result = ScientificOperations.natural_logarithm(x)
        assert result == expected or result == pytest.approx(expected)

    @pytest.mark.parametrize("x", [0, -1, -5, -100, -2.5])
    def test_natural_logarithm_non_positive_raises_valueerror(self, x):
        """Test natural_logarithm with zero or negative raises ValueError."""
        with pytest.raises(ValueError, match="x must be positive for natural logarithm"):
            ScientificOperations.natural_logarithm(x)

    @pytest.mark.parametrize("x", ["10", "hello", [10], None])
    def test_natural_logarithm_invalid_type_raises_typeerror(self, x):
        """Test natural_logarithm with invalid types raises TypeError."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.natural_logarithm(x)

    def test_natural_logarithm_bool_raises_typeerror(self):
        """Test natural_logarithm with bool raises TypeError (bool is excluded)."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.natural_logarithm(True)


class TestScientificOperationsPower:
    """Test suite for ScientificOperations.power() method."""

    @pytest.mark.parametrize("base,exponent,expected", [
        (2, 3, 8.0),
        (2, 0, 1.0),
        (0, 0, 1.0),
        (3, 2, 9.0),
        (-2, 2, 4.0),
        (-2, 3, -8.0),
        (2, -1, 0.5),
        (2, 0.5, pytest.approx(1.414213562)),
        (10, 3, 1000.0),
    ])
    def test_power_happy_path(self, base, exponent, expected):
        """Test power with valid numeric inputs."""
        result = ScientificOperations.power(base, exponent)
        assert result == expected or result == pytest.approx(expected)

    @pytest.mark.parametrize("base,exponent", [
        ("2", 3),
        (2, "3"),
        ("hello", 2),
        (2, "world"),
        (None, 3),
        (2, None),
    ])
    def test_power_invalid_base_or_exponent_raises_typeerror(self, base, exponent):
        """Test power with invalid base or exponent types raises TypeError."""
        with pytest.raises(TypeError, match="base must be an int or float|exponent must be an int or float"):
            ScientificOperations.power(base, exponent)

    @pytest.mark.parametrize("base,exponent", [
        (True, 2),
        (2, True),
        (False, 5),
        (3, False),
    ])
    def test_power_bool_raises_typeerror(self, base, exponent):
        """Test power with bool raises TypeError (bool is excluded)."""
        with pytest.raises(TypeError, match="base must be an int or float|exponent must be an int or float"):
            ScientificOperations.power(base, exponent)
