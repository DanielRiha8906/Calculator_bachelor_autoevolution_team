"""Comprehensive tests for the basic operations module.

Tests cover:
- 12 concrete operation classes: names, operand counts, execute() behavior
- register_basic_operations() function
- register_scientific_operations() function (stub)
"""

import pytest
import math
from src.operations.basic import (
    Add, Subtract, Multiply, Divide, Factorial, Square, Cube,
    SquareRoot, CubeRoot, Power, Log10, NaturalLog,
    register_basic_operations,
)
from src.operations.scientific import register_scientific_operations
from src.operations.base import OperationRegistry


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def registry():
    """Provides a fresh OperationRegistry instance for each test."""
    return OperationRegistry()


# ============================================================================
# TEST BASIC OPERATION NAMES
# ============================================================================


class TestBasicOperationNames:
    """Verify that each operation has the correct name."""

    def test_add_name(self):
        """Test that Add operation has name 'add'."""
        assert Add().name() == "add"

    def test_subtract_name(self):
        """Test that Subtract operation has name 'subtract'."""
        assert Subtract().name() == "subtract"

    def test_multiply_name(self):
        """Test that Multiply operation has name 'multiply'."""
        assert Multiply().name() == "multiply"

    def test_divide_name(self):
        """Test that Divide operation has name 'divide'."""
        assert Divide().name() == "divide"

    def test_factorial_name(self):
        """Test that Factorial operation has name 'factorial'."""
        assert Factorial().name() == "factorial"

    def test_square_name(self):
        """Test that Square operation has name 'square'."""
        assert Square().name() == "square"

    def test_cube_name(self):
        """Test that Cube operation has name 'cube'."""
        assert Cube().name() == "cube"

    def test_square_root_name(self):
        """Test that SquareRoot operation has name 'square_root'."""
        assert SquareRoot().name() == "square_root"

    def test_cube_root_name(self):
        """Test that CubeRoot operation has name 'cube_root'."""
        assert CubeRoot().name() == "cube_root"

    def test_power_name(self):
        """Test that Power operation has name 'power'."""
        assert Power().name() == "power"

    def test_log10_name(self):
        """Test that Log10 operation has name 'log10'."""
        assert Log10().name() == "log10"

    def test_natural_log_name(self):
        """Test that NaturalLog operation has name 'natural_log'."""
        assert NaturalLog().name() == "natural_log"


# ============================================================================
# TEST BASIC OPERATION OPERAND COUNTS
# ============================================================================


class TestBasicOperationOperandCounts:
    """Verify that each operation declares the correct operand count."""

    # Binary operations (2 operands)

    def test_add_operand_count(self):
        """Test that Add has operand_count 2."""
        assert Add().operand_count() == 2

    def test_subtract_operand_count(self):
        """Test that Subtract has operand_count 2."""
        assert Subtract().operand_count() == 2

    def test_multiply_operand_count(self):
        """Test that Multiply has operand_count 2."""
        assert Multiply().operand_count() == 2

    def test_divide_operand_count(self):
        """Test that Divide has operand_count 2."""
        assert Divide().operand_count() == 2

    def test_power_operand_count(self):
        """Test that Power has operand_count 2."""
        assert Power().operand_count() == 2

    # Unary operations (1 operand)

    def test_factorial_operand_count(self):
        """Test that Factorial has operand_count 1."""
        assert Factorial().operand_count() == 1

    def test_square_operand_count(self):
        """Test that Square has operand_count 1."""
        assert Square().operand_count() == 1

    def test_cube_operand_count(self):
        """Test that Cube has operand_count 1."""
        assert Cube().operand_count() == 1

    def test_square_root_operand_count(self):
        """Test that SquareRoot has operand_count 1."""
        assert SquareRoot().operand_count() == 1

    def test_cube_root_operand_count(self):
        """Test that CubeRoot has operand_count 1."""
        assert CubeRoot().operand_count() == 1

    def test_log10_operand_count(self):
        """Test that Log10 has operand_count 1."""
        assert Log10().operand_count() == 1

    def test_natural_log_operand_count(self):
        """Test that NaturalLog has operand_count 1."""
        assert NaturalLog().operand_count() == 1


# ============================================================================
# TEST BASIC OPERATION EXECUTE
# ============================================================================


class TestBasicOperationExecute:
    """Verify that each operation computes results correctly."""

    # Addition tests

    def test_add_two_integers(self):
        """Test addition of two integers."""
        assert Add().execute(3, 4) == 7.0

    def test_add_two_floats(self):
        """Test addition of two floats."""
        assert Add().execute(3.5, 2.5) == pytest.approx(6.0)

    def test_add_negative_numbers(self):
        """Test addition with negative operands."""
        assert Add().execute(-5, 3) == -2.0

    def test_add_zero(self):
        """Test addition involving zero."""
        assert Add().execute(5, 0) == 5.0

    # Subtraction tests

    def test_subtract_two_integers(self):
        """Test subtraction of two integers."""
        assert Subtract().execute(10, 3) == 7.0

    def test_subtract_two_floats(self):
        """Test subtraction of two floats."""
        assert Subtract().execute(10.5, 3.2) == pytest.approx(7.3)

    def test_subtract_negative_result(self):
        """Test subtraction resulting in negative."""
        assert Subtract().execute(3, 10) == -7.0

    def test_subtract_zero(self):
        """Test subtraction of zero."""
        assert Subtract().execute(5, 0) == 5.0

    # Multiplication tests

    def test_multiply_two_integers(self):
        """Test multiplication of two integers."""
        assert Multiply().execute(3, 4) == 12.0

    def test_multiply_two_floats(self):
        """Test multiplication of two floats."""
        assert Multiply().execute(2.5, 3.0) == pytest.approx(7.5)

    def test_multiply_by_zero(self):
        """Test multiplication by zero."""
        assert Multiply().execute(100, 0) == 0.0

    def test_multiply_negative_numbers(self):
        """Test multiplication with negative operands."""
        assert Multiply().execute(-3, 4) == -12.0
        assert Multiply().execute(-3, -4) == 12.0

    # Division tests

    def test_divide_two_integers(self):
        """Test division of two integers."""
        assert Divide().execute(10, 2) == 5.0

    def test_divide_two_floats(self):
        """Test division of two floats."""
        assert Divide().execute(10.0, 4.0) == pytest.approx(2.5)

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            Divide().execute(5, 0)

    def test_divide_negative_numbers(self):
        """Test division with negative operands."""
        assert Divide().execute(-10, 2) == -5.0
        assert Divide().execute(-10, -2) == 5.0

    # Factorial tests

    def test_factorial_zero(self):
        """Test factorial of 0."""
        assert Factorial().execute(0) == 1.0

    def test_factorial_five(self):
        """Test factorial of 5."""
        assert Factorial().execute(5) == 120.0

    def test_factorial_one(self):
        """Test factorial of 1."""
        assert Factorial().execute(1) == 1.0

    def test_factorial_ten(self):
        """Test factorial of 10."""
        assert Factorial().execute(10) == 3628800.0

    def test_factorial_negative_raises_error(self):
        """Test that factorial of negative number raises ValueError."""
        with pytest.raises(ValueError):
            Factorial().execute(-1)

    # Square tests

    def test_square_positive_integer(self):
        """Test squaring a positive integer."""
        assert Square().execute(4) == 16.0

    def test_square_positive_float(self):
        """Test squaring a positive float."""
        assert Square().execute(2.5) == pytest.approx(6.25)

    def test_square_negative_integer(self):
        """Test squaring a negative integer."""
        assert Square().execute(-5) == 25.0

    def test_square_zero(self):
        """Test squaring zero."""
        assert Square().execute(0) == 0.0

    # Cube tests

    def test_cube_positive_integer(self):
        """Test cubing a positive integer."""
        assert Cube().execute(3) == 27.0

    def test_cube_positive_float(self):
        """Test cubing a positive float."""
        assert Cube().execute(2.0) == pytest.approx(8.0)

    def test_cube_negative_integer(self):
        """Test cubing a negative integer."""
        assert Cube().execute(-2) == -8.0

    def test_cube_zero(self):
        """Test cubing zero."""
        assert Cube().execute(0) == 0.0

    # SquareRoot tests

    def test_square_root_perfect_square(self):
        """Test square root of perfect square."""
        assert SquareRoot().execute(9) == pytest.approx(3.0)

    def test_square_root_perfect_square_float(self):
        """Test square root of perfect square (float)."""
        assert SquareRoot().execute(16.0) == pytest.approx(4.0)

    def test_square_root_non_perfect_square(self):
        """Test square root of non-perfect square."""
        assert SquareRoot().execute(2) == pytest.approx(math.sqrt(2))

    def test_square_root_zero(self):
        """Test square root of zero."""
        assert SquareRoot().execute(0) == 0.0

    def test_square_root_negative_raises_error(self):
        """Test that square root of negative raises ValueError."""
        with pytest.raises(ValueError):
            SquareRoot().execute(-4)

    # CubeRoot tests

    def test_cube_root_perfect_cube(self):
        """Test cube root of perfect cube."""
        assert CubeRoot().execute(27) == pytest.approx(3.0)

    def test_cube_root_perfect_cube_float(self):
        """Test cube root of perfect cube (float)."""
        assert CubeRoot().execute(8.0) == pytest.approx(2.0)

    def test_cube_root_negative_number(self):
        """Test cube root of negative number."""
        assert CubeRoot().execute(-8) == pytest.approx(-2.0)

    def test_cube_root_zero(self):
        """Test cube root of zero."""
        assert CubeRoot().execute(0) == 0.0

    # Power tests

    def test_power_basic(self):
        """Test basic exponentiation."""
        assert Power().execute(2, 10) == pytest.approx(1024.0)

    def test_power_zero_exponent(self):
        """Test raising to the power of zero."""
        assert Power().execute(5, 0) == pytest.approx(1.0)

    def test_power_one_exponent(self):
        """Test raising to the power of one."""
        assert Power().execute(7, 1) == pytest.approx(7.0)

    def test_power_negative_exponent(self):
        """Test raising to a negative exponent."""
        assert Power().execute(2, -1) == pytest.approx(0.5)

    def test_power_fractional_exponent(self):
        """Test raising to a fractional exponent."""
        assert Power().execute(4, 0.5) == pytest.approx(2.0)

    # Log10 tests

    def test_log10_hundred(self):
        """Test log10 of 100."""
        assert Log10().execute(100) == pytest.approx(2.0)

    def test_log10_one(self):
        """Test log10 of 1."""
        assert Log10().execute(1) == pytest.approx(0.0)

    def test_log10_ten(self):
        """Test log10 of 10."""
        assert Log10().execute(10) == pytest.approx(1.0)

    def test_log10_thousand(self):
        """Test log10 of 1000."""
        assert Log10().execute(1000) == pytest.approx(3.0)

    def test_log10_zero_or_negative_raises_error(self):
        """Test that log10 of zero or negative raises ValueError."""
        with pytest.raises(ValueError):
            Log10().execute(0)
        with pytest.raises(ValueError):
            Log10().execute(-5)

    # NaturalLog tests

    def test_natural_log_one(self):
        """Test natural log of 1."""
        assert NaturalLog().execute(1) == pytest.approx(0.0)

    def test_natural_log_e(self):
        """Test natural log of e."""
        assert NaturalLog().execute(math.e) == pytest.approx(1.0)

    def test_natural_log_positive_number(self):
        """Test natural log of positive number."""
        assert NaturalLog().execute(math.e ** 2) == pytest.approx(2.0)

    def test_natural_log_zero_or_negative_raises_error(self):
        """Test that natural log of zero or negative raises ValueError."""
        with pytest.raises(ValueError):
            NaturalLog().execute(0)
        with pytest.raises(ValueError):
            NaturalLog().execute(-5)


# ============================================================================
# TEST REGISTER_BASIC_OPERATIONS
# ============================================================================


class TestRegisterBasicOperations:
    """Test the register_basic_operations function."""

    def test_register_basic_operations_populates_registry(self, registry):
        """Test that register_basic_operations registers all 12 operations."""
        register_basic_operations(registry)
        operations = registry.list_operations()
        assert len(operations) >= 12
        assert "add" in operations
        assert "subtract" in operations
        assert "multiply" in operations
        assert "divide" in operations
        assert "factorial" in operations
        assert "square" in operations
        assert "cube" in operations
        assert "square_root" in operations
        assert "cube_root" in operations
        assert "power" in operations
        assert "log10" in operations
        assert "natural_log" in operations

    def test_all_registered_operations_are_callable(self, registry):
        """Test that each registered operation can be executed."""
        register_basic_operations(registry)

        # Test binary operations
        add_op = registry.get("add")
        assert add_op is not None
        assert add_op.execute(3, 4) == 7.0

        multiply_op = registry.get("multiply")
        assert multiply_op is not None
        assert multiply_op.execute(3, 4) == 12.0

        divide_op = registry.get("divide")
        assert divide_op is not None
        assert divide_op.execute(10, 2) == 5.0

        # Test unary operations
        square_op = registry.get("square")
        assert square_op is not None
        assert square_op.execute(4) == 16.0

        factorial_op = registry.get("factorial")
        assert factorial_op is not None
        assert factorial_op.execute(5) == 120.0

    def test_registered_operations_have_correct_operand_counts(self, registry):
        """Test that registered operations have the correct operand counts."""
        register_basic_operations(registry)

        # Binary
        assert registry.get("add").operand_count() == 2
        assert registry.get("subtract").operand_count() == 2
        assert registry.get("multiply").operand_count() == 2
        assert registry.get("divide").operand_count() == 2
        assert registry.get("power").operand_count() == 2

        # Unary
        assert registry.get("factorial").operand_count() == 1
        assert registry.get("square").operand_count() == 1
        assert registry.get("cube").operand_count() == 1
        assert registry.get("square_root").operand_count() == 1
        assert registry.get("cube_root").operand_count() == 1
        assert registry.get("log10").operand_count() == 1
        assert registry.get("natural_log").operand_count() == 1

    def test_register_basic_operations_multiple_times(self, registry):
        """Test that calling register_basic_operations twice works correctly."""
        register_basic_operations(registry)
        first_list = registry.list_operations()

        register_basic_operations(registry)
        second_list = registry.list_operations()

        # Both calls should result in all 12 operations being present
        assert len(first_list) >= 12
        assert len(second_list) >= 12


# ============================================================================
# TEST REGISTER_SCIENTIFIC_OPERATIONS
# ============================================================================


class TestRegisterScientificOperations:
    """Test the register_scientific_operations function."""

    def test_register_scientific_operations_adds_all_eight_operations(self, registry):
        """Test that register_scientific_operations registers all 8 scientific operations."""
        assert registry.list_operations() == []
        register_scientific_operations(registry)
        operations = registry.list_operations()

        # Check that all 8 operations are registered
        assert len(operations) == 8
        assert "sin" in operations
        assert "cos" in operations
        assert "tan" in operations
        assert "exp" in operations
        assert "log" in operations
        assert "log10" in operations
        assert "sqrt" in operations
        assert "factorial" in operations

    def test_register_scientific_operations_coexists_with_basic(self, registry):
        """Test that scientific operations coexist with basic operations."""
        register_basic_operations(registry)
        basic_ops = set(registry.list_operations())

        register_scientific_operations(registry)
        all_ops = set(registry.list_operations())

        # All basic operations should still be present
        assert basic_ops.issubset(all_ops)

        # Scientific operations should be added (some overlap: factorial, log10)
        scientific_ops = {"sin", "cos", "tan", "exp", "log", "log10", "sqrt", "factorial"}
        assert scientific_ops.issubset(all_ops)

        # Total should be at least 12 (basic) + new scientific ops (sin, cos, tan, exp, log, sqrt)
        # Note: log10 and factorial exist in both, so they are not "new"
        assert len(all_ops) >= 16
