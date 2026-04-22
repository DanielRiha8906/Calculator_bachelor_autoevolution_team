"""Unit tests for OperationRegistry class."""

import pytest
from src.calculator import Calculator
from src.operations import OperationRegistry


class TestOperationRegistryInitialization:
    """Test suite for OperationRegistry initialization."""

    @pytest.fixture
    def calculator(self):
        """Fixture to provide a Calculator instance."""
        return Calculator()

    def test_registry_initialization(self, calculator):
        """Test that registry is initialized with all 12 operations."""
        registry = OperationRegistry(calculator)
        ops = registry.list_operations()
        assert len(ops) == 12
        assert "add" in ops
        assert "subtract" in ops
        assert "multiply" in ops
        assert "divide" in ops
        assert "power" in ops
        assert "factorial" in ops
        assert "square" in ops
        assert "cube" in ops
        assert "square_root" in ops
        assert "cube_root" in ops
        assert "log" in ops
        assert "ln" in ops

    def test_registry_keys_match_expected(self, calculator):
        """Test that all operation keys are present."""
        registry = OperationRegistry(calculator)
        ops = registry.list_operations()
        expected_keys = {
            "add", "subtract", "multiply", "divide", "power",
            "factorial", "square", "cube", "square_root", "cube_root",
            "log", "ln"
        }
        assert set(ops.keys()) == expected_keys


class TestGetOperation:
    """Test suite for OperationRegistry.get_operation() method."""

    @pytest.fixture
    def registry(self):
        """Fixture to provide a OperationRegistry instance."""
        calculator = Calculator()
        return OperationRegistry(calculator)

    @pytest.mark.parametrize("operation_key", [
        "add", "subtract", "multiply", "divide", "power",
        "factorial", "square", "cube", "square_root", "cube_root",
        "log", "ln"
    ])
    def test_get_operation_returns_tuple(self, registry, operation_key):
        """Test that get_operation returns a tuple for all operations."""
        result = registry.get_operation(operation_key)
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_get_operation_returns_callable(self, registry):
        """Test that first element of returned tuple is callable."""
        method, arity, description = registry.get_operation("add")
        assert callable(method)

    def test_get_operation_add_correct_arity(self, registry):
        """Test that 'add' operation has arity of 2."""
        method, arity, description = registry.get_operation("add")
        assert arity == 2

    def test_get_operation_square_correct_arity(self, registry):
        """Test that 'square' operation has arity of 1."""
        method, arity, description = registry.get_operation("square")
        assert arity == 1

    def test_get_operation_returns_description(self, registry):
        """Test that third element is a string description."""
        method, arity, description = registry.get_operation("add")
        assert isinstance(description, str)
        assert len(description) > 0

    def test_get_operation_unknown_raises_keyerror(self, registry):
        """Test that unknown operation key raises KeyError."""
        with pytest.raises(KeyError, match="Unknown operation: 'unknown'"):
            registry.get_operation("unknown")

    @pytest.mark.parametrize("invalid_key", [
        "xyz", "ADD", "addd", "", "sqrt", "division"
    ])
    def test_get_operation_various_invalid_keys(self, registry, invalid_key):
        """Test that various invalid keys raise KeyError."""
        with pytest.raises(KeyError):
            registry.get_operation(invalid_key)


class TestListOperations:
    """Test suite for OperationRegistry.list_operations() method."""

    @pytest.fixture
    def registry(self):
        """Fixture to provide a OperationRegistry instance."""
        calculator = Calculator()
        return OperationRegistry(calculator)

    def test_list_operations_returns_dict(self, registry):
        """Test that list_operations returns a dictionary."""
        result = registry.list_operations()
        assert isinstance(result, dict)

    def test_list_operations_includes_all_keys(self, registry):
        """Test that list_operations includes all 12 operations."""
        ops = registry.list_operations()
        assert len(ops) == 12

    def test_list_operations_description_format(self, registry):
        """Test that each operation has a meaningful description."""
        ops = registry.list_operations()
        for key, description in ops.items():
            assert isinstance(description, str)
            assert len(description) > 0
            # Descriptions should contain some parentheses with formula
            assert "(" in description and ")" in description

    def test_list_operations_not_empty(self, registry):
        """Test that list_operations returns non-empty dict."""
        ops = registry.list_operations()
        assert len(ops) > 0


class TestOperationArity:
    """Test suite for operation arity validation."""

    @pytest.fixture
    def registry(self):
        """Fixture to provide a OperationRegistry instance."""
        calculator = Calculator()
        return OperationRegistry(calculator)

    @pytest.mark.parametrize("binary_op", [
        "add", "subtract", "multiply", "divide", "power"
    ])
    def test_binary_operations_have_arity_two(self, registry, binary_op):
        """Test that binary operations have arity of 2."""
        method, arity, description = registry.get_operation(binary_op)
        assert arity == 2

    @pytest.mark.parametrize("unary_op", [
        "factorial", "square", "cube", "square_root", "cube_root", "log", "ln"
    ])
    def test_unary_operations_have_arity_one(self, registry, unary_op):
        """Test that unary operations have arity of 1."""
        method, arity, description = registry.get_operation(unary_op)
        assert arity == 1


class TestOperationCallability:
    """Test suite for operation method callability and correctness."""

    @pytest.fixture
    def registry(self):
        """Fixture to provide a OperationRegistry instance."""
        calculator = Calculator()
        return OperationRegistry(calculator)

    def test_add_operation_callable_and_correct(self, registry):
        """Test that add operation is callable and produces correct result."""
        method, arity, description = registry.get_operation("add")
        assert callable(method)
        result = method(5, 3)
        assert result == 8

    def test_square_operation_callable_and_correct(self, registry):
        """Test that square operation is callable and produces correct result."""
        method, arity, description = registry.get_operation("square")
        assert callable(method)
        result = method(5)
        assert result == 25

    def test_divide_operation_callable_and_correct(self, registry):
        """Test that divide operation is callable and produces correct result."""
        method, arity, description = registry.get_operation("divide")
        assert callable(method)
        result = method(10, 2)
        assert result == 5.0

    def test_factorial_operation_callable_and_correct(self, registry):
        """Test that factorial operation is callable and produces correct result."""
        method, arity, description = registry.get_operation("factorial")
        assert callable(method)
        result = method(5)
        assert result == 120

    def test_cube_root_operation_callable_and_correct(self, registry):
        """Test that cube_root operation is callable and produces correct result."""
        method, arity, description = registry.get_operation("cube_root")
        assert callable(method)
        result = method(8)
        assert result == 2.0

    def test_ln_operation_callable_and_correct(self, registry):
        """Test that ln operation is callable and produces correct result."""
        method, arity, description = registry.get_operation("ln")
        assert callable(method)
        result = method(1)
        assert result == 0.0

    def test_operation_raises_exception_on_invalid_input(self, registry):
        """Test that operations raise appropriate exceptions on invalid input."""
        # Division by zero
        divide_method, _, _ = registry.get_operation("divide")
        with pytest.raises(ZeroDivisionError):
            divide_method(5, 0)

        # Factorial of negative number
        factorial_method, _, _ = registry.get_operation("factorial")
        with pytest.raises(ValueError):
            factorial_method(-1)

        # Log of negative number
        log_method, _, _ = registry.get_operation("log")
        with pytest.raises(ValueError):
            log_method(-1)


class TestRegistryIsolation:
    """Test that registry is properly isolated with different Calculator instances."""

    def test_registry_with_different_calculator_instances(self):
        """Test that different Calculator instances produce independent registries."""
        calc1 = Calculator()
        calc2 = Calculator()
        registry1 = OperationRegistry(calc1)
        registry2 = OperationRegistry(calc2)

        # Both should work independently
        method1, _, _ = registry1.get_operation("add")
        method2, _, _ = registry2.get_operation("add")

        assert method1(2, 3) == 5
        assert method2(2, 3) == 5
