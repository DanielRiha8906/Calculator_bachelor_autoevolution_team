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


class TestRegisterOperation:
    """Test suite for OperationRegistry.register_operation() method."""

    @pytest.fixture
    def registry(self):
        """Fixture to provide a fresh OperationRegistry instance."""
        calculator = Calculator()
        return OperationRegistry(calculator)

    # ========== Happy Path Tests ==========

    def test_register_operation_success_unary(self, registry):
        """Test successful registration of a unary operation."""
        # Define a simple unary operation
        def double(x):
            return x * 2

        registry.register_operation(
            key="double",
            method=double,
            arity=1,
            description="Double the value"
        )

        # Verify operation was registered
        method, arity, description = registry.get_operation("double")
        assert method is double
        assert arity == 1
        assert description == "Double the value"
        assert callable(method)

    def test_register_operation_success_binary(self, registry):
        """Test successful registration of a binary operation."""
        # Define a simple binary operation
        def modulo(a, b):
            return a % b

        registry.register_operation(
            key="modulo",
            method=modulo,
            arity=2,
            description="Modulo (a % b)"
        )

        # Verify operation was registered
        method, arity, description = registry.get_operation("modulo")
        assert method is modulo
        assert arity == 2
        assert description == "Modulo (a % b)"

    def test_register_operation_appears_in_list_operations(self, registry):
        """Test that a registered operation appears in list_operations()."""
        def absolute(x):
            return abs(x)

        registry.register_operation(
            key="abs",
            method=absolute,
            arity=1,
            description="Absolute value (|x|)"
        )

        ops = registry.list_operations()
        assert "abs" in ops
        assert ops["abs"] == "Absolute value (|x|)"

    def test_register_operation_callable_with_engine(self, registry):
        """Test end-to-end: registered operation works with CalculationEngine."""
        from src.engine import CalculationEngine

        def subtract_10(x):
            return x - 10

        registry.register_operation(
            key="subtract_10",
            method=subtract_10,
            arity=1,
            description="Subtract 10 from x"
        )

        calculator = Calculator()
        engine = CalculationEngine(calculator, registry)
        result = engine.execute_operation("subtract_10", [25])
        assert result == 15

    def test_register_multiple_operations_independently(self, registry):
        """Test that multiple custom operations can be registered independently."""
        def op1(x):
            return x + 1

        def op2(x):
            return x - 1

        registry.register_operation("op1", op1, 1, "Op1")
        registry.register_operation("op2", op2, 1, "Op2")

        # Both should be retrievable
        m1, a1, _ = registry.get_operation("op1")
        m2, a2, _ = registry.get_operation("op2")

        assert m1 is op1
        assert m2 is op2
        assert m1(5) == 6
        assert m2(5) == 4

    # ========== Duplicate Key Tests ==========

    def test_register_operation_duplicate_key_raises_valueerror(self, registry):
        """Test that registering a duplicate key raises ValueError."""
        def custom_op(x):
            return x

        registry.register_operation("new_op", custom_op, 1, "Custom")

        with pytest.raises(ValueError, match="already registered"):
            registry.register_operation("new_op", custom_op, 1, "Duplicate")

    def test_register_operation_duplicate_builtin_key_raises_valueerror(self, registry):
        """Test that trying to register an existing built-in key raises ValueError."""
        def fake_add(a, b):
            return a - b  # Intentionally wrong

        with pytest.raises(ValueError, match="already registered"):
            registry.register_operation("add", fake_add, 2, "Fake add")

    @pytest.mark.parametrize("builtin_key", [
        "add", "subtract", "multiply", "divide", "power",
        "factorial", "square", "cube", "square_root", "cube_root",
        "log", "ln"
    ])
    def test_register_operation_all_builtin_keys_protected(self, registry, builtin_key):
        """Test that all built-in operation keys cannot be overridden."""
        def dummy(x):
            return x

        with pytest.raises(ValueError, match="already registered"):
            registry.register_operation(builtin_key, dummy, 1, "Dummy")

    # ========== Non-Callable Method Tests ==========

    def test_register_operation_non_callable_int_raises_typeerror(self, registry):
        """Test that passing an int as method raises TypeError."""
        with pytest.raises(TypeError, match="must be callable"):
            registry.register_operation("bad", 42, 1, "Bad")

    def test_register_operation_non_callable_string_raises_typeerror(self, registry):
        """Test that passing a string as method raises TypeError."""
        with pytest.raises(TypeError, match="must be callable"):
            registry.register_operation("bad", "not_callable", 1, "Bad")

    def test_register_operation_non_callable_none_raises_typeerror(self, registry):
        """Test that passing None as method raises TypeError."""
        with pytest.raises(TypeError, match="must be callable"):
            registry.register_operation("bad", None, 1, "Bad")

    def test_register_operation_non_callable_list_raises_typeerror(self, registry):
        """Test that passing a list as method raises TypeError."""
        with pytest.raises(TypeError, match="must be callable"):
            registry.register_operation("bad", [1, 2, 3], 1, "Bad")

    def test_register_operation_non_callable_dict_raises_typeerror(self, registry):
        """Test that passing a dict as method raises TypeError."""
        with pytest.raises(TypeError, match="must be callable"):
            registry.register_operation("bad", {"a": 1}, 1, "Bad")

    # ========== Arity Validation Tests ==========

    def test_register_operation_arity_zero_raises_valueerror(self, registry):
        """Test that arity=0 raises ValueError."""
        def no_args():
            return 42

        with pytest.raises(ValueError, match="must be a positive integer"):
            registry.register_operation("zero_arity", no_args, 0, "Zero arity")

    def test_register_operation_arity_negative_raises_valueerror(self, registry):
        """Test that negative arity raises ValueError."""
        def dummy(x):
            return x

        with pytest.raises(ValueError, match="must be a positive integer"):
            registry.register_operation("neg_arity", dummy, -1, "Negative arity")

    def test_register_operation_arity_large_negative_raises_valueerror(self, registry):
        """Test that large negative arity raises ValueError."""
        def dummy(x):
            return x

        with pytest.raises(ValueError, match="must be a positive integer"):
            registry.register_operation("neg_arity", dummy, -999, "Large negative")

    def test_register_operation_arity_bool_true_raises_valueerror(self, registry):
        """Test that arity=True (bool) raises ValueError."""
        def dummy(x):
            return x

        with pytest.raises(ValueError, match="must be a positive integer"):
            registry.register_operation("bool_arity", dummy, True, "Bool True")

    def test_register_operation_arity_bool_false_raises_valueerror(self, registry):
        """Test that arity=False (bool) raises ValueError."""
        def dummy(x):
            return x

        with pytest.raises(ValueError, match="must be a positive integer"):
            registry.register_operation("bool_arity", dummy, False, "Bool False")

    def test_register_operation_arity_float_raises_valueerror(self, registry):
        """Test that arity as float raises ValueError."""
        def dummy(x):
            return x

        with pytest.raises(ValueError, match="must be a positive integer"):
            registry.register_operation("float_arity", dummy, 1.0, "Float arity")

    def test_register_operation_arity_float_non_integer_raises_valueerror(self, registry):
        """Test that non-integer float arity raises ValueError."""
        def dummy(x):
            return x

        with pytest.raises(ValueError, match="must be a positive integer"):
            registry.register_operation("float_arity", dummy, 1.5, "Non-int float")

    def test_register_operation_arity_string_raises_valueerror(self, registry):
        """Test that string arity raises ValueError."""
        def dummy(x):
            return x

        with pytest.raises(ValueError, match="must be a positive integer"):
            registry.register_operation("str_arity", dummy, "2", "String arity")

    def test_register_operation_arity_none_raises_valueerror(self, registry):
        """Test that None arity raises ValueError."""
        def dummy(x):
            return x

        with pytest.raises(ValueError, match="must be a positive integer"):
            registry.register_operation("none_arity", dummy, None, "None arity")

    def test_register_operation_arity_valid_positive_integers(self, registry):
        """Test that valid positive integer arities are accepted."""
        def dummy1(x):
            return x

        def dummy2(a, b):
            return a + b

        def dummy5(*args):
            return sum(args)

        # Should not raise
        registry.register_operation("arity1", dummy1, 1, "Arity 1")
        registry.register_operation("arity2", dummy2, 2, "Arity 2")
        registry.register_operation("arity5", dummy5, 5, "Arity 5")

        # Verify all were registered
        _, a1, _ = registry.get_operation("arity1")
        _, a2, _ = registry.get_operation("arity2")
        _, a5, _ = registry.get_operation("arity5")

        assert a1 == 1
        assert a2 == 2
        assert a5 == 5

    # ========== Description Field Tests ==========

    def test_register_operation_with_empty_description(self, registry):
        """Test that empty description string is allowed (edge case)."""
        def dummy(x):
            return x

        # Should not raise
        registry.register_operation("empty_desc", dummy, 1, "")

        _, _, description = registry.get_operation("empty_desc")
        assert description == ""

    def test_register_operation_with_long_description(self, registry):
        """Test that long description string is accepted."""
        def dummy(x):
            return x

        long_desc = "This is a very long description " * 100

        registry.register_operation("long_desc", dummy, 1, long_desc)

        _, _, description = registry.get_operation("long_desc")
        assert description == long_desc

    def test_register_operation_description_with_special_chars(self, registry):
        """Test that description with special characters is preserved."""
        def dummy(x):
            return x

        special_desc = "Special: © ® ™ 你好 🔬 √ ∞"

        registry.register_operation("special_desc", dummy, 1, special_desc)

        _, _, description = registry.get_operation("special_desc")
        assert description == special_desc

    # ========== Lambda and Callable Class Tests ==========

    def test_register_operation_with_lambda(self, registry):
        """Test that lambda functions are accepted as methods."""
        registry.register_operation(
            "lambda_op",
            lambda x: x ** 2,
            1,
            "Square via lambda"
        )

        method, _, _ = registry.get_operation("lambda_op")
        assert method(5) == 25

    def test_register_operation_with_callable_class(self, registry):
        """Test that callable class instances are accepted as methods."""
        class Doubler:
            def __call__(self, x):
                return x * 2

        doubler = Doubler()
        registry.register_operation("doubler", doubler, 1, "Double via class")

        method, _, _ = registry.get_operation("doubler")
        assert method(5) == 10

    def test_register_operation_with_builtin_function(self, registry):
        """Test that built-in functions like abs() are accepted."""
        registry.register_operation("builtin_abs", abs, 1, "Absolute value")

        method, _, _ = registry.get_operation("builtin_abs")
        assert method(-5) == 5

    def test_register_operation_with_math_module_function(self, registry):
        """Test that standard library functions like math.sqrt are accepted."""
        import math

        registry.register_operation("math_sqrt", math.sqrt, 1, "Square root via math")

        method, _, _ = registry.get_operation("math_sqrt")
        assert method(16) == 4.0

    # ========== State and Side Effect Tests ==========

    def test_register_operation_does_not_modify_existing_operations(self, registry):
        """Test that registering a new operation doesn't affect existing ones."""
        add_before, _, _ = registry.get_operation("add")

        def dummy(x):
            return x

        registry.register_operation("dummy", dummy, 1, "Dummy")

        add_after, _, _ = registry.get_operation("add")
        assert add_before is add_after
        assert add_before(2, 3) == 5

    def test_register_operation_all_builtin_operations_still_present(self, registry):
        """Test that built-in operations are still present after registering custom ones."""
        def dummy(x):
            return x

        registry.register_operation("custom1", dummy, 1, "Custom 1")
        registry.register_operation("custom2", dummy, 2, "Custom 2")

        ops = registry.list_operations()
        expected_builtin = {
            "add", "subtract", "multiply", "divide", "power",
            "factorial", "square", "cube", "square_root", "cube_root",
            "log", "ln"
        }
        for key in expected_builtin:
            assert key in ops
