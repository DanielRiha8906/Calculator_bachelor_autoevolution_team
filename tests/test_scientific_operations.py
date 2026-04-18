"""Comprehensive pytest tests for scientific operations in Calculator.

Tests verify:
- Calculator trigonometric methods (sin, cos, tan, asin, acos, atan)
- Calculator constant methods (get_pi, get_e)
- Domain validation for inverse trig functions (asin, acos)
- SCIENTIFIC_OPERATIONS registry structure (8 entries)
- Each entry has required fields: method, arity, label
- Correct arity values (1 for trig, 0 for constants)
- All method names map to existing Calculator methods
"""

import math
import pytest
from src.core.calculator import Calculator
from src.operations.scientific import SCIENTIFIC_OPERATIONS


# ===========================================================================
# SCIENTIFIC_OPERATIONS Registry: Structure and Entries
# ===========================================================================

def test_scientific_operations_is_dict():
    """SCIENTIFIC_OPERATIONS must be a dictionary."""
    assert isinstance(SCIENTIFIC_OPERATIONS, dict)


def test_scientific_operations_has_8_entries():
    """SCIENTIFIC_OPERATIONS must contain exactly 8 entries."""
    assert len(SCIENTIFIC_OPERATIONS) == 8


def test_scientific_operations_keys_are_strings():
    """All keys in SCIENTIFIC_OPERATIONS must be strings."""
    assert all(isinstance(key, str) for key in SCIENTIFIC_OPERATIONS.keys())


def test_scientific_operations_values_are_dicts():
    """All values in SCIENTIFIC_OPERATIONS must be dictionaries."""
    assert all(isinstance(value, dict) for value in SCIENTIFIC_OPERATIONS.values())


def test_scientific_operations_expected_keys():
    """SCIENTIFIC_OPERATIONS must contain exactly the expected 8 keys."""
    expected_keys = {"sin", "cos", "tan", "asin", "acos", "atan", "pi", "e"}
    assert set(SCIENTIFIC_OPERATIONS.keys()) == expected_keys


# ===========================================================================
# SCIENTIFIC_OPERATIONS: Trig Functions (sin, cos, tan, asin, acos, atan)
# ===========================================================================

@pytest.mark.parametrize("op_key", ["sin", "cos", "tan", "asin", "acos", "atan"])
def test_scientific_trig_functions_exist(op_key):
    """Each trig function key must exist in SCIENTIFIC_OPERATIONS."""
    assert op_key in SCIENTIFIC_OPERATIONS


@pytest.mark.parametrize("op_key", ["sin", "cos", "tan", "asin", "acos", "atan"])
def test_scientific_trig_has_required_fields(op_key):
    """Each trig function must have method, arity, and label fields."""
    entry = SCIENTIFIC_OPERATIONS[op_key]
    assert "method" in entry
    assert "arity" in entry
    assert "label" in entry


@pytest.mark.parametrize("op_key", ["sin", "cos", "tan", "asin", "acos", "atan"])
def test_scientific_trig_arity_is_1(op_key):
    """All trig functions must have arity=1."""
    entry = SCIENTIFIC_OPERATIONS[op_key]
    assert entry["arity"] == 1


@pytest.mark.parametrize("op_key,expected_method", [
    ("sin", "sin"),
    ("cos", "cos"),
    ("tan", "tan"),
    ("asin", "asin"),
    ("acos", "acos"),
    ("atan", "atan"),
])
def test_scientific_trig_method_names(op_key, expected_method):
    """Trig function method field must match the Calculator method name."""
    entry = SCIENTIFIC_OPERATIONS[op_key]
    assert entry["method"] == expected_method


# ===========================================================================
# SCIENTIFIC_OPERATIONS: Constants (pi, e)
# ===========================================================================

@pytest.mark.parametrize("op_key", ["pi", "e"])
def test_scientific_constants_exist(op_key):
    """Each constant key (pi, e) must exist in SCIENTIFIC_OPERATIONS."""
    assert op_key in SCIENTIFIC_OPERATIONS


@pytest.mark.parametrize("op_key", ["pi", "e"])
def test_scientific_constants_has_required_fields(op_key):
    """Each constant must have method, arity, and label fields."""
    entry = SCIENTIFIC_OPERATIONS[op_key]
    assert "method" in entry
    assert "arity" in entry
    assert "label" in entry


@pytest.mark.parametrize("op_key", ["pi", "e"])
def test_scientific_constants_arity_is_0(op_key):
    """All constants (pi, e) must have arity=0."""
    entry = SCIENTIFIC_OPERATIONS[op_key]
    assert entry["arity"] == 0


@pytest.mark.parametrize("op_key,expected_method", [
    ("pi", "get_pi"),
    ("e", "get_e"),
])
def test_scientific_constants_method_names(op_key, expected_method):
    """Constant method field must match the Calculator getter method name."""
    entry = SCIENTIFIC_OPERATIONS[op_key]
    assert entry["method"] == expected_method


# ===========================================================================
# SCIENTIFIC_OPERATIONS: Labels and Metadata
# ===========================================================================

def test_scientific_operations_all_labels_are_strings():
    """All label values must be strings."""
    assert all(isinstance(entry["label"], str) for entry in SCIENTIFIC_OPERATIONS.values())


def test_scientific_operations_all_labels_are_non_empty():
    """All label values must be non-empty strings."""
    assert all(len(entry["label"]) > 0 for entry in SCIENTIFIC_OPERATIONS.values())


def test_scientific_operations_all_methods_are_strings():
    """All method values must be strings."""
    assert all(isinstance(entry["method"], str) for entry in SCIENTIFIC_OPERATIONS.values())


def test_scientific_operations_all_arities_are_non_negative_ints():
    """All arity values must be non-negative integers."""
    assert all(isinstance(entry["arity"], int) and entry["arity"] >= 0
               for entry in SCIENTIFIC_OPERATIONS.values())


def test_scientific_operations_arity_values_in_valid_range():
    """All arity values must be 0 or 1 (no binary operations in scientific)."""
    assert all(entry["arity"] in (0, 1) for entry in SCIENTIFIC_OPERATIONS.values())


# ===========================================================================
# SCIENTIFIC_OPERATIONS: No Extra Fields
# ===========================================================================

def test_scientific_operations_no_unexpected_fields():
    """Each entry should only have expected fields (method, arity, label, optional coerce)."""
    allowed_fields = {"method", "arity", "label", "coerce"}
    for key, entry in SCIENTIFIC_OPERATIONS.items():
        assert set(entry.keys()).issubset(allowed_fields), f"Unexpected fields in {key}"


# ===========================================================================
# Calculator: sin method
# ===========================================================================

def test_calculator_sin_zero():
    """sin(0) must equal 0."""
    calc = Calculator()
    assert calc.sin(0) == 0.0


def test_calculator_sin_pi_half():
    """sin(pi/2) must be approximately 1.0."""
    calc = Calculator()
    result = calc.sin(math.pi / 2)
    assert result == pytest.approx(1.0, abs=1e-10)


def test_calculator_sin_pi():
    """sin(pi) must be approximately 0."""
    calc = Calculator()
    result = calc.sin(math.pi)
    assert result == pytest.approx(0.0, abs=1e-10)


def test_calculator_sin_negative_value():
    """sin(-pi/2) must be approximately -1.0."""
    calc = Calculator()
    result = calc.sin(-math.pi / 2)
    assert result == pytest.approx(-1.0, abs=1e-10)


def test_calculator_sin_small_angle():
    """sin(0.1) must be approximately 0.1."""
    calc = Calculator()
    result = calc.sin(0.1)
    assert result == pytest.approx(0.0998334, rel=1e-5)


# ===========================================================================
# Calculator: cos method
# ===========================================================================

def test_calculator_cos_zero():
    """cos(0) must equal 1."""
    calc = Calculator()
    assert calc.cos(0) == 1.0


def test_calculator_cos_pi_half():
    """cos(pi/2) must be approximately 0."""
    calc = Calculator()
    result = calc.cos(math.pi / 2)
    assert result == pytest.approx(0.0, abs=1e-10)


def test_calculator_cos_pi():
    """cos(pi) must be approximately -1."""
    calc = Calculator()
    result = calc.cos(math.pi)
    assert result == pytest.approx(-1.0, abs=1e-10)


def test_calculator_cos_negative_value():
    """cos(-pi) must be approximately -1."""
    calc = Calculator()
    result = calc.cos(-math.pi)
    assert result == pytest.approx(-1.0, abs=1e-10)


# ===========================================================================
# Calculator: tan method
# ===========================================================================

def test_calculator_tan_zero():
    """tan(0) must equal 0."""
    calc = Calculator()
    assert calc.tan(0) == 0.0


def test_calculator_tan_pi_quarter():
    """tan(pi/4) must be approximately 1."""
    calc = Calculator()
    result = calc.tan(math.pi / 4)
    assert result == pytest.approx(1.0, abs=1e-10)


def test_calculator_tan_negative_value():
    """tan(-pi/4) must be approximately -1."""
    calc = Calculator()
    result = calc.tan(-math.pi / 4)
    assert result == pytest.approx(-1.0, abs=1e-10)


# ===========================================================================
# Calculator: asin method (domain validation)
# ===========================================================================

def test_calculator_asin_zero():
    """asin(0) must equal 0."""
    calc = Calculator()
    assert calc.asin(0.0) == 0.0


def test_calculator_asin_one():
    """asin(1.0) must be approximately pi/2."""
    calc = Calculator()
    result = calc.asin(1.0)
    assert result == pytest.approx(math.pi / 2, abs=1e-10)


def test_calculator_asin_negative_one():
    """asin(-1.0) must be approximately -pi/2."""
    calc = Calculator()
    result = calc.asin(-1.0)
    assert result == pytest.approx(-math.pi / 2, abs=1e-10)


def test_calculator_asin_half():
    """asin(0.5) must be approximately pi/6."""
    calc = Calculator()
    result = calc.asin(0.5)
    assert result == pytest.approx(math.pi / 6, rel=1e-10)


def test_calculator_asin_domain_error_above_1():
    """asin(1.5) must raise ValueError (domain error)."""
    calc = Calculator()
    with pytest.raises(ValueError, match="asin.*not defined"):
        calc.asin(1.5)


def test_calculator_asin_domain_error_below_minus_1():
    """asin(-1.5) must raise ValueError (domain error)."""
    calc = Calculator()
    with pytest.raises(ValueError, match="asin.*not defined"):
        calc.asin(-1.5)


def test_calculator_asin_just_above_boundary():
    """asin(1.00001) must raise ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.asin(1.00001)


def test_calculator_asin_just_below_negative_boundary():
    """asin(-1.00001) must raise ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.asin(-1.00001)


def test_calculator_asin_at_boundary_1():
    """asin(1.0) must be valid (at boundary)."""
    calc = Calculator()
    result = calc.asin(1.0)
    assert result == pytest.approx(math.pi / 2, abs=1e-10)


def test_calculator_asin_at_boundary_minus_1():
    """asin(-1.0) must be valid (at boundary)."""
    calc = Calculator()
    result = calc.asin(-1.0)
    assert result == pytest.approx(-math.pi / 2, abs=1e-10)


# ===========================================================================
# Calculator: acos method (domain validation)
# ===========================================================================

def test_calculator_acos_zero():
    """acos(0.0) must be approximately pi/2."""
    calc = Calculator()
    result = calc.acos(0.0)
    assert result == pytest.approx(math.pi / 2, abs=1e-10)


def test_calculator_acos_one():
    """acos(1.0) must be approximately 0."""
    calc = Calculator()
    result = calc.acos(1.0)
    assert result == pytest.approx(0.0, abs=1e-10)


def test_calculator_acos_negative_one():
    """acos(-1.0) must be approximately pi."""
    calc = Calculator()
    result = calc.acos(-1.0)
    assert result == pytest.approx(math.pi, abs=1e-10)


def test_calculator_acos_half():
    """acos(0.5) must be approximately pi/3."""
    calc = Calculator()
    result = calc.acos(0.5)
    assert result == pytest.approx(math.pi / 3, rel=1e-10)


def test_calculator_acos_domain_error_above_1():
    """acos(1.5) must raise ValueError (domain error)."""
    calc = Calculator()
    with pytest.raises(ValueError, match="acos.*not defined"):
        calc.acos(1.5)


def test_calculator_acos_domain_error_below_minus_1():
    """acos(-1.5) must raise ValueError (domain error)."""
    calc = Calculator()
    with pytest.raises(ValueError, match="acos.*not defined"):
        calc.acos(-1.5)


def test_calculator_acos_just_above_boundary():
    """acos(1.00001) must raise ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.acos(1.00001)


def test_calculator_acos_at_boundary_1():
    """acos(1.0) must be valid (at boundary)."""
    calc = Calculator()
    result = calc.acos(1.0)
    assert result == pytest.approx(0.0, abs=1e-10)


def test_calculator_acos_at_boundary_minus_1():
    """acos(-1.0) must be valid (at boundary)."""
    calc = Calculator()
    result = calc.acos(-1.0)
    assert result == pytest.approx(math.pi, abs=1e-10)


# ===========================================================================
# Calculator: atan method
# ===========================================================================

def test_calculator_atan_zero():
    """atan(0) must equal 0."""
    calc = Calculator()
    assert calc.atan(0.0) == 0.0


def test_calculator_atan_one():
    """atan(1.0) must be approximately pi/4."""
    calc = Calculator()
    result = calc.atan(1.0)
    assert result == pytest.approx(math.pi / 4, abs=1e-10)


def test_calculator_atan_negative_one():
    """atan(-1.0) must be approximately -pi/4."""
    calc = Calculator()
    result = calc.atan(-1.0)
    assert result == pytest.approx(-math.pi / 4, abs=1e-10)


def test_calculator_atan_large_positive():
    """atan(1000) must be approximately pi/2."""
    calc = Calculator()
    result = calc.atan(1000)
    assert result == pytest.approx(math.pi / 2, abs=0.01)


def test_calculator_atan_large_negative():
    """atan(-1000) must be approximately -pi/2."""
    calc = Calculator()
    result = calc.atan(-1000)
    assert result == pytest.approx(-math.pi / 2, abs=0.01)


def test_calculator_atan_no_domain_limit():
    """atan accepts any real number (no domain restriction)."""
    calc = Calculator()
    # Should not raise for any value
    result = calc.atan(1e100)
    assert isinstance(result, float)


# ===========================================================================
# Calculator: get_pi method
# ===========================================================================

def test_calculator_get_pi():
    """get_pi() must return math.pi."""
    calc = Calculator()
    result = calc.get_pi()
    assert result == math.pi


def test_calculator_get_pi_is_float():
    """get_pi() must return a float."""
    calc = Calculator()
    result = calc.get_pi()
    assert isinstance(result, float)


def test_calculator_get_pi_value():
    """get_pi() must return approximately 3.14159265."""
    calc = Calculator()
    result = calc.get_pi()
    assert result == pytest.approx(3.14159265, rel=1e-8)


def test_calculator_get_pi_takes_no_args():
    """get_pi() takes no arguments."""
    calc = Calculator()
    result = calc.get_pi()
    assert isinstance(result, float)


def test_calculator_get_pi_called_multiple_times():
    """Multiple calls to get_pi() return the same value."""
    calc = Calculator()
    result1 = calc.get_pi()
    result2 = calc.get_pi()
    assert result1 == result2 == math.pi


# ===========================================================================
# Calculator: get_e method
# ===========================================================================

def test_calculator_get_e():
    """get_e() must return math.e."""
    calc = Calculator()
    result = calc.get_e()
    assert result == math.e


def test_calculator_get_e_is_float():
    """get_e() must return a float."""
    calc = Calculator()
    result = calc.get_e()
    assert isinstance(result, float)


def test_calculator_get_e_value():
    """get_e() must return approximately 2.71828182."""
    calc = Calculator()
    result = calc.get_e()
    assert result == pytest.approx(2.71828182, rel=1e-8)


def test_calculator_get_e_takes_no_args():
    """get_e() takes no arguments."""
    calc = Calculator()
    result = calc.get_e()
    assert isinstance(result, float)


def test_calculator_get_e_called_multiple_times():
    """Multiple calls to get_e() return the same value."""
    calc = Calculator()
    result1 = calc.get_e()
    result2 = calc.get_e()
    assert result1 == result2 == math.e


# ===========================================================================
# Integration: All Methods Callable and Methods Exist
# ===========================================================================

@pytest.mark.parametrize("method_name", ["sin", "cos", "tan", "asin", "acos", "atan", "get_pi", "get_e"])
def test_all_scientific_methods_exist_on_calculator(method_name):
    """Each method referenced in SCIENTIFIC_OPERATIONS must exist on Calculator."""
    calc = Calculator()
    assert hasattr(calc, method_name)
    assert callable(getattr(calc, method_name))


# ===========================================================================
# Integration: SCIENTIFIC_OPERATIONS Completeness
# ===========================================================================

def test_scientific_operations_contains_all_8_operations():
    """SCIENTIFIC_OPERATIONS contains all 8 expected operations."""
    expected = {"sin", "cos", "tan", "asin", "acos", "atan", "pi", "e"}
    actual = set(SCIENTIFIC_OPERATIONS.keys())
    assert actual == expected


def test_no_duplicate_method_names_in_scientific():
    """Each operation's method name in SCIENTIFIC_OPERATIONS must be unique."""
    methods = [entry["method"] for entry in SCIENTIFIC_OPERATIONS.values()]
    assert len(methods) == len(set(methods))


def test_scientific_operations_is_not_empty():
    """SCIENTIFIC_OPERATIONS must not be empty (8 entries)."""
    assert len(SCIENTIFIC_OPERATIONS) > 0
    assert len(SCIENTIFIC_OPERATIONS) == 8
