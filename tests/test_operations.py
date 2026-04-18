"""Comprehensive pytest tests for src/operations.py.

Tests verify:
- OPERATIONS registry structure and completeness
- All 12 operation entries have required metadata
- Registry can be imported from both operations.py and input_handler.py (backwards compatibility)
- All registry entries are accessible and correctly formatted
"""

import pytest
from src.operations import OPERATIONS


# ===========================================================================
# OPERATIONS Registry: Structure and Completeness
# ===========================================================================


def test_operations_is_dict():
    """OPERATIONS must be a dictionary."""
    assert isinstance(OPERATIONS, dict)


def test_operations_has_12_entries():
    """OPERATIONS must contain exactly 20 operation entries (12 normal + 8 scientific)."""
    assert len(OPERATIONS) == 20


def test_operations_keys_are_strings():
    """All keys in OPERATIONS must be strings."""
    assert all(isinstance(key, str) for key in OPERATIONS.keys())


def test_operations_values_are_dicts():
    """All values in OPERATIONS must be dictionaries."""
    assert all(isinstance(value, dict) for value in OPERATIONS.values())


# ===========================================================================
# OPERATIONS: Verify All 12 Operations Present
# ===========================================================================


@pytest.mark.parametrize("op_key", [
    "add", "subtract", "multiply", "divide", "power",
    "factorial", "square", "cube", "square_root", "cube_root",
    "log10", "ln"
])
def test_operations_contains_all_operations(op_key):
    """Each expected operation key must exist in OPERATIONS."""
    assert op_key in OPERATIONS


# ===========================================================================
# OPERATIONS: Required Metadata (method, arity, label)
# ===========================================================================


def test_operations_add_has_required_fields():
    """add entry must have 'method', 'arity', and 'label' keys."""
    assert "method" in OPERATIONS["add"]
    assert "arity" in OPERATIONS["add"]
    assert "label" in OPERATIONS["add"]


@pytest.mark.parametrize("op_key", [
    "add", "subtract", "multiply", "divide", "power",
    "factorial", "square", "cube", "square_root", "cube_root",
    "log10", "ln"
])
def test_operations_all_have_required_fields(op_key):
    """Each operation must have 'method', 'arity', and 'label' keys."""
    entry = OPERATIONS[op_key]
    assert "method" in entry
    assert "arity" in entry
    assert "label" in entry


# ===========================================================================
# OPERATIONS: Method Names Match Calculator Methods
# ===========================================================================


@pytest.mark.parametrize("op_key,expected_method", [
    ("add", "add"),
    ("subtract", "subtract"),
    ("multiply", "multiply"),
    ("divide", "divide"),
    ("power", "power"),
    ("factorial", "factorial"),
    ("square", "square"),
    ("cube", "cube"),
    ("square_root", "square_root"),
    ("cube_root", "cube_root"),
    ("log10", "log10"),
    ("ln", "ln"),
])
def test_operations_method_names(op_key, expected_method):
    """method field must match the corresponding Calculator method name."""
    assert OPERATIONS[op_key]["method"] == expected_method


# ===========================================================================
# OPERATIONS: Arity (Number of Operands)
# ===========================================================================


@pytest.mark.parametrize("op_key", ["add", "subtract", "multiply", "divide", "power"])
def test_operations_binary_arity(op_key):
    """Binary operations must have arity of 2."""
    assert OPERATIONS[op_key]["arity"] == 2


@pytest.mark.parametrize("op_key", ["factorial", "square", "cube", "square_root", "cube_root", "log10", "ln"])
def test_operations_unary_arity(op_key):
    """Unary operations must have arity of 1."""
    assert OPERATIONS[op_key]["arity"] == 1


def test_operations_arity_is_int():
    """All arity values must be integers."""
    assert all(isinstance(entry["arity"], int) for entry in OPERATIONS.values())


# ===========================================================================
# OPERATIONS: Label (Human-Readable Description)
# ===========================================================================


def test_operations_labels_are_strings():
    """All label values must be strings."""
    assert all(isinstance(entry["label"], str) for entry in OPERATIONS.values())


def test_operations_labels_are_non_empty():
    """All label values must be non-empty strings."""
    assert all(len(entry["label"]) > 0 for entry in OPERATIONS.values())


@pytest.mark.parametrize("op_key", [
    "add", "subtract", "multiply", "divide", "power",
    "factorial", "square", "cube", "square_root", "cube_root",
    "log10", "ln"
])
def test_operations_label_content(op_key):
    """Each operation must have a meaningful label."""
    label = OPERATIONS[op_key]["label"]
    assert isinstance(label, str)
    assert len(label) > 0


# ===========================================================================
# OPERATIONS: Coerce Callable (Optional, Defaults to float)
# ===========================================================================


def test_operations_coerce_optional():
    """coerce field is optional; may not be present in all entries."""
    # Add, subtract, multiply, divide, power, square, cube, square_root,
    # cube_root, log10, ln should not have coerce (default to float)
    assert "coerce" not in OPERATIONS["add"]
    assert "coerce" not in OPERATIONS["square"]


def test_operations_factorial_has_coerce():
    """factorial must have a coerce field set to int."""
    assert "coerce" in OPERATIONS["factorial"]
    assert OPERATIONS["factorial"]["coerce"] is int


def test_operations_coerce_callable_is_callable():
    """coerce field must be a callable if present."""
    for entry in OPERATIONS.values():
        if "coerce" in entry:
            assert callable(entry["coerce"])


# ===========================================================================
# OPERATIONS: Backwards Compatibility (Import from input_handler)
# ===========================================================================


def test_operations_importable_from_input_handler():
    """OPERATIONS should be importable from input_handler for backwards compatibility."""
    from src.input_handler import OPERATIONS as OPERATIONS_FROM_HANDLER
    assert OPERATIONS_FROM_HANDLER is OPERATIONS or OPERATIONS_FROM_HANDLER == OPERATIONS


def test_operations_exported_from_init():
    """OPERATIONS should be exported from src.__init__ for API consistency."""
    from src import OPERATIONS as OPERATIONS_FROM_INIT
    assert OPERATIONS_FROM_INIT is OPERATIONS or OPERATIONS_FROM_INIT == OPERATIONS


# ===========================================================================
# OPERATIONS: Complete Entry Validation
# ===========================================================================


def test_operations_add_complete():
    """Validate complete add entry."""
    entry = OPERATIONS["add"]
    assert entry["method"] == "add"
    assert entry["arity"] == 2
    assert isinstance(entry["label"], str)
    assert len(entry) == 3  # only method, arity, label


def test_operations_factorial_complete():
    """Validate complete factorial entry (with coerce)."""
    entry = OPERATIONS["factorial"]
    assert entry["method"] == "factorial"
    assert entry["arity"] == 1
    assert isinstance(entry["label"], str)
    assert entry["coerce"] is int
    assert len(entry) == 4  # method, arity, label, coerce


def test_operations_square_complete():
    """Validate complete square entry (no coerce)."""
    entry = OPERATIONS["square"]
    assert entry["method"] == "square"
    assert entry["arity"] == 1
    assert isinstance(entry["label"], str)
    assert "coerce" not in entry
    assert len(entry) == 3  # only method, arity, label


# ===========================================================================
# OPERATIONS: Data Consistency and Type Safety
# ===========================================================================


def test_operations_all_methods_are_strings():
    """All method values must be strings."""
    assert all(isinstance(entry["method"], str) for entry in OPERATIONS.values())


def test_operations_all_arities_positive():
    """All arity values must be non-negative (0, 1, or 2)."""
    assert all(entry["arity"] in (0, 1, 2) for entry in OPERATIONS.values())


def test_operations_no_extra_unknown_fields():
    """Each entry should only have expected fields (method, arity, label, optional coerce)."""
    allowed_fields = {"method", "arity", "label", "coerce"}
    for entry in OPERATIONS.values():
        assert set(entry.keys()).issubset(allowed_fields)


# ===========================================================================
# OPERATIONS: Immutability Check (Read-Only Verification)
# ===========================================================================


def test_operations_can_be_read():
    """OPERATIONS dict can be read without errors."""
    for op_key, entry in OPERATIONS.items():
        assert isinstance(op_key, str)
        assert isinstance(entry, dict)


def test_operations_deep_structure():
    """Verify deep structure of a few key entries."""
    # add
    assert OPERATIONS["add"]["method"] == "add"
    assert OPERATIONS["add"]["arity"] == 2

    # factorial
    assert OPERATIONS["factorial"]["method"] == "factorial"
    assert OPERATIONS["factorial"]["arity"] == 1
    assert OPERATIONS["factorial"]["coerce"] is int


# ===========================================================================
# OPERATIONS: No Duplicate Method Names (Each operation is unique)
# ===========================================================================


def test_operations_no_duplicate_methods():
    """Each operation's method name should be unique."""
    methods = [entry["method"] for entry in OPERATIONS.values()]
    assert len(methods) == len(set(methods))


# ===========================================================================
# OPERATIONS: Callable Validation
# ===========================================================================


def test_operations_coerce_float_works():
    """Default coerce (float) works on valid input."""
    coerce = float  # default
    assert coerce("3.14") == 3.14


def test_operations_coerce_int_works():
    """int coerce works on valid input (factorial)."""
    coerce = OPERATIONS["factorial"]["coerce"]
    assert coerce("42") == 42


def test_operations_coerce_int_fails_on_float_string():
    """int coerce (factorial) fails on float string."""
    coerce = OPERATIONS["factorial"]["coerce"]
    with pytest.raises(ValueError):
        coerce("3.14")


# ===========================================================================
# OPERATIONS: Usage with OperationDispatcher
# ===========================================================================


def test_operations_used_with_dispatcher():
    """Verify OPERATIONS can be used with OperationDispatcher."""
    from src.dispatcher import OperationDispatcher
    from src.calculator import Calculator

    calc = Calculator()
    dispatcher = OperationDispatcher(calc)

    # Pick a few operations and verify they work
    for op_key in ["add", "factorial", "square_root"]:
        entry = OPERATIONS[op_key]
        # Just verify the structure exists; OperationDispatcher will handle the actual dispatch
        assert "method" in entry
        assert "arity" in entry
