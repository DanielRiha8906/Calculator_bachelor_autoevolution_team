"""Tests for modular calculator structure (Issue #404).

This test module verifies that the calculator logic is properly separated
into modular components: basic_operations, advanced_operations, and
calculator_core modules.
"""

import math
import pytest


# Test 1: basic_operations module exists
def test_basic_operations_module_exists():
    """Verify basic_operations module can be imported."""
    from src import basic_operations
    assert basic_operations is not None


# Test 2: advanced_operations module exists
def test_advanced_operations_module_exists():
    """Verify advanced_operations module can be imported."""
    from src import advanced_operations
    assert advanced_operations is not None


# Test 3: calculator_core module exists
def test_calculator_core_module_exists():
    """Verify calculator_core module can be imported."""
    from src import calculator_core
    assert calculator_core is not None


# Test 4: OPERATIONS registry exists in interface
def test_operations_registry_exists():
    """Verify OPERATIONS dict in interface with all 12 operations."""
    from src.interface import OPERATIONS
    assert isinstance(OPERATIONS, dict)
    assert len(OPERATIONS) == 12
    expected_ops = {"+", "-", "*", "/", "square", "cube", "sqrt", "cbrt", "factorial", "power", "log", "ln"}
    assert set(OPERATIONS.keys()) == expected_ops


# Test 5: Calculator backward compatible from src.calculator
def test_calculator_backward_compat_import():
    """Verify Calculator still importable from src.calculator for backward compatibility."""
    from src.calculator import Calculator
    c = Calculator()
    assert isinstance(c, Calculator)


# Test 6: basic_operations.add
def test_basic_operations_add():
    """Test basic_operations.add(5, 3) returns 8."""
    from src import basic_operations
    result = basic_operations.add(5, 3)
    assert result == 8


# Test 7: basic_operations.subtract
def test_basic_operations_subtract():
    """Test basic_operations.subtract(10, 4) returns 6."""
    from src import basic_operations
    result = basic_operations.subtract(10, 4)
    assert result == 6


# Test 8: basic_operations.multiply
def test_basic_operations_multiply():
    """Test basic_operations.multiply(3, 7) returns 21."""
    from src import basic_operations
    result = basic_operations.multiply(3, 7)
    assert result == 21


# Test 9: basic_operations.divide
def test_basic_operations_divide():
    """Test basic_operations.divide(20, 4) returns 5.0."""
    from src import basic_operations
    result = basic_operations.divide(20, 4)
    assert result == 5.0


# Test 10: basic_operations.divide by zero
def test_basic_operations_divide_by_zero():
    """Test basic_operations.divide(10, 0) raises ZeroDivisionError."""
    from src import basic_operations
    with pytest.raises(ZeroDivisionError):
        basic_operations.divide(10, 0)


# Test 11: advanced_operations.square
def test_advanced_operations_square():
    """Test advanced_operations.square(5) returns 25."""
    from src import advanced_operations
    result = advanced_operations.square(5)
    assert result == 25


# Test 12: advanced_operations.cube
def test_advanced_operations_cube():
    """Test advanced_operations.cube(3) returns 27."""
    from src import advanced_operations
    result = advanced_operations.cube(3)
    assert result == 27


# Test 13: advanced_operations.square_root
def test_advanced_operations_sqrt():
    """Test advanced_operations.square_root(16) returns 4.0."""
    from src import advanced_operations
    result = advanced_operations.square_root(16)
    assert result == 4.0


# Test 14: advanced_operations.square_root negative
def test_advanced_operations_sqrt_negative():
    """Test advanced_operations.square_root(-1) raises ValueError."""
    from src import advanced_operations
    with pytest.raises(ValueError):
        advanced_operations.square_root(-1)


# Test 15: advanced_operations.cube_root
def test_advanced_operations_cbrt():
    """Test advanced_operations.cube_root(8) returns 2.0."""
    from src import advanced_operations
    result = advanced_operations.cube_root(8)
    assert result == 2.0


# Test 16: advanced_operations.cube_root negative
def test_advanced_operations_cbrt_negative():
    """Test advanced_operations.cube_root(-8) returns approximately -2.0."""
    from src import advanced_operations
    result = advanced_operations.cube_root(-8)
    assert result == pytest.approx(-2.0, abs=1e-9)


# Test 17: advanced_operations.factorial
def test_advanced_operations_factorial():
    """Test advanced_operations.factorial(5) returns 120."""
    from src import advanced_operations
    result = advanced_operations.factorial(5)
    assert result == 120


# Test 18: advanced_operations.factorial zero
def test_advanced_operations_factorial_zero():
    """Test advanced_operations.factorial(0) returns 1."""
    from src import advanced_operations
    result = advanced_operations.factorial(0)
    assert result == 1


# Test 19: advanced_operations.factorial negative
def test_advanced_operations_factorial_negative():
    """Test advanced_operations.factorial(-1) raises ValueError."""
    from src import advanced_operations
    with pytest.raises(ValueError):
        advanced_operations.factorial(-1)


# Test 20: advanced_operations.power
def test_advanced_operations_power():
    """Test advanced_operations.power(2, 3) returns 8."""
    from src import advanced_operations
    result = advanced_operations.power(2, 3)
    assert result == 8


# Test 21: advanced_operations.log
def test_advanced_operations_log():
    """Test advanced_operations.log(100) returns pytest.approx(2.0)."""
    from src import advanced_operations
    result = advanced_operations.log(100)
    assert result == pytest.approx(2.0)


# Test 22: advanced_operations.log zero
def test_advanced_operations_log_zero():
    """Test advanced_operations.log(0) raises ValueError."""
    from src import advanced_operations
    with pytest.raises(ValueError):
        advanced_operations.log(0)


# Test 23: advanced_operations.ln
def test_advanced_operations_ln():
    """Test advanced_operations.ln(math.e) returns pytest.approx(1.0)."""
    from src import advanced_operations
    result = advanced_operations.ln(math.e)
    assert result == pytest.approx(1.0)


# Test 24: advanced_operations.ln negative
def test_advanced_operations_ln_negative():
    """Test advanced_operations.ln(-1) raises ValueError."""
    from src import advanced_operations
    with pytest.raises(ValueError):
        advanced_operations.ln(-1)


# Test 25: Calculator has all 12 methods
def test_calculator_has_all_12_methods():
    """Verify Calculator exposes all 12 operations as methods."""
    from src.calculator import Calculator
    calc = Calculator()
    expected_methods = [
        "add", "subtract", "multiply", "divide",
        "square", "cube", "square_root", "cube_root",
        "factorial", "power", "log", "ln"
    ]
    for method in expected_methods:
        assert hasattr(calc, method), f"Calculator missing method: {method}"


# Test 26: Calculator history recording still works
def test_calculator_history_after_refactoring():
    """Verify Calculator history recording still works after refactoring."""
    from src.calculator import Calculator
    calc = Calculator()
    result = calc.add(5, 3)
    history = calc.get_history()
    assert len(history) == 1
    assert history[0]["operation"] == "add"
    assert history[0]["operands"] == [5, 3]
    assert history[0]["result"] == 8


# Test 27: OPERATIONS registry complete
def test_operations_registry_complete():
    """Verify OPERATIONS dict has all 12 operations."""
    from src.interface import OPERATIONS
    expected_keys = {"+", "-", "*", "/", "square", "cube", "sqrt", "cbrt", "factorial", "power", "log", "ln"}
    assert set(OPERATIONS.keys()) == expected_keys


# Test 28: Calculator available from calculator_core
def test_calculator_core_class_available():
    """Verify Calculator class available from calculator_core."""
    from src.calculator_core import Calculator
    c = Calculator()
    assert isinstance(c, Calculator)


# Test 29: basic_operations module has expected functions
def test_basic_operations_module_has_expected_functions():
    """Verify basic_operations has all 4 functions."""
    from src import basic_operations
    expected_functions = ["add", "subtract", "multiply", "divide"]
    for func_name in expected_functions:
        assert hasattr(basic_operations, func_name), f"basic_operations missing: {func_name}"
        assert callable(getattr(basic_operations, func_name))


# Test 30: advanced_operations module has expected functions
def test_advanced_operations_module_has_expected_functions():
    """Verify advanced_operations has all 8 functions."""
    from src import advanced_operations
    expected_functions = [
        "square", "cube", "square_root", "cube_root",
        "factorial", "power", "log", "ln"
    ]
    for func_name in expected_functions:
        assert hasattr(advanced_operations, func_name), f"advanced_operations missing: {func_name}"
        assert callable(getattr(advanced_operations, func_name))
