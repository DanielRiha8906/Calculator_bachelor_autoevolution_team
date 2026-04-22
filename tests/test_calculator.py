import pytest
import math
from src import Calculator


@pytest.fixture
def calculator():
    """Fixture providing a fresh Calculator instance for tests."""
    return Calculator()


class TestDivision:
    """Tests for the divide method with valid and invalid inputs."""

    def test_divide_positive_numbers(self, calculator):
        """Test division with positive integers."""
        assert calculator.divide(10, 2) == 5

    def test_divide_with_floats(self, calculator):
        """Test division with floating point numbers."""
        assert calculator.divide(7.5, 2.5) == 3.0

    def test_divide_negative_numbers(self, calculator):
        """Test division with negative numbers."""
        assert calculator.divide(-10, 2) == -5
        assert calculator.divide(10, -2) == -5

    def test_divide_by_zero_raises_exception(self, calculator):
        """Test that division by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)

    def test_divide_zero_by_nonzero(self, calculator):
        """Test dividing zero by a nonzero number returns zero."""
        assert calculator.divide(0, 5) == 0

    @pytest.mark.parametrize("invalid_a,invalid_b", [
        ("10", 2),       # string as dividend
        (10, "2"),       # string as divisor
        (None, 5),       # None as dividend
        (5, None),       # None as divisor
        ([10], 2),       # list as dividend
        (10, [2]),       # list as divisor
    ])
    def test_divide_non_numeric_inputs_raise_typeerror(self, calculator, invalid_a, invalid_b):
        """Test that non-numeric inputs (string, None, list) raise TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(invalid_a, invalid_b)

    def test_divide_result_precision(self, calculator):
        """Test division result with expected precision."""
        result = calculator.divide(10, 3)
        assert abs(result - 3.333333333333333) < 1e-10

    def test_divide_large_numbers(self, calculator):
        """Test division with very large numbers."""
        assert calculator.divide(10**15, 10**10) == 10**5

    def test_divide_very_small_numbers(self, calculator):
        """Test division with very small numbers."""
        result = calculator.divide(1e-10, 1e-5)
        assert abs(result - 1e-5) < 1e-15


class TestAddition:
    """Tests for the add method with various inputs."""

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
    def test_add_various_numbers(self, calculator, a, b, expected):
        """Test addition with positive, negative, zero, and floating point numbers."""
        assert calculator.add(a, b) == expected

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
    def test_add_non_numeric_inputs_raise_typeerror(self, calculator, invalid_a, invalid_b):
        """Test that non-numeric inputs raise TypeError."""
        with pytest.raises(TypeError):
            calculator.add(invalid_a, invalid_b)


class TestSubtraction:
    """Tests for the subtract method with various inputs."""

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
    def test_subtract_various_numbers(self, calculator, a, b, expected):
        """Test subtraction with positive, negative, zero, and floating point numbers."""
        assert calculator.subtract(a, b) == expected

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
    def test_subtract_non_numeric_inputs_raise_typeerror(self, calculator, invalid_a, invalid_b):
        """Test that non-numeric inputs raise TypeError."""
        with pytest.raises(TypeError):
            calculator.subtract(invalid_a, invalid_b)


class TestMultiplication:
    """Tests for the multiply method with various inputs."""

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
    def test_multiply_various_numbers(self, calculator, a, b, expected):
        """Test multiplication with positive, negative, zero, and floating point numbers."""
        assert calculator.multiply(a, b) == expected

    @pytest.mark.parametrize("invalid_a,invalid_b", [
        (None, 5),
        (5, None),
        ({}, 5),
        (5, {}),
    ])
    def test_multiply_non_numeric_inputs_raise_typeerror(self, calculator, invalid_a, invalid_b):
        """Test that unsupported types (None, dict) raise TypeError."""
        with pytest.raises(TypeError):
            calculator.multiply(invalid_a, invalid_b)

    @pytest.mark.parametrize("a,b,expected", [
        ("2", 3, "222"),
        ([2], 3, [2, 2, 2]),
    ])
    def test_multiply_with_strings_and_lists(self, calculator, a, b, expected):
        """Test that multiply with strings/lists works due to Python's * operator behavior."""
        assert calculator.multiply(a, b) == expected


class TestFactorial:
    """Tests for the factorial method with valid and invalid inputs."""

    @pytest.mark.parametrize("n,expected", [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (5, 120),
        (10, 3628800),
        (20, 2432902008176640000),
        (100, 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000),
    ])
    def test_factorial_valid_integers(self, calculator, n, expected):
        """Test factorial with valid non-negative integers."""
        assert calculator.factorial(n) == expected

    @pytest.mark.parametrize("n", [
        -1,
        -5,
        -100,
    ])
    def test_factorial_negative_integers_raise_valueerror(self, calculator, n):
        """Test that negative integers raise ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(n)

    @pytest.mark.parametrize("n", [
        3.0,
        2.5,
        "5",
        None,
        [],
        {},
        True,
        False,
    ])
    def test_factorial_non_integer_types_raise_typeerror(self, calculator, n):
        """Test that non-integer types raise TypeError."""
        with pytest.raises(TypeError):
            calculator.factorial(n)


class TestSquare:
    """Tests for the square method with various inputs."""

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
    def test_square_various_numbers(self, calculator, x, expected):
        """Test squaring with positive, negative, zero, and floating point numbers."""
        result = calculator.square(x)
        if isinstance(expected, float) and expected != int(expected):
            assert result == pytest.approx(expected)
        else:
            assert result == expected

    def test_square_result_correctness(self, calculator):
        """Test that square result equals x * x."""
        x_values = [0, 1, 2, -3, 4.5, -2.5, 100, 0.1]
        for x in x_values:
            assert calculator.square(x) == x * x


class TestCube:
    """Tests for the cube method with various inputs."""

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
    def test_cube_various_numbers(self, calculator, x, expected):
        """Test cubing with positive, negative, zero, and floating point numbers."""
        result = calculator.cube(x)
        if isinstance(expected, float):
            assert result == pytest.approx(expected)
        else:
            assert result == expected

    def test_cube_negative_sign_preservation(self, calculator):
        """Test that cube preserves the sign of negative numbers."""
        assert calculator.cube(-2) == -8
        assert calculator.cube(-5) == -125
        assert calculator.cube(-0.5) < 0

    def test_cube_result_correctness(self, calculator):
        """Test that cube result equals x * x * x."""
        x_values = [0, 1, 2, -3, 4.5, -2.5, 100, -10]
        for x in x_values:
            assert calculator.cube(x) == pytest.approx(x * x * x)


class TestSquareRoot:
    """Tests for the square_root method with valid and invalid inputs."""

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
    def test_square_root_valid_inputs(self, calculator, x, expected):
        """Test square root with non-negative inputs."""
        result = calculator.square_root(x)
        assert result == pytest.approx(expected)

    def test_square_root_perfect_squares(self, calculator):
        """Test square root of perfect squares."""
        for i in range(0, 11):
            assert calculator.square_root(i * i) == pytest.approx(i)

    def test_square_root_large_perfect_squares(self, calculator):
        """Test square root with large perfect squares."""
        assert calculator.square_root(10000) == 100
        assert calculator.square_root(1e12) == 1e6

    @pytest.mark.parametrize("x", [
        -1,
        -0.5,
        -100,
        -1e-10,
    ])
    def test_square_root_negative_raises_valueerror(self, calculator, x):
        """Test that square root of negative numbers raises ValueError."""
        with pytest.raises(ValueError):
            calculator.square_root(x)


class TestCubeRoot:
    """Tests for the cube_root method with various inputs."""

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
    def test_cube_root_various_numbers(self, calculator, x, expected):
        """Test cube root with positive, negative, zero, and floating point numbers."""
        result = calculator.cube_root(x)
        assert result == pytest.approx(expected, rel=1e-10)

    def test_cube_root_negative_sign_preservation(self, calculator):
        """Test that cube root preserves sign for negative numbers."""
        assert calculator.cube_root(-8) == pytest.approx(-2)
        assert calculator.cube_root(-27) < 0
        assert calculator.cube_root(8) > 0

    def test_cube_root_result_correctness(self, calculator):
        """Test that cbrt(x)³ approximately equals x."""
        x_values = [0, 1, 8, 27, -8, -27, 2.5, -2.5, 100, -100]
        for x in x_values:
            cbrt_x = calculator.cube_root(x)
            assert cbrt_x ** 3 == pytest.approx(x, rel=1e-10)

    def test_cube_root_large_numbers(self, calculator):
        """Test cube root with large numbers."""
        assert calculator.cube_root(1e15) == pytest.approx(1e5, rel=1e-10)
        assert calculator.cube_root(-1e15) == pytest.approx(-1e5, rel=1e-10)


class TestPower:
    """Tests for the power method with various base and exponent combinations."""

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
    def test_power_various_bases_and_exponents(self, calculator, base, exponent, expected):
        """Test power function with positive, negative, zero, and fractional exponents."""
        result = calculator.power(base, exponent)
        assert result == pytest.approx(expected, rel=1e-10)

    def test_power_any_base_to_zero_equals_one(self, calculator):
        """Test that any base to power 0 equals 1."""
        bases = [0, 1, 2, 5, 10, -2, -5, 0.5, 1.5, -3.5]
        for base in bases:
            # 0^0 is undefined/special case in Python, skip it
            if base != 0:
                assert calculator.power(base, 0) == pytest.approx(1)

    def test_power_zero_base_positive_exponent(self, calculator):
        """Test that 0 raised to positive power equals 0."""
        for exp in [0.5, 1, 2, 5, 10]:
            assert calculator.power(0, exp) == pytest.approx(0)

    def test_power_fractional_exponents(self, calculator):
        """Test power with fractional exponents (square roots, cube roots, etc)."""
        assert calculator.power(4, 0.5) == pytest.approx(2)
        assert calculator.power(8, 1/3) == pytest.approx(2, rel=1e-10)
        assert calculator.power(16, 0.25) == pytest.approx(2, rel=1e-10)

    def test_power_negative_exponents(self, calculator):
        """Test power with negative exponents."""
        assert calculator.power(2, -1) == pytest.approx(0.5)
        assert calculator.power(10, -2) == pytest.approx(0.01)
        assert calculator.power(2, -3) == pytest.approx(0.125)

    def test_power_negative_base_odd_exponent(self, calculator):
        """Test negative base with odd exponent preserves sign."""
        assert calculator.power(-2, 3) == pytest.approx(-8)
        assert calculator.power(-3, 1) == pytest.approx(-3)


class TestNaturalLog:
    """Tests for the natural_log method with valid and invalid inputs."""

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
    def test_natural_log_valid_inputs(self, calculator, x, expected):
        """Test natural log with valid positive inputs."""
        result = calculator.natural_log(x)
        assert result == pytest.approx(expected, rel=1e-8)

    def test_natural_log_one_equals_zero(self, calculator):
        """Test that ln(1) = 0."""
        assert calculator.natural_log(1) == pytest.approx(0)

    def test_natural_log_e_equals_one(self, calculator):
        """Test that ln(e) ≈ 1."""
        assert calculator.natural_log(math.e) == pytest.approx(1)

    def test_natural_log_large_values(self, calculator):
        """Test natural log with large values."""
        assert calculator.natural_log(1e10) == pytest.approx(23.025850929940457, rel=1e-10)
        assert calculator.natural_log(1e100) == pytest.approx(230.25850929940457, rel=1e-10)

    def test_natural_log_small_positive_values(self, calculator):
        """Test natural log with very small positive values."""
        result = calculator.natural_log(1e-10)
        assert result == pytest.approx(-23.025850929940457, rel=1e-10)

    @pytest.mark.parametrize("x", [
        0,
        -1,
        -0.5,
        -100,
    ])
    def test_natural_log_non_positive_raises_valueerror(self, calculator, x):
        """Test that natural log of non-positive numbers raises ValueError."""
        with pytest.raises(ValueError):
            calculator.natural_log(x)


class TestLogBase10:
    """Tests for the log_base_10 method with valid and invalid inputs."""

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
    def test_log_base_10_valid_inputs(self, calculator, x, expected):
        """Test base-10 log with valid positive inputs."""
        result = calculator.log_base_10(x)
        assert result == pytest.approx(expected, rel=1e-8)

    def test_log_base_10_one_equals_zero(self, calculator):
        """Test that log₁₀(1) = 0."""
        assert calculator.log_base_10(1) == pytest.approx(0)

    def test_log_base_10_ten_equals_one(self, calculator):
        """Test that log₁₀(10) = 1."""
        assert calculator.log_base_10(10) == pytest.approx(1)

    def test_log_base_10_powers_of_ten(self, calculator):
        """Test log₁₀ with powers of 10."""
        for i in range(-3, 4):
            expected = i
            assert calculator.log_base_10(10 ** i) == pytest.approx(expected)

    def test_log_base_10_fractional_values(self, calculator):
        """Test log₁₀ with values between 0 and 1."""
        assert calculator.log_base_10(0.1) == pytest.approx(-1)
        assert calculator.log_base_10(0.01) == pytest.approx(-2)
        assert calculator.log_base_10(0.001) == pytest.approx(-3)

    def test_log_base_10_precision(self, calculator):
        """Test log₁₀ result precision."""
        result = calculator.log_base_10(2)
        expected = math.log10(2)
        assert result == pytest.approx(expected)

    @pytest.mark.parametrize("x", [
        0,
        -1,
        -0.5,
        -100,
    ])
    def test_log_base_10_non_positive_raises_valueerror(self, calculator, x):
        """Test that log₁₀ of non-positive numbers raises ValueError."""
        with pytest.raises(ValueError):
            calculator.log_base_10(x)