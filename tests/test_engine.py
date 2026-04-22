"""Comprehensive tests for CalculationEngine."""

import pytest
import math
from src.engine import CalculationEngine
from src.calculator import Calculator
from src.operations import OperationRegistry


class TestEngineInitialization:
    """Test suite for CalculationEngine initialization."""

    def test_engine_initializes_with_calculator_and_registry(self):
        """Test that engine initializes correctly with required dependencies."""
        calculator = Calculator()
        registry = OperationRegistry(calculator)
        engine = CalculationEngine(calculator, registry)

        assert engine._calculator is calculator
        assert engine._registry is registry

    def test_engine_stores_references_not_copies(self):
        """Test that engine stores references to the same objects."""
        calculator = Calculator()
        registry = OperationRegistry(calculator)
        engine = CalculationEngine(calculator, registry)

        # Verify the objects are the same instances
        assert engine._calculator is calculator
        assert engine._registry is registry


class TestEngineExecuteOperation:
    """Test suite for CalculationEngine.execute_operation()."""

    @pytest.fixture
    def engine(self):
        """Fixture providing a fully configured CalculationEngine."""
        calculator = Calculator()
        registry = OperationRegistry(calculator)
        return CalculationEngine(calculator, registry)

    # Binary operations - happy path
    @pytest.mark.parametrize("op_key,operands,expected", [
        ("add", [2, 3], 5),
        ("add", [0, 0], 0),
        ("add", [-5, 3], -2),
        ("add", [1.5, 2.5], 4.0),
        ("subtract", [10, 4], 6),
        ("subtract", [5, 5], 0),
        ("subtract", [3, 7], -4),
        ("subtract", [0.5, 0.3], pytest.approx(0.2)),
        ("multiply", [3, 4], 12),
        ("multiply", [0, 100], 0),
        ("multiply", [-2, 5], -10),
        ("multiply", [2.5, 4], 10.0),
        ("divide", [10, 2], 5.0),
        ("divide", [9, 3], 3.0),
        ("divide", [1, 2], 0.5),
        ("divide", [-8, 4], -2.0),
        ("power", [2, 3], 8),
        ("power", [5, 0], 1),
        ("power", [2, -2], 0.25),
        ("power", [0, 5], 0),
    ])
    def test_binary_operations_happy_path(self, engine, op_key, operands, expected):
        """Test all binary operations with valid operands."""
        result = engine.execute_operation(op_key, operands)
        assert result == expected or (isinstance(expected, float) and pytest.approx(result) == expected)

    # Unary operations - happy path
    @pytest.mark.parametrize("op_key,operands,expected", [
        ("factorial", [0], 1),
        ("factorial", [1], 1),
        ("factorial", [5], 120),
        ("factorial", [10], 3628800),
        ("square", [0], 0),
        ("square", [5], 25),
        ("square", [-3], 9),
        ("square", [0.5], 0.25),
        ("cube", [0], 0),
        ("cube", [2], 8),
        ("cube", [-2], -8),
        ("cube", [0.5], 0.125),
        ("square_root", [0], 0),
        ("square_root", [4], 2),
        ("square_root", [9], 3),
        ("square_root", [0.25], 0.5),
        ("cube_root", [0], 0),
        ("cube_root", [8], 2),
        ("cube_root", [-8], -2),
        ("cube_root", [27], 3),
        ("log", [1], 0),
        ("log", [10], 1),
        ("log", [100], 2),
        ("log", [0.1], -1),
        ("ln", [1], 0),
        ("ln", [math.e], pytest.approx(1, abs=1e-10)),
    ])
    def test_unary_operations_happy_path(self, engine, op_key, operands, expected):
        """Test all unary operations with valid operands."""
        result = engine.execute_operation(op_key, operands)
        assert result == expected or pytest.approx(result) == expected

    # Edge cases for divide
    def test_divide_by_zero_raises_error(self, engine):
        """Test that divide by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            engine.execute_operation("divide", [5, 0])

    def test_divide_by_very_small_number(self, engine):
        """Test divide with very small divisor (not zero)."""
        result = engine.execute_operation("divide", [1, 1e-10])
        assert result == pytest.approx(1e10)

    # Edge cases for factorial
    @pytest.mark.parametrize("invalid_input", [-1, -5, -100])
    def test_factorial_negative_raises_error(self, engine, invalid_input):
        """Test that negative factorial raises ValueError."""
        with pytest.raises(ValueError):
            engine.execute_operation("factorial", [invalid_input])

    @pytest.mark.parametrize("invalid_input", [0.5, 1.1, 2.7, -0.5])
    def test_factorial_non_integer_raises_error(self, engine, invalid_input):
        """Test that non-integer factorial raises ValueError."""
        with pytest.raises(ValueError):
            engine.execute_operation("factorial", [invalid_input])

    @pytest.mark.parametrize("invalid_input", [True, False])
    def test_factorial_boolean_raises_error(self, engine, invalid_input):
        """Test that boolean input to factorial raises ValueError."""
        with pytest.raises(ValueError):
            engine.execute_operation("factorial", [invalid_input])

    # Edge cases for square_root
    @pytest.mark.parametrize("invalid_input", [-1, -5, -0.5, -100])
    def test_square_root_negative_raises_error(self, engine, invalid_input):
        """Test that negative square root raises ValueError."""
        with pytest.raises(ValueError):
            engine.execute_operation("square_root", [invalid_input])

    # Edge cases for log (base-10)
    @pytest.mark.parametrize("invalid_input", [0, -1, -5])
    def test_log_non_positive_raises_error(self, engine, invalid_input):
        """Test that log of non-positive number raises ValueError."""
        with pytest.raises(ValueError):
            engine.execute_operation("log", [invalid_input])

    # Edge cases for ln (natural log)
    @pytest.mark.parametrize("invalid_input", [0, -1, -5])
    def test_ln_non_positive_raises_error(self, engine, invalid_input):
        """Test that ln of non-positive number raises ValueError."""
        with pytest.raises(ValueError):
            engine.execute_operation("ln", [invalid_input])

    # Edge case for power with 0^negative
    @pytest.mark.parametrize("exponent", [-1, -2, -0.5])
    def test_power_zero_to_negative_raises_error(self, engine, exponent):
        """Test that 0^(negative) raises ValueError."""
        with pytest.raises(ValueError):
            engine.execute_operation("power", [0, exponent])

    # Edge cases for cube_root (should handle negatives)
    def test_cube_root_negative_number(self, engine):
        """Test that cube root of negative numbers works correctly."""
        result = engine.execute_operation("cube_root", [-8])
        assert result == -2

    def test_cube_root_very_small_positive(self, engine):
        """Test cube root of very small positive number."""
        result = engine.execute_operation("cube_root", [1e-9])
        assert result == pytest.approx(1e-3)


class TestEngineExceptionHandling:
    """Test suite for exception propagation in CalculationEngine."""

    @pytest.fixture
    def engine(self):
        """Fixture providing a fully configured CalculationEngine."""
        calculator = Calculator()
        registry = OperationRegistry(calculator)
        return CalculationEngine(calculator, registry)

    def test_unknown_operation_raises_keyerror(self, engine):
        """Test that unknown operation key raises KeyError."""
        with pytest.raises(KeyError):
            engine.execute_operation("unknown_op", [1, 2])

    def test_unknown_operation_keyerror_has_descriptive_message(self, engine):
        """Test that KeyError for unknown operation contains the operation key."""
        with pytest.raises(KeyError) as exc_info:
            engine.execute_operation("nonexistent", [1, 2])
        assert "nonexistent" in str(exc_info.value)

    def test_zerodivisionerror_propagates_unchanged(self, engine):
        """Test that ZeroDivisionError from divide propagates unchanged."""
        with pytest.raises(ZeroDivisionError):
            engine.execute_operation("divide", [10, 0])

    def test_valueerror_from_factorial_propagates(self, engine):
        """Test that ValueError from factorial propagates unchanged."""
        with pytest.raises(ValueError):
            engine.execute_operation("factorial", [-5])

    def test_valueerror_from_square_root_propagates(self, engine):
        """Test that ValueError from square_root propagates unchanged."""
        with pytest.raises(ValueError):
            engine.execute_operation("square_root", [-1])

    def test_valueerror_from_log_propagates(self, engine):
        """Test that ValueError from log propagates unchanged."""
        with pytest.raises(ValueError):
            engine.execute_operation("log", [0])

    def test_valueerror_from_ln_propagates(self, engine):
        """Test that ValueError from ln propagates unchanged."""
        with pytest.raises(ValueError):
            engine.execute_operation("ln", [-5])

    def test_valueerror_from_power_propagates(self, engine):
        """Test that ValueError from power(0, negative) propagates unchanged."""
        with pytest.raises(ValueError):
            engine.execute_operation("power", [0, -1])


class TestEngineArityValidation:
    """Test suite for arity-based operation execution."""

    @pytest.fixture
    def engine(self):
        """Fixture providing a fully configured CalculationEngine."""
        calculator = Calculator()
        registry = OperationRegistry(calculator)
        return CalculationEngine(calculator, registry)

    def test_unary_operation_with_single_operand(self, engine):
        """Test that unary operations accept exactly one operand."""
        # factorial is unary
        result = engine.execute_operation("factorial", [5])
        assert result == 120

    def test_binary_operation_with_two_operands(self, engine):
        """Test that binary operations accept exactly two operands."""
        # add is binary
        result = engine.execute_operation("add", [5, 3])
        assert result == 8

    def test_wrong_operand_count_causes_error(self, engine):
        """Test that providing wrong operand count causes TypeError or similar."""
        # Try to call unary operation with two operands
        with pytest.raises((TypeError, IndexError)):
            engine.execute_operation("square", [5, 3])

    def test_missing_operand_causes_error(self, engine):
        """Test that missing operands causes error."""
        with pytest.raises((TypeError, IndexError)):
            engine.execute_operation("add", [5])


class TestEngineIntegration:
    """Integration tests combining engine, calculator, and registry."""

    def test_engine_with_all_operations_in_registry(self):
        """Test that engine can successfully execute all registered operations."""
        calculator = Calculator()
        registry = OperationRegistry(calculator)
        engine = CalculationEngine(calculator, registry)

        # Get all operations from registry
        available_ops = registry.list_operations()

        # Ensure all operations can be called (with valid operands)
        test_cases = {
            "add": [2, 3],
            "subtract": [5, 2],
            "multiply": [3, 4],
            "divide": [10, 2],
            "power": [2, 3],
            "factorial": [5],
            "square": [4],
            "cube": [2],
            "square_root": [9],
            "cube_root": [8],
            "log": [10],
            "ln": [2.718],
        }

        for op_key, operands in test_cases.items():
            result = engine.execute_operation(op_key, operands)
            assert isinstance(result, (int, float))

    def test_engine_preserves_calculation_precision(self):
        """Test that engine doesn't lose precision in calculations."""
        calculator = Calculator()
        registry = OperationRegistry(calculator)
        engine = CalculationEngine(calculator, registry)

        # Test with values that might lose precision
        result = engine.execute_operation("divide", [1, 3])
        direct_calc = 1 / 3
        assert result == direct_calc

    def test_engine_result_types_are_correct(self):
        """Test that engine returns appropriate numeric types."""
        calculator = Calculator()
        registry = OperationRegistry(calculator)
        engine = CalculationEngine(calculator, registry)

        # Most operations return float or int
        add_result = engine.execute_operation("add", [5, 3])
        assert isinstance(add_result, (int, float))

        factorial_result = engine.execute_operation("factorial", [5])
        assert isinstance(factorial_result, (int, float))

        sqrt_result = engine.execute_operation("square_root", [9])
        assert isinstance(sqrt_result, (int, float))
