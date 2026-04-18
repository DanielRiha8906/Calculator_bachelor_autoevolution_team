"""Comprehensive pytest tests for src/interface/mode.py.

Tests verify:
- CalculatorMode is an abstract base class that cannot be instantiated
- SimpleMode returns NORMAL_OPERATIONS
- ScientificMode returns OPERATIONS (full registry)
- Mode filtering correctness: all returned operations are valid
"""

import pytest
from abc import ABC

from src.interface.mode import CalculatorMode, SimpleMode, ScientificMode
from src.operations import NORMAL_OPERATIONS, OPERATIONS, SCIENTIFIC_OPERATIONS


# ===========================================================================
# CalculatorMode: Abstract Base Class
# ===========================================================================


def test_calculator_mode_is_abstract():
    """CalculatorMode cannot be instantiated directly."""
    with pytest.raises(TypeError):
        CalculatorMode()


def test_calculator_mode_is_abc():
    """CalculatorMode is an ABC (Abstract Base Class)."""
    assert issubclass(CalculatorMode, ABC)


def test_calculator_mode_has_abstract_method():
    """CalculatorMode declares available_operations as abstract."""
    assert hasattr(CalculatorMode, '__abstractmethods__')
    assert 'available_operations' in CalculatorMode.__abstractmethods__


# ===========================================================================
# SimpleMode: Returns NORMAL_OPERATIONS
# ===========================================================================


def test_simple_mode_can_be_instantiated():
    """SimpleMode can be instantiated without error."""
    mode = SimpleMode()
    assert isinstance(mode, SimpleMode)


def test_simple_mode_is_calculator_mode_subclass():
    """SimpleMode is a subclass of CalculatorMode."""
    assert issubclass(SimpleMode, CalculatorMode)


def test_simple_mode_available_operations_returns_dict():
    """SimpleMode.available_operations() returns a dict."""
    mode = SimpleMode()
    result = mode.available_operations()
    assert isinstance(result, dict)


def test_simple_mode_available_operations_returns_normal_operations():
    """SimpleMode.available_operations() returns NORMAL_OPERATIONS."""
    mode = SimpleMode()
    result = mode.available_operations()
    assert result == NORMAL_OPERATIONS


def test_simple_mode_available_operations_has_expected_keys():
    """SimpleMode returns operations with expected operation names."""
    mode = SimpleMode()
    ops = mode.available_operations()
    expected_keys = {
        "add", "subtract", "multiply", "divide", "power",
        "factorial", "square", "cube", "square_root", "cube_root",
        "log10", "ln"
    }
    assert set(ops.keys()) == expected_keys


def test_simple_mode_no_scientific_operations():
    """SimpleMode does not include scientific-only operations."""
    mode = SimpleMode()
    ops = mode.available_operations()
    # All returned operations must be in NORMAL_OPERATIONS
    for op_key in ops.keys():
        assert op_key in NORMAL_OPERATIONS


def test_simple_mode_operations_all_have_metadata():
    """All operations in SimpleMode have required metadata fields."""
    mode = SimpleMode()
    ops = mode.available_operations()
    for op_key, op_info in ops.items():
        assert "method" in op_info
        assert "arity" in op_info
        assert "label" in op_info


# ===========================================================================
# ScientificMode: Returns Full OPERATIONS
# ===========================================================================


def test_scientific_mode_can_be_instantiated():
    """ScientificMode can be instantiated without error."""
    mode = ScientificMode()
    assert isinstance(mode, ScientificMode)


def test_scientific_mode_is_calculator_mode_subclass():
    """ScientificMode is a subclass of CalculatorMode."""
    assert issubclass(ScientificMode, CalculatorMode)


def test_scientific_mode_available_operations_returns_dict():
    """ScientificMode.available_operations() returns a dict."""
    mode = ScientificMode()
    result = mode.available_operations()
    assert isinstance(result, dict)


def test_scientific_mode_available_operations_returns_operations():
    """ScientificMode.available_operations() returns full OPERATIONS."""
    mode = ScientificMode()
    result = mode.available_operations()
    assert result == OPERATIONS


def test_scientific_mode_includes_normal_operations():
    """ScientificMode includes all normal operations."""
    mode = ScientificMode()
    ops = mode.available_operations()
    for op_key in NORMAL_OPERATIONS.keys():
        assert op_key in ops


def test_scientific_mode_includes_scientific_operations():
    """ScientificMode includes all scientific operations."""
    mode = ScientificMode()
    ops = mode.available_operations()
    for op_key in SCIENTIFIC_OPERATIONS.keys():
        assert op_key in ops


def test_scientific_mode_operations_all_have_metadata():
    """All operations in ScientificMode have required metadata fields."""
    mode = ScientificMode()
    ops = mode.available_operations()
    for op_key, op_info in ops.items():
        assert "method" in op_info
        assert "arity" in op_info
        assert "label" in op_info


# ===========================================================================
# Mode Filtering Correctness
# ===========================================================================


def test_mode_filtering_simple_mode_keys():
    """SimpleMode returns only keys present in NORMAL_OPERATIONS."""
    simple_mode = SimpleMode()
    simple_ops = simple_mode.available_operations()
    for op_key in simple_ops.keys():
        assert op_key in NORMAL_OPERATIONS, f"{op_key} not in NORMAL_OPERATIONS"


def test_mode_filtering_scientific_mode_keys():
    """ScientificMode returns only keys present in OPERATIONS."""
    scientific_mode = ScientificMode()
    scientific_ops = scientific_mode.available_operations()
    for op_key in scientific_ops.keys():
        assert op_key in OPERATIONS, f"{op_key} not in OPERATIONS"


def test_simple_and_scientific_mode_same_when_scientific_empty():
    """When SCIENTIFIC_OPERATIONS is empty, SimpleMode and ScientificMode return the same dict."""
    simple_mode = SimpleMode()
    scientific_mode = ScientificMode()

    simple_ops = simple_mode.available_operations()
    scientific_ops = scientific_mode.available_operations()

    # If SCIENTIFIC_OPERATIONS is empty, both should be equal
    if len(SCIENTIFIC_OPERATIONS) == 0:
        assert simple_ops == scientific_ops


def test_mode_consistency_across_multiple_calls():
    """Calling available_operations() multiple times returns the same dict."""
    simple_mode = SimpleMode()
    scientific_mode = ScientificMode()

    simple_result_1 = simple_mode.available_operations()
    simple_result_2 = simple_mode.available_operations()
    assert simple_result_1 == simple_result_2

    scientific_result_1 = scientific_mode.available_operations()
    scientific_result_2 = scientific_mode.available_operations()
    assert scientific_result_1 == scientific_result_2


# ===========================================================================
# Mode Edge Cases
# ===========================================================================


def test_simple_mode_operations_arity_values():
    """All operations in SimpleMode have valid arity (1 or 2)."""
    mode = SimpleMode()
    ops = mode.available_operations()
    for op_key, op_info in ops.items():
        arity = op_info["arity"]
        assert arity in (1, 2), f"{op_key} has invalid arity {arity}"


def test_scientific_mode_operations_arity_values():
    """All operations in ScientificMode have valid arity (1 or 2)."""
    mode = ScientificMode()
    ops = mode.available_operations()
    for op_key, op_info in ops.items():
        arity = op_info["arity"]
        assert arity in (1, 2), f"{op_key} has invalid arity {arity}"


def test_simple_mode_operations_method_field_is_string():
    """All operation 'method' fields in SimpleMode are non-empty strings."""
    mode = SimpleMode()
    ops = mode.available_operations()
    for op_key, op_info in ops.items():
        method = op_info["method"]
        assert isinstance(method, str), f"{op_key}.method is not a string"
        assert len(method) > 0, f"{op_key}.method is empty"


def test_simple_mode_operations_label_field_is_string():
    """All operation 'label' fields in SimpleMode are non-empty strings."""
    mode = SimpleMode()
    ops = mode.available_operations()
    for op_key, op_info in ops.items():
        label = op_info["label"]
        assert isinstance(label, str), f"{op_key}.label is not a string"
        assert len(label) > 0, f"{op_key}.label is empty"


def test_simple_mode_operations_coerce_field_when_present():
    """When 'coerce' field is present in SimpleMode, it is callable."""
    mode = SimpleMode()
    ops = mode.available_operations()
    for op_key, op_info in ops.items():
        if "coerce" in op_info:
            coerce = op_info["coerce"]
            assert callable(coerce), f"{op_key}.coerce is not callable"


@pytest.mark.parametrize("mode_class", [SimpleMode, ScientificMode])
def test_mode_instantiation_creates_independent_instances(mode_class):
    """Multiple mode instances are independent."""
    mode1 = mode_class()
    mode2 = mode_class()
    assert mode1 is not mode2
    assert mode1.available_operations() == mode2.available_operations()
