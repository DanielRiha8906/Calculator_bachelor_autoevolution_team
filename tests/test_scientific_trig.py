"""Tests for trigonometric operations in ScientificOperations and Calculator."""

import pytest
import math
from src.core.operations.scientific import ScientificOperations
from src.core.calculator import Calculator


class TestScientificOperationsSin:
    """Test suite for ScientificOperations.sin() static method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0.0),
        (math.pi / 2, 1.0),
        (math.pi, 0.0),
        (3 * math.pi / 2, -1.0),
        (2 * math.pi, 0.0),
    ])
    def test_sin_valid_inputs(self, x, expected):
        """Test sin with valid radian inputs."""
        result = ScientificOperations.sin(x)
        assert math.isclose(result, expected, abs_tol=1e-10)

    @pytest.mark.parametrize("invalid_x", [True, False])
    def test_sin_rejects_bool(self, invalid_x):
        """Test sin raises TypeError for bool input."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.sin(invalid_x)

    @pytest.mark.parametrize("invalid_x", ["0", "pi/2", None, [0]])
    def test_sin_rejects_non_numeric(self, invalid_x):
        """Test sin raises TypeError for non-numeric input."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.sin(invalid_x)


class TestScientificOperationsCos:
    """Test suite for ScientificOperations.cos() static method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 1.0),
        (math.pi / 2, 0.0),
        (math.pi, -1.0),
        (3 * math.pi / 2, 0.0),
        (2 * math.pi, 1.0),
    ])
    def test_cos_valid_inputs(self, x, expected):
        """Test cos with valid radian inputs."""
        result = ScientificOperations.cos(x)
        assert math.isclose(result, expected, abs_tol=1e-10)

    @pytest.mark.parametrize("invalid_x", [True, False])
    def test_cos_rejects_bool(self, invalid_x):
        """Test cos raises TypeError for bool input."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.cos(invalid_x)

    @pytest.mark.parametrize("invalid_x", ["0", "pi", None, {}])
    def test_cos_rejects_non_numeric(self, invalid_x):
        """Test cos raises TypeError for non-numeric input."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.cos(invalid_x)


class TestScientificOperationsTan:
    """Test suite for ScientificOperations.tan() static method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0.0),
        (math.pi / 4, 1.0),
        (math.pi, 0.0),
    ])
    def test_tan_valid_inputs(self, x, expected):
        """Test tan with valid radian inputs."""
        result = ScientificOperations.tan(x)
        assert math.isclose(result, expected, abs_tol=1e-10)

    @pytest.mark.parametrize("invalid_x", [True, False])
    def test_tan_rejects_bool(self, invalid_x):
        """Test tan raises TypeError for bool input."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.tan(invalid_x)

    @pytest.mark.parametrize("invalid_x", ["pi/4", "1.57", None, set()])
    def test_tan_rejects_non_numeric(self, invalid_x):
        """Test tan raises TypeError for non-numeric input."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.tan(invalid_x)


class TestScientificOperationsCot:
    """Test suite for ScientificOperations.cot() static method."""

    @pytest.mark.parametrize("x,expected", [
        (math.pi / 4, 1.0),
        (math.pi / 6, math.sqrt(3)),
    ])
    def test_cot_valid_inputs(self, x, expected):
        """Test cot with valid radian inputs where sin(x) != 0."""
        result = ScientificOperations.cot(x)
        assert math.isclose(result, expected, abs_tol=1e-10)

    def test_cot_raises_on_sin_zero(self):
        """Test cot raises ValueError when sin(x) == 0."""
        # Only test with exactly 0, as floating point sin(pi) != 0 due to precision
        with pytest.raises(ValueError, match="cotangent is undefined when sin\\(x\\) == 0"):
            ScientificOperations.cot(0)

    @pytest.mark.parametrize("invalid_x", [True, False])
    def test_cot_rejects_bool(self, invalid_x):
        """Test cot raises TypeError for bool input."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.cot(invalid_x)

    @pytest.mark.parametrize("invalid_x", ["pi/4", "45", None, {}])
    def test_cot_rejects_non_numeric(self, invalid_x):
        """Test cot raises TypeError for non-numeric input."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.cot(invalid_x)


class TestScientificOperationsAsin:
    """Test suite for ScientificOperations.asin() static method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0.0),
        (1.0, math.pi / 2),
        (-1.0, -math.pi / 2),
        (0.5, math.asin(0.5)),
    ])
    def test_asin_valid_inputs(self, x, expected):
        """Test asin with valid inputs in [-1, 1]."""
        result = ScientificOperations.asin(x)
        assert math.isclose(result, expected, abs_tol=1e-10)

    @pytest.mark.parametrize("invalid_x", [2.0, -2.0, 1.5, -1.1])
    def test_asin_raises_on_out_of_range(self, invalid_x):
        """Test asin raises ValueError for input outside [-1, 1]."""
        with pytest.raises(ValueError, match="x must be in the range \\[-1, 1\\] for asin"):
            ScientificOperations.asin(invalid_x)

    @pytest.mark.parametrize("invalid_x", [True, False])
    def test_asin_rejects_bool(self, invalid_x):
        """Test asin raises TypeError for bool input."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.asin(invalid_x)

    @pytest.mark.parametrize("invalid_x", ["0.5", "asin(0.5)", None, [0.5]])
    def test_asin_rejects_non_numeric(self, invalid_x):
        """Test asin raises TypeError for non-numeric input."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.asin(invalid_x)


class TestScientificOperationsAcos:
    """Test suite for ScientificOperations.acos() static method."""

    @pytest.mark.parametrize("x,expected", [
        (1.0, 0.0),
        (0, math.pi / 2),
        (-1.0, math.pi),
        (0.5, math.acos(0.5)),
    ])
    def test_acos_valid_inputs(self, x, expected):
        """Test acos with valid inputs in [-1, 1]."""
        result = ScientificOperations.acos(x)
        assert math.isclose(result, expected, abs_tol=1e-10)

    @pytest.mark.parametrize("invalid_x", [2.0, -2.0, 1.5, -1.1])
    def test_acos_raises_on_out_of_range(self, invalid_x):
        """Test acos raises ValueError for input outside [-1, 1]."""
        with pytest.raises(ValueError, match="x must be in the range \\[-1, 1\\] for acos"):
            ScientificOperations.acos(invalid_x)

    @pytest.mark.parametrize("invalid_x", [True, False])
    def test_acos_rejects_bool(self, invalid_x):
        """Test acos raises TypeError for bool input."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.acos(invalid_x)

    @pytest.mark.parametrize("invalid_x", ["1.0", "acos(0.5)", None, (0, 1)])
    def test_acos_rejects_non_numeric(self, invalid_x):
        """Test acos raises TypeError for non-numeric input."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            ScientificOperations.acos(invalid_x)


class TestCalculatorTrigonometric:
    """Test suite for Calculator delegation of trigonometric operations."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance."""
        return Calculator()

    def test_calculator_sin_delegation(self, calculator):
        """Test Calculator.sin() delegates correctly to ScientificOperations."""
        result = calculator.sin(0)
        assert result == 0.0

    def test_calculator_cos_delegation(self, calculator):
        """Test Calculator.cos() delegates correctly to ScientificOperations."""
        result = calculator.cos(0)
        assert result == 1.0

    def test_calculator_tan_delegation(self, calculator):
        """Test Calculator.tan() delegates correctly to ScientificOperations."""
        result = calculator.tan(0)
        assert result == 0.0

    def test_calculator_cot_delegation(self, calculator):
        """Test Calculator.cot() delegates correctly to ScientificOperations."""
        result = calculator.cot(math.pi / 4)
        assert math.isclose(result, 1.0, abs_tol=1e-10)

    def test_calculator_asin_delegation(self, calculator):
        """Test Calculator.asin() delegates correctly to ScientificOperations."""
        result = calculator.asin(0)
        assert result == 0.0

    def test_calculator_acos_delegation(self, calculator):
        """Test Calculator.acos() delegates correctly to ScientificOperations."""
        result = calculator.acos(1.0)
        assert result == 0.0

    def test_calculator_sin_error_handling(self, calculator):
        """Test Calculator.sin() raises TypeError for bool."""
        with pytest.raises(TypeError, match="x must be an int or float"):
            calculator.sin(True)

    def test_calculator_cot_error_handling(self, calculator):
        """Test Calculator.cot() raises ValueError when appropriate."""
        with pytest.raises(ValueError, match="cotangent is undefined"):
            calculator.cot(0)

    def test_calculator_asin_error_handling(self, calculator):
        """Test Calculator.asin() raises ValueError for out-of-range."""
        with pytest.raises(ValueError, match="x must be in the range"):
            calculator.asin(2.0)
