import pytest
import math
from src.calculator import Calculator


class TestSquare:
    """Test suite for Calculator.square() method."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance for each test."""
        return Calculator()

    # Happy Path Tests
    @pytest.mark.parametrize("x,expected", [
        (2, 4.0),
        (3, 9.0),
        (0, 0.0),
        (-2, 4.0),
        (2.5, 6.25),
    ])
    def test_square_valid_inputs(self, calculator, x, expected):
        """Test square computation for valid int and float inputs."""
        result = calculator.square(x)
        assert result == pytest.approx(expected)

    # Edge Cases: Type Rejection
    @pytest.mark.parametrize("x", [True, False])
    def test_square_bool_raises_type_error(self, calculator, x):
        """Test square with boolean input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.square(x)

    @pytest.mark.parametrize("x", ["string", "5"])
    def test_square_string_raises_type_error(self, calculator, x):
        """Test square with string input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.square(x)

    @pytest.mark.parametrize("x", [None, [], {}, (1, 2)])
    def test_square_invalid_types_raise_type_error(self, calculator, x):
        """Test square with invalid types raises TypeError."""
        with pytest.raises(TypeError):
            calculator.square(x)


class TestCube:
    """Test suite for Calculator.cube() method."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance for each test."""
        return Calculator()

    # Happy Path Tests
    @pytest.mark.parametrize("x,expected", [
        (2, 8.0),
        (3, 27.0),
        (0, 0.0),
        (-2, -8.0),
        (2.5, 15.625),
    ])
    def test_cube_valid_inputs(self, calculator, x, expected):
        """Test cube computation for valid int and float inputs."""
        result = calculator.cube(x)
        assert result == pytest.approx(expected)

    # Edge Cases: Type Rejection
    @pytest.mark.parametrize("x", [True, False])
    def test_cube_bool_raises_type_error(self, calculator, x):
        """Test cube with boolean input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.cube(x)

    @pytest.mark.parametrize("x", ["string", "5"])
    def test_cube_string_raises_type_error(self, calculator, x):
        """Test cube with string input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.cube(x)

    @pytest.mark.parametrize("x", [None, [], {}, (1, 2)])
    def test_cube_invalid_types_raise_type_error(self, calculator, x):
        """Test cube with invalid types raises TypeError."""
        with pytest.raises(TypeError):
            calculator.cube(x)


class TestSquareRoot:
    """Test suite for Calculator.square_root() method."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance for each test."""
        return Calculator()

    # Happy Path Tests
    @pytest.mark.parametrize("x,expected", [
        (4, 2.0),
        (0, 0.0),
        (2, 1.4142135623730951),
        (6.25, 2.5),
    ])
    def test_square_root_valid_inputs(self, calculator, x, expected):
        """Test square root computation for valid non-negative inputs."""
        result = calculator.square_root(x)
        assert result == pytest.approx(expected)

    # Edge Cases: Negative Input Rejection
    @pytest.mark.parametrize("x", [-1, -100, -0.5])
    def test_square_root_negative_raises_value_error(self, calculator, x):
        """Test square root with negative input raises ValueError."""
        with pytest.raises(ValueError):
            calculator.square_root(x)

    # Edge Cases: Type Rejection
    @pytest.mark.parametrize("x", [True, False])
    def test_square_root_bool_raises_type_error(self, calculator, x):
        """Test square root with boolean input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.square_root(x)

    @pytest.mark.parametrize("x", ["string", "5"])
    def test_square_root_string_raises_type_error(self, calculator, x):
        """Test square root with string input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.square_root(x)

    @pytest.mark.parametrize("x", [None, [], {}, (1, 2)])
    def test_square_root_invalid_types_raise_type_error(self, calculator, x):
        """Test square root with invalid types raises TypeError."""
        with pytest.raises(TypeError):
            calculator.square_root(x)


class TestCubeRoot:
    """Test suite for Calculator.cube_root() method."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance for each test."""
        return Calculator()

    # Happy Path Tests - Positive Cube Roots
    @pytest.mark.parametrize("x,expected", [
        (8, 2.0),
        (0, 0.0),
        (27, 3.0),
        (15.625, 2.5),
    ])
    def test_cube_root_positive_inputs(self, calculator, x, expected):
        """Test cube root computation for valid positive inputs."""
        result = calculator.cube_root(x)
        assert result == pytest.approx(expected)

    # Happy Path Tests - Negative Cube Roots (must preserve sign)
    @pytest.mark.parametrize("x,expected", [
        (-8, -2.0),
        (-1, -1.0),
        (-27, -3.0),
    ])
    def test_cube_root_negative_inputs(self, calculator, x, expected):
        """Test cube root computation preserves sign for negative inputs."""
        result = calculator.cube_root(x)
        assert result == pytest.approx(expected)

    # Edge Cases: Type Rejection
    @pytest.mark.parametrize("x", [True, False])
    def test_cube_root_bool_raises_type_error(self, calculator, x):
        """Test cube root with boolean input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.cube_root(x)

    @pytest.mark.parametrize("x", ["string", "5"])
    def test_cube_root_string_raises_type_error(self, calculator, x):
        """Test cube root with string input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.cube_root(x)

    @pytest.mark.parametrize("x", [None, [], {}, (1, 2)])
    def test_cube_root_invalid_types_raise_type_error(self, calculator, x):
        """Test cube root with invalid types raises TypeError."""
        with pytest.raises(TypeError):
            calculator.cube_root(x)


class TestPower:
    """Test suite for Calculator.power() method."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance for each test."""
        return Calculator()

    # Happy Path Tests
    @pytest.mark.parametrize("base,exponent,expected", [
        (2, 3, 8.0),
        (10, 2, 100.0),
        (2, 0, 1.0),
        (0, 0, 1.0),
        (0, 2, 0.0),
        (2, -1, 0.5),
        (2, 0.5, 1.4142135623730951),
    ])
    def test_power_valid_inputs(self, calculator, base, exponent, expected):
        """Test power computation for valid inputs."""
        result = calculator.power(base, exponent)
        assert result == pytest.approx(expected)

    # Edge Cases: Type Rejection - Base is invalid
    @pytest.mark.parametrize("base", [True, False])
    def test_power_base_bool_raises_type_error(self, calculator, base):
        """Test power with boolean base raises TypeError."""
        with pytest.raises(TypeError):
            calculator.power(base, 2)

    @pytest.mark.parametrize("base", ["string", "5"])
    def test_power_base_string_raises_type_error(self, calculator, base):
        """Test power with string base raises TypeError."""
        with pytest.raises(TypeError):
            calculator.power(base, 2)

    @pytest.mark.parametrize("base", [None, [], {}, (1, 2)])
    def test_power_base_invalid_types_raise_type_error(self, calculator, base):
        """Test power with invalid base types raises TypeError."""
        with pytest.raises(TypeError):
            calculator.power(base, 2)

    # Edge Cases: Type Rejection - Exponent is invalid
    @pytest.mark.parametrize("exponent", [True, False])
    def test_power_exponent_bool_raises_type_error(self, calculator, exponent):
        """Test power with boolean exponent raises TypeError."""
        with pytest.raises(TypeError):
            calculator.power(2, exponent)

    @pytest.mark.parametrize("exponent", ["string", "5"])
    def test_power_exponent_string_raises_type_error(self, calculator, exponent):
        """Test power with string exponent raises TypeError."""
        with pytest.raises(TypeError):
            calculator.power(2, exponent)

    @pytest.mark.parametrize("exponent", [None, [], {}, (1, 2)])
    def test_power_exponent_invalid_types_raise_type_error(self, calculator, exponent):
        """Test power with invalid exponent types raises TypeError."""
        with pytest.raises(TypeError):
            calculator.power(2, exponent)


class TestLogarithm:
    """Test suite for Calculator.logarithm() method (base-10)."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance for each test."""
        return Calculator()

    # Happy Path Tests
    @pytest.mark.parametrize("x,expected", [
        (10, 1.0),
        (100, 2.0),
        (1, 0.0),
        (1000, 3.0),
    ])
    def test_logarithm_valid_inputs(self, calculator, x, expected):
        """Test base-10 logarithm computation for valid positive inputs."""
        result = calculator.logarithm(x)
        assert result == pytest.approx(expected)

    # Edge Cases: Zero and Negative Input Rejection
    @pytest.mark.parametrize("x", [0, -1, -100, -0.5])
    def test_logarithm_non_positive_raises_value_error(self, calculator, x):
        """Test logarithm with zero or negative input raises ValueError."""
        with pytest.raises(ValueError):
            calculator.logarithm(x)

    # Edge Cases: Type Rejection
    @pytest.mark.parametrize("x", [True, False])
    def test_logarithm_bool_raises_type_error(self, calculator, x):
        """Test logarithm with boolean input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.logarithm(x)

    @pytest.mark.parametrize("x", ["string", "5"])
    def test_logarithm_string_raises_type_error(self, calculator, x):
        """Test logarithm with string input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.logarithm(x)

    @pytest.mark.parametrize("x", [None, [], {}, (1, 2)])
    def test_logarithm_invalid_types_raise_type_error(self, calculator, x):
        """Test logarithm with invalid types raises TypeError."""
        with pytest.raises(TypeError):
            calculator.logarithm(x)


class TestNaturalLogarithm:
    """Test suite for Calculator.natural_logarithm() method (base-e)."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance for each test."""
        return Calculator()

    # Happy Path Tests
    @pytest.mark.parametrize("x,expected", [
        (1, 0.0),
        (math.e, 1.0),
        (10, 2.302585092994046),
    ])
    def test_natural_logarithm_valid_inputs(self, calculator, x, expected):
        """Test natural logarithm computation for valid positive inputs."""
        result = calculator.natural_logarithm(x)
        assert result == pytest.approx(expected)

    # Edge Cases: Zero and Negative Input Rejection
    @pytest.mark.parametrize("x", [0, -1, -100, -0.5])
    def test_natural_logarithm_non_positive_raises_value_error(self, calculator, x):
        """Test natural logarithm with zero or negative input raises ValueError."""
        with pytest.raises(ValueError):
            calculator.natural_logarithm(x)

    # Edge Cases: Type Rejection
    @pytest.mark.parametrize("x", [True, False])
    def test_natural_logarithm_bool_raises_type_error(self, calculator, x):
        """Test natural logarithm with boolean input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.natural_logarithm(x)

    @pytest.mark.parametrize("x", ["string", "5"])
    def test_natural_logarithm_string_raises_type_error(self, calculator, x):
        """Test natural logarithm with string input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.natural_logarithm(x)

    @pytest.mark.parametrize("x", [None, [], {}, (1, 2)])
    def test_natural_logarithm_invalid_types_raise_type_error(self, calculator, x):
        """Test natural logarithm with invalid types raises TypeError."""
        with pytest.raises(TypeError):
            calculator.natural_logarithm(x)
