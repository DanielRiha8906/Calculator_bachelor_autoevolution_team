"""Unit tests for calculator GUI mode abstraction.

This module tests the CalcMode abstract base class and its concrete
implementations (SimpleMode, ScientificMode) without requiring any tkinter
window creation.
"""

import pytest
from src.core.calculator import Calculator
from src.gui.modes import CalcMode, SimpleMode, ScientificMode


class TestSimpleMode:
    """Unit tests for SimpleMode."""

    @pytest.fixture
    def calculator(self):
        """Provide a fresh Calculator instance for each test."""
        return Calculator()

    @pytest.fixture
    def simple_mode(self, calculator):
        """Provide a SimpleMode instance."""
        return SimpleMode(calculator)

    def test_simple_mode_name(self, simple_mode):
        """Test that SimpleMode.name returns 'Simple'."""
        assert simple_mode.name == "Simple"

    def test_simple_mode_name_type(self, simple_mode):
        """Test that name property returns a string."""
        assert isinstance(simple_mode.name, str)

    def test_simple_mode_operations_count(self, simple_mode):
        """Test that SimpleMode has exactly 6 operations."""
        ops = simple_mode.get_operations()
        assert len(ops) == 6

    def test_simple_mode_operations_type(self, simple_mode):
        """Test that get_operations returns a dict."""
        ops = simple_mode.get_operations()
        assert isinstance(ops, dict)

    def test_simple_mode_contains_add(self, simple_mode):
        """Test that 'add' is in SimpleMode operations."""
        ops = simple_mode.get_operations()
        assert "add" in ops

    def test_simple_mode_contains_subtract(self, simple_mode):
        """Test that 'subtract' is in SimpleMode operations."""
        ops = simple_mode.get_operations()
        assert "subtract" in ops

    def test_simple_mode_contains_multiply(self, simple_mode):
        """Test that 'multiply' is in SimpleMode operations."""
        ops = simple_mode.get_operations()
        assert "multiply" in ops

    def test_simple_mode_contains_divide(self, simple_mode):
        """Test that 'divide' is in SimpleMode operations."""
        ops = simple_mode.get_operations()
        assert "divide" in ops

    def test_simple_mode_contains_square(self, simple_mode):
        """Test that 'square' is in SimpleMode operations."""
        ops = simple_mode.get_operations()
        assert "square" in ops

    def test_simple_mode_contains_square_root(self, simple_mode):
        """Test that 'square_root' is in SimpleMode operations."""
        ops = simple_mode.get_operations()
        assert "square_root" in ops

    def test_simple_mode_excludes_power(self, simple_mode):
        """Test that 'power' is NOT in SimpleMode operations."""
        ops = simple_mode.get_operations()
        assert "power" not in ops

    def test_simple_mode_excludes_factorial(self, simple_mode):
        """Test that 'factorial' is NOT in SimpleMode operations."""
        ops = simple_mode.get_operations()
        assert "factorial" not in ops

    def test_simple_mode_excludes_sin(self, simple_mode):
        """Test that 'sin' is NOT in SimpleMode operations."""
        ops = simple_mode.get_operations()
        assert "sin" not in ops

    def test_simple_mode_excludes_cos(self, simple_mode):
        """Test that 'cos' is NOT in SimpleMode operations."""
        ops = simple_mode.get_operations()
        assert "cos" not in ops

    def test_simple_mode_excludes_log(self, simple_mode):
        """Test that 'log' is NOT in SimpleMode operations."""
        ops = simple_mode.get_operations()
        assert "log" not in ops

    def test_simple_mode_operations_are_tuples(self, simple_mode):
        """Test that all operations are tuples."""
        ops = simple_mode.get_operations()
        for op_name, op_tuple in ops.items():
            assert isinstance(op_tuple, tuple)

    def test_simple_mode_operation_tuple_length(self, simple_mode):
        """Test that all operation tuples have length 2 (callable, arity)."""
        ops = simple_mode.get_operations()
        for op_name, op_tuple in ops.items():
            assert len(op_tuple) == 2

    def test_simple_mode_operations_callables(self, simple_mode):
        """Test that all operation values are callable."""
        ops = simple_mode.get_operations()
        for op_name, (op_callable, arity) in ops.items():
            assert callable(op_callable)

    def test_simple_mode_operations_arity_are_ints(self, simple_mode):
        """Test that all operation arities are integers."""
        ops = simple_mode.get_operations()
        for op_name, (op_callable, arity) in ops.items():
            assert isinstance(arity, int)

    def test_simple_mode_operations_arity_valid_values(self, simple_mode):
        """Test that all operation arities are 1 or 2."""
        ops = simple_mode.get_operations()
        for op_name, (op_callable, arity) in ops.items():
            assert arity in (1, 2)

    def test_simple_mode_binary_ops_have_arity_2(self, simple_mode):
        """Test that binary operations have arity 2."""
        ops = simple_mode.get_operations()
        binary_ops = {"add", "subtract", "multiply", "divide"}
        for op_name in binary_ops:
            assert ops[op_name][1] == 2

    def test_simple_mode_unary_ops_have_arity_1(self, simple_mode):
        """Test that unary operations have arity 1."""
        ops = simple_mode.get_operations()
        unary_ops = {"square", "square_root"}
        for op_name in unary_ops:
            assert ops[op_name][1] == 1

    def test_simple_mode_get_operations_returns_copy(self, simple_mode):
        """Test that get_operations returns a new dict each call."""
        ops1 = simple_mode.get_operations()
        ops2 = simple_mode.get_operations()
        assert ops1 == ops2
        assert ops1 is not ops2

    def test_simple_mode_operations_are_bound_methods(self, simple_mode):
        """Test that operation callables are bound methods of Calculator."""
        ops = simple_mode.get_operations()
        for op_name, (op_callable, _) in ops.items():
            # Bound methods have __self__ attribute
            assert hasattr(op_callable, "__self__")


class TestScientificMode:
    """Unit tests for ScientificMode."""

    @pytest.fixture
    def calculator(self):
        """Provide a fresh Calculator instance for each test."""
        return Calculator()

    @pytest.fixture
    def scientific_mode(self, calculator):
        """Provide a ScientificMode instance."""
        return ScientificMode(calculator)

    def test_scientific_mode_name(self, scientific_mode):
        """Test that ScientificMode.name returns 'Scientific'."""
        assert scientific_mode.name == "Scientific"

    def test_scientific_mode_name_type(self, scientific_mode):
        """Test that name property returns a string."""
        assert isinstance(scientific_mode.name, str)

    def test_scientific_mode_operations_count(self, scientific_mode):
        """Test that ScientificMode has exactly 18 operations."""
        ops = scientific_mode.get_operations()
        assert len(ops) == 18

    def test_scientific_mode_operations_type(self, scientific_mode):
        """Test that get_operations returns a dict."""
        ops = scientific_mode.get_operations()
        assert isinstance(ops, dict)

    def test_scientific_mode_contains_all_normal_ops(self, scientific_mode):
        """Test that all 6 normal operations are in scientific mode."""
        ops = scientific_mode.get_operations()
        normal_ops = {"add", "subtract", "multiply", "divide", "square", "square_root"}
        for op_name in normal_ops:
            assert op_name in ops

    def test_scientific_mode_contains_power(self, scientific_mode):
        """Test that 'power' is in ScientificMode."""
        ops = scientific_mode.get_operations()
        assert "power" in ops

    def test_scientific_mode_contains_cube(self, scientific_mode):
        """Test that 'cube' is in ScientificMode."""
        ops = scientific_mode.get_operations()
        assert "cube" in ops

    def test_scientific_mode_contains_cube_root(self, scientific_mode):
        """Test that 'cube_root' is in ScientificMode."""
        ops = scientific_mode.get_operations()
        assert "cube_root" in ops

    def test_scientific_mode_contains_factorial(self, scientific_mode):
        """Test that 'factorial' is in ScientificMode."""
        ops = scientific_mode.get_operations()
        assert "factorial" in ops

    def test_scientific_mode_contains_log(self, scientific_mode):
        """Test that 'log' is in ScientificMode."""
        ops = scientific_mode.get_operations()
        assert "log" in ops

    def test_scientific_mode_contains_ln(self, scientific_mode):
        """Test that 'ln' is in ScientificMode."""
        ops = scientific_mode.get_operations()
        assert "ln" in ops

    def test_scientific_mode_contains_sin(self, scientific_mode):
        """Test that 'sin' is in ScientificMode."""
        ops = scientific_mode.get_operations()
        assert "sin" in ops

    def test_scientific_mode_contains_cos(self, scientific_mode):
        """Test that 'cos' is in ScientificMode."""
        ops = scientific_mode.get_operations()
        assert "cos" in ops

    def test_scientific_mode_contains_tan(self, scientific_mode):
        """Test that 'tan' is in ScientificMode."""
        ops = scientific_mode.get_operations()
        assert "tan" in ops

    def test_scientific_mode_contains_cot(self, scientific_mode):
        """Test that 'cot' is in ScientificMode."""
        ops = scientific_mode.get_operations()
        assert "cot" in ops

    def test_scientific_mode_contains_asin(self, scientific_mode):
        """Test that 'asin' is in ScientificMode."""
        ops = scientific_mode.get_operations()
        assert "asin" in ops

    def test_scientific_mode_contains_acos(self, scientific_mode):
        """Test that 'acos' is in ScientificMode."""
        ops = scientific_mode.get_operations()
        assert "acos" in ops

    def test_scientific_mode_operations_are_tuples(self, scientific_mode):
        """Test that all operations are tuples."""
        ops = scientific_mode.get_operations()
        for op_name, op_tuple in ops.items():
            assert isinstance(op_tuple, tuple)

    def test_scientific_mode_operation_tuple_length(self, scientific_mode):
        """Test that all operation tuples have length 2."""
        ops = scientific_mode.get_operations()
        for op_name, op_tuple in ops.items():
            assert len(op_tuple) == 2

    def test_scientific_mode_operations_callables(self, scientific_mode):
        """Test that all operation callables are callable."""
        ops = scientific_mode.get_operations()
        for op_name, (op_callable, arity) in ops.items():
            assert callable(op_callable)

    def test_scientific_mode_operations_arity_are_ints(self, scientific_mode):
        """Test that all operation arities are integers."""
        ops = scientific_mode.get_operations()
        for op_name, (op_callable, arity) in ops.items():
            assert isinstance(arity, int)

    def test_scientific_mode_operations_arity_valid_values(self, scientific_mode):
        """Test that all operation arities are 1 or 2."""
        ops = scientific_mode.get_operations()
        for op_name, (op_callable, arity) in ops.items():
            assert arity in (1, 2)

    def test_scientific_mode_binary_ops_have_arity_2(self, scientific_mode):
        """Test that binary operations have arity 2."""
        ops = scientific_mode.get_operations()
        binary_ops = {"add", "subtract", "multiply", "divide", "power"}
        for op_name in binary_ops:
            assert ops[op_name][1] == 2

    def test_scientific_mode_unary_ops_have_arity_1(self, scientific_mode):
        """Test that unary operations have arity 1."""
        ops = scientific_mode.get_operations()
        unary_ops = {
            "square", "square_root", "cube", "cube_root", "factorial",
            "log", "ln", "sin", "cos", "tan", "cot", "asin", "acos"
        }
        for op_name in unary_ops:
            assert ops[op_name][1] == 1

    def test_scientific_mode_get_operations_returns_copy(self, scientific_mode):
        """Test that get_operations returns a new dict each call."""
        ops1 = scientific_mode.get_operations()
        ops2 = scientific_mode.get_operations()
        assert ops1 == ops2
        assert ops1 is not ops2

    def test_scientific_mode_operations_are_bound_methods(self, scientific_mode):
        """Test that operation callables are bound methods of Calculator."""
        ops = scientific_mode.get_operations()
        for op_name, (op_callable, _) in ops.items():
            assert hasattr(op_callable, "__self__")


class TestCalcModeAbstraction:
    """Test the CalcMode abstract base class contract."""

    def test_calc_mode_is_abstract(self):
        """Test that CalcMode cannot be instantiated directly."""
        with pytest.raises(TypeError):
            CalcMode()

    def test_simple_mode_is_subclass_of_calc_mode(self):
        """Test that SimpleMode is a subclass of CalcMode."""
        assert issubclass(SimpleMode, CalcMode)

    def test_scientific_mode_is_subclass_of_calc_mode(self):
        """Test that ScientificMode is a subclass of CalcMode."""
        assert issubclass(ScientificMode, CalcMode)

    def test_simple_mode_instance_is_calc_mode(self):
        """Test that SimpleMode instances are instances of CalcMode."""
        calc = Calculator()
        simple = SimpleMode(calc)
        assert isinstance(simple, CalcMode)

    def test_scientific_mode_instance_is_calc_mode(self):
        """Test that ScientificMode instances are instances of CalcMode."""
        calc = Calculator()
        scientific = ScientificMode(calc)
        assert isinstance(scientific, CalcMode)


class TestModeOperationIntegration:
    """Integration tests verifying operations work with their arity."""

    @pytest.fixture
    def calculator(self):
        """Provide a fresh Calculator instance."""
        return Calculator()

    def test_simple_mode_binary_op_callable(self, calculator):
        """Test that a binary op from SimpleMode is callable with 2 args."""
        simple = SimpleMode(calculator)
        ops = simple.get_operations()
        add_fn, add_arity = ops["add"]

        assert add_arity == 2
        result = add_fn(2, 3)
        assert result == 5

    def test_simple_mode_unary_op_callable(self, calculator):
        """Test that a unary op from SimpleMode is callable with 1 arg."""
        simple = SimpleMode(calculator)
        ops = simple.get_operations()
        square_fn, square_arity = ops["square"]

        assert square_arity == 1
        result = square_fn(4)
        assert result == 16

    def test_scientific_mode_binary_op_callable(self, calculator):
        """Test that a binary op from ScientificMode is callable."""
        scientific = ScientificMode(calculator)
        ops = scientific.get_operations()
        power_fn, power_arity = ops["power"]

        assert power_arity == 2
        result = power_fn(2, 3)
        assert result == 8

    def test_scientific_mode_unary_op_callable(self, calculator):
        """Test that a unary op from ScientificMode is callable."""
        scientific = ScientificMode(calculator)
        ops = scientific.get_operations()
        factorial_fn, factorial_arity = ops["factorial"]

        assert factorial_arity == 1
        result = factorial_fn(5)
        assert result == 120

    def test_scientific_mode_has_more_ops_than_simple(self, calculator):
        """Test that ScientificMode has more operations than SimpleMode."""
        simple = SimpleMode(calculator)
        scientific = ScientificMode(calculator)

        simple_ops = simple.get_operations()
        scientific_ops = scientific.get_operations()

        assert len(scientific_ops) > len(simple_ops)
        assert len(scientific_ops) == 18
        assert len(simple_ops) == 6

    def test_scientific_mode_contains_all_simple_ops(self, calculator):
        """Test that ScientificMode contains all SimpleMode operations."""
        simple = SimpleMode(calculator)
        scientific = ScientificMode(calculator)

        simple_ops = simple.get_operations()
        scientific_ops = scientific.get_operations()

        for op_name in simple_ops:
            assert op_name in scientific_ops
