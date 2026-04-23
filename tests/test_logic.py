"""test_logic.py — comprehensive unit tests for CalculatorEngine.

Tests cover:
- All 12 operation methods (add, subtract, multiply, divide, factorial, square,
  cube, square_root, cube_root, power, natural_log, log_base_10) with valid inputs
- History tracking with correct keys (operand1, operator, operand2, result)
- Unary operations record None as operand2
- Exception handling for invalid inputs (TypeError, ValueError, ZeroDivisionError)
- History isolation: Calculator.get_history() correctly proxies from CalculatorEngine
- Import path: from src.logic import CalculatorEngine works
"""

import pytest
import math
from src.logic import CalculatorEngine


@pytest.fixture
def engine():
    """Fixture providing a fresh CalculatorEngine instance for tests."""
    return CalculatorEngine()


# =============================================================================
# TestArithmeticOperations - Binary operations
# =============================================================================


class TestAdd:
    """Tests for the add method."""

    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 5),
        (0, 5, 5),
        (5, 0, 5),
        (0, 0, 0),
        (-2, 3, 1),
        (3, -2, 1),
        (-2, -3, -5),
        (1.5, 2.5, 4.0),
        (0.1, 0.2, pytest.approx(0.3)),
        (10**15, 1, 10**15 + 1),
        (1e-10, 1e-10, pytest.approx(2e-10)),
    ])
    def test_add_valid_inputs(self, engine, a, b, expected):
        """Test add with valid numeric inputs."""
        assert engine.add(a, b) == expected

    @pytest.mark.parametrize("invalid_a,invalid_b", [
        ("10", 2),
        (10, "2"),
        (None, 5),
        (5, None),
        ([10], 2),
        (10, [2]),
        ({}, 5),
        (5, {}),
    ])
    def test_add_non_numeric_inputs_raise_typeerror(self, engine, invalid_a, invalid_b):
        """Test that non-numeric inputs raise TypeError."""
        with pytest.raises(TypeError):
            engine.add(invalid_a, invalid_b)


class TestSubtract:
    """Tests for the subtract method."""

    @pytest.mark.parametrize("a,b,expected", [
        (5, 2, 3),
        (2, 5, -3),
        (5, 0, 5),
        (0, 5, -5),
        (0, 0, 0),
        (-2, 3, -5),
        (3, -2, 5),
        (-2, -3, 1),
        (2.5, 1.5, 1.0),
        (0.3, 0.1, pytest.approx(0.2)),
        (10**15, 1, 10**15 - 1),
        (1e-10, 1e-10, pytest.approx(0, abs=1e-15)),
    ])
    def test_subtract_valid_inputs(self, engine, a, b, expected):
        """Test subtract with valid numeric inputs."""
        assert engine.subtract(a, b) == expected

    @pytest.mark.parametrize("invalid_a,invalid_b", [
        ("5", 2),
        (5, "2"),
        (None, 5),
        (5, None),
        ([5], 2),
        (5, [2]),
        ({}, 5),
        (5, {}),
    ])
    def test_subtract_non_numeric_inputs_raise_typeerror(self, engine, invalid_a, invalid_b):
        """Test that non-numeric inputs raise TypeError."""
        with pytest.raises(TypeError):
            engine.subtract(invalid_a, invalid_b)


class TestMultiply:
    """Tests for the multiply method."""

    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 6),
        (5, 0, 0),
        (0, 5, 0),
        (0, 0, 0),
        (-2, 3, -6),
        (3, -2, -6),
        (-2, -3, 6),
        (2.5, 2, 5.0),
        (1.5, 2.5, pytest.approx(3.75)),
        (10**10, 10**10, 10**20),
        (1e-10, 1e5, pytest.approx(1e-5)),
    ])
    def test_multiply_valid_inputs(self, engine, a, b, expected):
        """Test multiply with valid numeric inputs."""
        assert engine.multiply(a, b) == expected

    @pytest.mark.parametrize("invalid_a,invalid_b", [
        (None, 5),
        (5, None),
        ({}, 5),
        (5, {}),
    ])
    def test_multiply_non_numeric_inputs_raise_typeerror(self, engine, invalid_a, invalid_b):
        """Test that unsupported types (None, dict) raise TypeError."""
        with pytest.raises(TypeError):
            engine.multiply(invalid_a, invalid_b)


class TestDivide:
    """Tests for the divide method."""

    @pytest.mark.parametrize("a,b,expected", [
        (10, 2, 5),
        (7.5, 2.5, 3.0),
        (-10, 2, -5),
        (10, -2, -5),
        (0, 5, 0),
        (10, 3, pytest.approx(3.333333333333333, rel=1e-10)),
        (10**15, 10**10, 10**5),
        (1e-10, 1e-5, pytest.approx(1e-5, rel=1e-10)),
    ])
    def test_divide_valid_inputs(self, engine, a, b, expected):
        """Test divide with valid numeric inputs."""
        assert engine.divide(a, b) == expected

    def test_divide_by_zero_raises_zerodivisionerror(self, engine):
        """Test that division by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            engine.divide(10, 0)

    @pytest.mark.parametrize("invalid_a,invalid_b", [
        ("10", 2),
        (10, "2"),
        (None, 5),
        (5, None),
        ([10], 2),
        (10, [2]),
    ])
    def test_divide_non_numeric_inputs_raise_typeerror(self, engine, invalid_a, invalid_b):
        """Test that non-numeric inputs raise TypeError."""
        with pytest.raises(TypeError):
            engine.divide(invalid_a, invalid_b)


# =============================================================================
# TestUnaryOperations - Unary math operations
# =============================================================================


class TestFactorial:
    """Tests for the factorial method."""

    @pytest.mark.parametrize("n,expected", [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (5, 120),
        (10, 3628800),
        (20, 2432902008176640000),
    ])
    def test_factorial_valid_non_negative_integers(self, engine, n, expected):
        """Test factorial with valid non-negative integers."""
        assert engine.factorial(n) == expected

    @pytest.mark.parametrize("n", [-1, -5, -100])
    def test_factorial_negative_integers_raise_valueerror(self, engine, n):
        """Test that negative integers raise ValueError."""
        with pytest.raises(ValueError):
            engine.factorial(n)

    @pytest.mark.parametrize("n", [3.0, 2.5, "5", None, [], {}, True, False])
    def test_factorial_non_integer_types_raise_typeerror(self, engine, n):
        """Test that non-integer types raise TypeError."""
        with pytest.raises(TypeError):
            engine.factorial(n)


class TestSquare:
    """Tests for the square method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (1, 1),
        (2, 4),
        (3, 9),
        (5, 25),
        (-2, 4),
        (-3, 9),
        (-5.5, 30.25),
        (2.5, 6.25),
        (0.5, 0.25),
        (10, 100),
        (100, 10000),
        (1e10, 1e20),
        (1e-5, pytest.approx(1e-10)),
    ])
    def test_square_valid_inputs(self, engine, x, expected):
        """Test square with various numeric inputs."""
        result = engine.square(x)
        if isinstance(expected, float) and expected != int(expected):
            assert result == pytest.approx(expected)
        else:
            assert result == expected

    def test_square_result_equals_x_times_x(self, engine):
        """Test that square result equals x * x."""
        x_values = [0, 1, 2, -3, 4.5, -2.5, 100, 0.1]
        for x in x_values:
            assert engine.square(x) == x * x


class TestCube:
    """Tests for the cube method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (1, 1),
        (2, 8),
        (3, 27),
        (-2, -8),
        (-3, -27),
        (2.5, 15.625),
        (-1.5, -3.375),
        (0.5, 0.125),
        (10, 1000),
        (-10, -1000),
        (1e5, 1e15),
        (-1e5, -1e15),
    ])
    def test_cube_valid_inputs(self, engine, x, expected):
        """Test cube with various numeric inputs."""
        result = engine.cube(x)
        if isinstance(expected, float):
            assert result == pytest.approx(expected)
        else:
            assert result == expected

    def test_cube_negative_sign_preservation(self, engine):
        """Test that cube preserves the sign of negative numbers."""
        assert engine.cube(-2) == -8
        assert engine.cube(-5) == -125
        assert engine.cube(-0.5) < 0

    def test_cube_result_equals_x_times_x_times_x(self, engine):
        """Test that cube result equals x * x * x."""
        x_values = [0, 1, 2, -3, 4.5, -2.5, 100, -10]
        for x in x_values:
            assert engine.cube(x) == pytest.approx(x * x * x)


class TestSquareRoot:
    """Tests for the square_root method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (1, 1),
        (4, 2),
        (9, 3),
        (16, 4),
        (25, 5),
        (100, 10),
        (0.25, 0.5),
        (2.25, 1.5),
        (0.0001, 0.01),
        (1e10, 1e5),
        (2, pytest.approx(1.414213562)),
    ])
    def test_square_root_valid_non_negative_inputs(self, engine, x, expected):
        """Test square_root with non-negative inputs."""
        result = engine.square_root(x)
        assert result == pytest.approx(expected)

    def test_square_root_perfect_squares(self, engine):
        """Test square_root of perfect squares."""
        for i in range(0, 11):
            assert engine.square_root(i * i) == pytest.approx(i)

    def test_square_root_large_perfect_squares(self, engine):
        """Test square_root with large perfect squares."""
        assert engine.square_root(10000) == 100
        assert engine.square_root(1e12) == 1e6

    @pytest.mark.parametrize("x", [-1, -0.5, -100, -1e-10])
    def test_square_root_negative_raises_valueerror(self, engine, x):
        """Test that square_root of negative numbers raises ValueError."""
        with pytest.raises(ValueError):
            engine.square_root(x)


class TestCubeRoot:
    """Tests for the cube_root method."""

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (1, 1),
        (8, 2),
        (27, 3),
        (64, 4),
        (125, 5),
        (-8, -2),
        (-27, -3),
        (-64, -4),
        (-125, -5),
        (0.125, 0.5),
        (-0.125, -0.5),
        (1000, 10),
        (-1000, -10),
    ])
    def test_cube_root_valid_inputs(self, engine, x, expected):
        """Test cube_root with positive, negative, zero, and floating point inputs."""
        result = engine.cube_root(x)
        assert result == pytest.approx(expected, rel=1e-10)

    def test_cube_root_negative_sign_preservation(self, engine):
        """Test that cube_root preserves sign for negative numbers."""
        assert engine.cube_root(-8) == pytest.approx(-2)
        assert engine.cube_root(-27) < 0
        assert engine.cube_root(8) > 0

    def test_cube_root_cubed_equals_original(self, engine):
        """Test that cbrt(x)³ approximately equals x."""
        x_values = [0, 1, 8, 27, -8, -27, 2.5, -2.5, 100, -100]
        for x in x_values:
            cbrt_x = engine.cube_root(x)
            assert cbrt_x ** 3 == pytest.approx(x, rel=1e-10)

    def test_cube_root_large_numbers(self, engine):
        """Test cube_root with large numbers."""
        assert engine.cube_root(1e15) == pytest.approx(1e5, rel=1e-10)
        assert engine.cube_root(-1e15) == pytest.approx(-1e5, rel=1e-10)


class TestPower:
    """Tests for the power method."""

    @pytest.mark.parametrize("base,exponent,expected", [
        (2, 3, 8),
        (2, 0, 1),
        (5, 0, 1),
        (-5, 0, 1),
        (0, 5, 0),
        (0, 0.5, 0),
        (3, 2, 9),
        (10, 2, 100),
        (4, 0.5, 2),
        (9, 0.5, 3),
        (2, -1, 0.5),
        (10, -1, 0.1),
        (2, -2, 0.25),
        (4, 1.5, 8),
        (-2, 3, -8),
        (-2, 4, 16),
        (-3, 2, 9),
        (0.5, 2, 0.25),
        (1.5, 2, 2.25),
        (2, 10, 1024),
    ])
    def test_power_valid_inputs(self, engine, base, exponent, expected):
        """Test power with various base and exponent combinations."""
        result = engine.power(base, exponent)
        assert result == pytest.approx(expected, rel=1e-10)

    def test_power_any_base_to_zero_equals_one(self, engine):
        """Test that any base to power 0 equals 1 (excluding 0^0)."""
        bases = [1, 2, 5, 10, -2, -5, 0.5, 1.5, -3.5]
        for base in bases:
            assert engine.power(base, 0) == pytest.approx(1)

    def test_power_zero_base_positive_exponent(self, engine):
        """Test that 0 raised to positive power equals 0."""
        for exp in [0.5, 1, 2, 5, 10]:
            assert engine.power(0, exp) == pytest.approx(0)

    def test_power_fractional_exponents(self, engine):
        """Test power with fractional exponents (square roots, cube roots, etc)."""
        assert engine.power(4, 0.5) == pytest.approx(2)
        assert engine.power(8, 1/3) == pytest.approx(2, rel=1e-10)
        assert engine.power(16, 0.25) == pytest.approx(2, rel=1e-10)

    def test_power_negative_exponents(self, engine):
        """Test power with negative exponents."""
        assert engine.power(2, -1) == pytest.approx(0.5)
        assert engine.power(10, -2) == pytest.approx(0.01)
        assert engine.power(2, -3) == pytest.approx(0.125)

    def test_power_negative_base_odd_exponent(self, engine):
        """Test negative base with odd exponent preserves sign."""
        assert engine.power(-2, 3) == pytest.approx(-8)
        assert engine.power(-3, 1) == pytest.approx(-3)


class TestNaturalLog:
    """Tests for the natural_log method."""

    @pytest.mark.parametrize("x,expected", [
        (1, 0),
        (math.e, pytest.approx(1)),
        (math.e**2, pytest.approx(2)),
        (10, pytest.approx(2.302585093)),
        (100, pytest.approx(4.605170186)),
        (0.5, pytest.approx(-0.693147181)),
        (0.1, pytest.approx(-2.302585093)),
        (2, pytest.approx(0.693147181)),
    ])
    def test_natural_log_valid_positive_inputs(self, engine, x, expected):
        """Test natural_log with valid positive inputs."""
        result = engine.natural_log(x)
        assert result == pytest.approx(expected, rel=1e-8)

    def test_natural_log_one_equals_zero(self, engine):
        """Test that ln(1) = 0."""
        assert engine.natural_log(1) == pytest.approx(0)

    def test_natural_log_e_equals_one(self, engine):
        """Test that ln(e) ≈ 1."""
        assert engine.natural_log(math.e) == pytest.approx(1)

    def test_natural_log_large_values(self, engine):
        """Test natural_log with large values."""
        assert engine.natural_log(1e10) == pytest.approx(23.025850929940457, rel=1e-10)
        assert engine.natural_log(1e100) == pytest.approx(230.25850929940457, rel=1e-10)

    def test_natural_log_small_positive_values(self, engine):
        """Test natural_log with very small positive values."""
        result = engine.natural_log(1e-10)
        assert result == pytest.approx(-23.025850929940457, rel=1e-10)

    @pytest.mark.parametrize("x", [0, -1, -0.5, -100])
    def test_natural_log_non_positive_raises_valueerror(self, engine, x):
        """Test that natural_log of non-positive numbers raises ValueError."""
        with pytest.raises(ValueError):
            engine.natural_log(x)


class TestLogBase10:
    """Tests for the log_base_10 method."""

    @pytest.mark.parametrize("x,expected", [
        (1, 0),
        (10, 1),
        (100, 2),
        (1000, 3),
        (0.1, -1),
        (0.01, -2),
        (0.001, -3),
        (5, pytest.approx(0.698970004)),
        (2, pytest.approx(0.301029996)),
        (50, pytest.approx(1.698970004)),
    ])
    def test_log_base_10_valid_positive_inputs(self, engine, x, expected):
        """Test log_base_10 with valid positive inputs."""
        result = engine.log_base_10(x)
        assert result == pytest.approx(expected, rel=1e-8)

    def test_log_base_10_one_equals_zero(self, engine):
        """Test that log₁₀(1) = 0."""
        assert engine.log_base_10(1) == pytest.approx(0)

    def test_log_base_10_ten_equals_one(self, engine):
        """Test that log₁₀(10) = 1."""
        assert engine.log_base_10(10) == pytest.approx(1)

    def test_log_base_10_powers_of_ten(self, engine):
        """Test log₁₀ with powers of 10."""
        for i in range(-3, 4):
            expected = i
            assert engine.log_base_10(10 ** i) == pytest.approx(expected)

    def test_log_base_10_fractional_values(self, engine):
        """Test log₁₀ with values between 0 and 1."""
        assert engine.log_base_10(0.1) == pytest.approx(-1)
        assert engine.log_base_10(0.01) == pytest.approx(-2)
        assert engine.log_base_10(0.001) == pytest.approx(-3)

    def test_log_base_10_precision(self, engine):
        """Test log₁₀ result precision."""
        result = engine.log_base_10(2)
        expected = math.log10(2)
        assert result == pytest.approx(expected)

    @pytest.mark.parametrize("x", [0, -1, -0.5, -100])
    def test_log_base_10_non_positive_raises_valueerror(self, engine, x):
        """Test that log₁₀ of non-positive numbers raises ValueError."""
        with pytest.raises(ValueError):
            engine.log_base_10(x)


# =============================================================================
# TestHistoryTracking
# =============================================================================


class TestHistoryTracking:
    """Tests for history recording and retrieval."""

    def test_get_history_returns_list(self, engine):
        """Test that get_history returns a list."""
        history = engine.get_history()
        assert isinstance(history, list)

    def test_get_history_empty_on_new_engine(self, engine):
        """Test that history is empty for a new engine."""
        assert engine.get_history() == []

    def test_single_binary_operation_recorded_in_history(self, engine):
        """Test that a single binary operation is recorded with correct keys."""
        engine.add(2, 3)
        history = engine.get_history()
        assert len(history) == 1
        assert history[0]["operand1"] == 2
        assert history[0]["operator"] == "add"
        assert history[0]["operand2"] == 3
        assert history[0]["result"] == 5

    def test_single_unary_operation_recorded_in_history(self, engine):
        """Test that a single unary operation is recorded with operand2=None."""
        engine.square(4)
        history = engine.get_history()
        assert len(history) == 1
        assert history[0]["operand1"] == 4
        assert history[0]["operator"] == "square"
        assert history[0]["operand2"] is None
        assert history[0]["result"] == 16

    def test_multiple_operations_recorded_in_order(self, engine):
        """Test that multiple operations are recorded in chronological order."""
        engine.add(2, 3)
        engine.multiply(5, 2)
        engine.subtract(10, 3)
        history = engine.get_history()
        assert len(history) == 3
        assert history[0]["operator"] == "add"
        assert history[1]["operator"] == "multiply"
        assert history[2]["operator"] == "subtract"

    def test_history_records_all_binary_operations(self, engine):
        """Test that all binary operations are correctly recorded."""
        engine.add(1, 2)
        engine.subtract(5, 3)
        engine.multiply(4, 5)
        engine.divide(10, 2)
        engine.power(2, 3)
        history = engine.get_history()
        assert len(history) == 5
        operators = [h["operator"] for h in history]
        assert operators == ["add", "subtract", "multiply", "divide", "power"]

    def test_history_records_all_unary_operations(self, engine):
        """Test that all unary operations record operand2 as None."""
        engine.square(2)
        engine.cube(3)
        engine.square_root(4)
        engine.cube_root(8)
        engine.factorial(5)
        engine.natural_log(10)
        engine.log_base_10(100)
        history = engine.get_history()
        assert len(history) == 7
        for record in history:
            assert record["operand2"] is None

    def test_history_with_floats_and_negatives(self, engine):
        """Test that history records floating point and negative operands."""
        engine.add(2.5, -3.5)
        history = engine.get_history()
        assert history[0]["operand1"] == 2.5
        assert history[0]["operand2"] == -3.5
        assert history[0]["result"] == pytest.approx(-1.0)

    def test_history_with_zero_values(self, engine):
        """Test that history correctly records zero values."""
        engine.add(0, 5)
        engine.multiply(3, 0)
        history = engine.get_history()
        assert history[0]["operand1"] == 0
        assert history[1]["operand2"] == 0

    def test_history_isolation_between_engines(self, engine):
        """Test that separate engine instances have isolated histories."""
        engine1 = CalculatorEngine()
        engine2 = CalculatorEngine()
        engine1.add(1, 2)
        engine2.add(10, 20)
        assert len(engine1.get_history()) == 1
        assert len(engine2.get_history()) == 1
        assert engine1.get_history()[0]["result"] == 3
        assert engine2.get_history()[0]["result"] == 30

    def test_factorial_records_in_history(self, engine):
        """Test that factorial is correctly recorded in history."""
        engine.factorial(5)
        history = engine.get_history()
        assert len(history) == 1
        assert history[0]["operand1"] == 5
        assert history[0]["operator"] == "factorial"
        assert history[0]["operand2"] is None
        assert history[0]["result"] == 120

    def test_square_root_records_in_history(self, engine):
        """Test that square_root is correctly recorded in history."""
        engine.square_root(16)
        history = engine.get_history()
        assert len(history) == 1
        assert history[0]["operand1"] == 16
        assert history[0]["operator"] == "square_root"
        assert history[0]["operand2"] is None
        assert history[0]["result"] == 4

    def test_natural_log_records_in_history(self, engine):
        """Test that natural_log is correctly recorded in history."""
        engine.natural_log(math.e)
        history = engine.get_history()
        assert len(history) == 1
        assert history[0]["operand1"] == math.e
        assert history[0]["operator"] == "natural_log"
        assert history[0]["operand2"] is None
        assert history[0]["result"] == pytest.approx(1)

    def test_log_base_10_records_in_history(self, engine):
        """Test that log_base_10 is correctly recorded in history."""
        engine.log_base_10(100)
        history = engine.get_history()
        assert len(history) == 1
        assert history[0]["operand1"] == 100
        assert history[0]["operator"] == "log_base_10"
        assert history[0]["operand2"] is None
        assert history[0]["result"] == 2

    def test_history_is_not_recorded_on_exception(self, engine):
        """Test that history is not recorded when operation raises exception."""
        # This test checks behavior: exceptions should be raised before recording
        with pytest.raises(ValueError):
            engine.square_root(-1)
        history = engine.get_history()
        assert len(history) == 0

    def test_history_not_recorded_for_type_errors(self, engine):
        """Test that history is not recorded when TypeError is raised."""
        with pytest.raises(TypeError):
            engine.add("not_a_number", 5)
        history = engine.get_history()
        assert len(history) == 0

    def test_divide_by_zero_not_recorded_in_history(self, engine):
        """Test that failed divide by zero is not recorded in history."""
        with pytest.raises(ZeroDivisionError):
            engine.divide(10, 0)
        history = engine.get_history()
        assert len(history) == 0


# =============================================================================
# TestCalculatorProxyToEngine
# =============================================================================


class TestCalculatorProxyToEngine:
    """Tests for Calculator class proxying to CalculatorEngine."""

    def test_calculator_get_history_proxies_to_engine(self):
        """Test that Calculator.get_history() correctly proxies from CalculatorEngine."""
        from src import Calculator
        calc = Calculator()
        calc.add(2, 3)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0]["operand1"] == 2
        assert history[0]["operator"] == "add"
        assert history[0]["operand2"] == 3
        assert history[0]["result"] == 5

    def test_calculator_operations_update_engine_history(self):
        """Test that Calculator operations update the underlying engine's history."""
        from src import Calculator
        calc = Calculator()
        calc.add(1, 2)
        calc.multiply(3, 4)
        calc.square(5)
        history = calc.get_history()
        assert len(history) == 3
        operators = [h["operator"] for h in history]
        assert operators == ["add", "multiply", "square"]

    def test_calculator_history_isolation(self):
        """Test that separate Calculator instances have isolated histories."""
        from src import Calculator
        calc1 = Calculator()
        calc2 = Calculator()
        calc1.add(10, 20)
        calc2.subtract(5, 3)
        assert len(calc1.get_history()) == 1
        assert len(calc2.get_history()) == 1
        assert calc1.get_history()[0]["operator"] == "add"
        assert calc2.get_history()[0]["operator"] == "subtract"


# =============================================================================
# TestImportPath
# =============================================================================


class TestImportPath:
    """Test that CalculatorEngine can be imported from src.logic."""

    def test_import_calculatorengine_from_src_logic(self):
        """Test that from src.logic import CalculatorEngine works."""
        # This test will pass if the import at the top of this file succeeded
        assert CalculatorEngine is not None
        engine = CalculatorEngine()
        assert hasattr(engine, "add")
        assert hasattr(engine, "divide")
        assert hasattr(engine, "get_history")


# =============================================================================
# TestModeParameter
# =============================================================================


class TestModeParameter:
    """Tests for CalculatorEngine mode parameter."""

    def test_engine_initializes_with_default_mode(self):
        """Test that CalculatorEngine() uses 'advanced' as default mode."""
        engine = CalculatorEngine()
        assert engine._mode == "advanced"

    def test_engine_initializes_with_explicit_mode(self):
        """Test that CalculatorEngine(mode='basic') works."""
        engine = CalculatorEngine(mode="basic")
        assert engine._mode == "basic"

    def test_engine_accepts_mode_parameter(self):
        """Test that CalculatorEngine accepts mode parameter at construction."""
        engine = CalculatorEngine(mode="advanced")
        assert engine._mode == "advanced"

    def test_backward_compatibility_engine_no_args(self):
        """Test that CalculatorEngine() with no args works identically to before."""
        engine = CalculatorEngine()
        result = engine.add(2, 3)
        assert result == 5
        assert engine.multiply(4, 5) == 20
        assert engine.divide(10, 2) == 5.0

    def test_backward_compatibility_all_basic_ops_available(self):
        """Test that all basic operations are available regardless of mode."""
        engine = CalculatorEngine(mode="basic")
        assert engine.add(1, 2) == 3
        assert engine.subtract(5, 2) == 3
        assert engine.multiply(3, 4) == 12
        assert engine.divide(10, 2) == 5.0

    def test_advanced_operations_not_available_in_basic_mode(self):
        """Test that advanced operations are NOT available in basic mode."""
        engine = CalculatorEngine(mode="basic")
        # Advanced operations should raise ValueError when accessed
        with pytest.raises(ValueError):
            engine.factorial(5)
        with pytest.raises(ValueError):
            engine.square(3)

    def test_history_recorded_with_mode_parameter(self):
        """Test that history is still recorded when mode is specified."""
        engine = CalculatorEngine(mode="basic")
        engine.add(1, 2)
        engine.multiply(3, 4)
        history = engine.get_history()
        assert len(history) == 2
        assert history[0]["operator"] == "add"
        assert history[1]["operator"] == "multiply"

    def test_mode_parameter_affects_available_operations(self):
        """Test that mode parameter controls which operations are available."""
        engine_basic = CalculatorEngine(mode="basic")
        engine_advanced = CalculatorEngine(mode="advanced")
        engine_scientific = CalculatorEngine(mode="scientific")

        # All modes have basic operations
        assert engine_basic.add(5, 3) == engine_advanced.add(5, 3) == engine_scientific.add(5, 3) == 8

        # Only advanced and scientific have factorial
        assert engine_advanced.factorial(4) == 24
        assert engine_scientific.factorial(4) == 24
        with pytest.raises(ValueError):
            engine_basic.factorial(4)

        # Only scientific has sin
        assert engine_scientific.sin(0) == 0.0
        with pytest.raises(ValueError):
            engine_basic.sin(0)
        with pytest.raises(ValueError):
            engine_advanced.sin(0)
