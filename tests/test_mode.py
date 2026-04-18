"""Tests for src/mode.py.

Tests the Mode enum and operation set retrieval functions that define
the calculator's operating modes and available operations.
"""

from __future__ import annotations

import pytest

from src.mode import (
    Mode,
    get_normal_operations,
    get_scientific_operations,
    get_operations_for_mode,
    _NORMAL_OPERATIONS,
    _SCIENTIFIC_OPERATIONS,
)


# ---------------------------------------------------------------------------
# Mode enum tests
# ---------------------------------------------------------------------------


class TestModeEnum:
    """Tests for the Mode enum."""

    def test_mode_normal_value(self) -> None:
        """Mode.NORMAL must have value 'normal'."""
        assert Mode.NORMAL.value == "normal"

    def test_mode_scientific_value(self) -> None:
        """Mode.SCIENTIFIC must have value 'scientific'."""
        assert Mode.SCIENTIFIC.value == "scientific"

    def test_mode_normal_is_enum_member(self) -> None:
        """Mode.NORMAL must be a Mode enum member."""
        assert isinstance(Mode.NORMAL, Mode)

    def test_mode_scientific_is_enum_member(self) -> None:
        """Mode.SCIENTIFIC must be a Mode enum member."""
        assert isinstance(Mode.SCIENTIFIC, Mode)

    def test_mode_members_count(self) -> None:
        """Mode enum must have exactly 2 members."""
        assert len(Mode.__members__) == 2

    def test_mode_members_names(self) -> None:
        """Mode enum members must be NORMAL and SCIENTIFIC."""
        assert set(Mode.__members__.keys()) == {"NORMAL", "SCIENTIFIC"}

    def test_mode_normal_not_equal_scientific(self) -> None:
        """Mode.NORMAL must not equal Mode.SCIENTIFIC."""
        assert Mode.NORMAL != Mode.SCIENTIFIC

    def test_mode_normal_equals_itself(self) -> None:
        """Mode.NORMAL must equal Mode.NORMAL."""
        assert Mode.NORMAL == Mode.NORMAL


# ---------------------------------------------------------------------------
# get_normal_operations tests
# ---------------------------------------------------------------------------


class TestGetNormalOperations:
    """Tests for get_normal_operations()."""

    def test_returns_frozenset(self) -> None:
        """get_normal_operations must return a frozenset."""
        result = get_normal_operations()
        assert isinstance(result, frozenset)

    def test_contains_four_operations(self) -> None:
        """get_normal_operations must return exactly 4 operations."""
        result = get_normal_operations()
        assert len(result) == 4

    def test_contains_add(self) -> None:
        """get_normal_operations must include 'add'."""
        result = get_normal_operations()
        assert "add" in result

    def test_contains_subtract(self) -> None:
        """get_normal_operations must include 'subtract'."""
        result = get_normal_operations()
        assert "subtract" in result

    def test_contains_multiply(self) -> None:
        """get_normal_operations must include 'multiply'."""
        result = get_normal_operations()
        assert "multiply" in result

    def test_contains_divide(self) -> None:
        """get_normal_operations must include 'divide'."""
        result = get_normal_operations()
        assert "divide" in result

    def test_does_not_contain_power(self) -> None:
        """get_normal_operations must not include 'power'."""
        result = get_normal_operations()
        assert "power" not in result

    def test_does_not_contain_factorial(self) -> None:
        """get_normal_operations must not include 'factorial'."""
        result = get_normal_operations()
        assert "factorial" not in result

    def test_does_not_contain_square(self) -> None:
        """get_normal_operations must not include 'square'."""
        result = get_normal_operations()
        assert "square" not in result

    def test_does_not_contain_log(self) -> None:
        """get_normal_operations must not include 'log'."""
        result = get_normal_operations()
        assert "log" not in result

    def test_all_strings(self) -> None:
        """All elements in get_normal_operations must be strings."""
        result = get_normal_operations()
        assert all(isinstance(op, str) for op in result)

    def test_consistent_across_calls(self) -> None:
        """get_normal_operations must return the same set each time."""
        result1 = get_normal_operations()
        result2 = get_normal_operations()
        assert result1 == result2

    def test_immutable_frozenset(self) -> None:
        """Returned frozenset must be immutable."""
        result = get_normal_operations()
        with pytest.raises(AttributeError):
            result.add("invalid")


# ---------------------------------------------------------------------------
# get_scientific_operations tests
# ---------------------------------------------------------------------------


class TestGetScientificOperations:
    """Tests for get_scientific_operations()."""

    def test_returns_frozenset(self) -> None:
        """get_scientific_operations must return a frozenset."""
        result = get_scientific_operations()
        assert isinstance(result, frozenset)

    def test_contains_twelve_operations(self) -> None:
        """get_scientific_operations must return 12 operations."""
        result = get_scientific_operations()
        assert len(result) == 12

    def test_contains_all_normal_operations(self) -> None:
        """get_scientific_operations must include all normal operations."""
        scientific = get_scientific_operations()
        normal = get_normal_operations()
        assert normal.issubset(scientific)

    def test_contains_power(self) -> None:
        """get_scientific_operations must include 'power'."""
        result = get_scientific_operations()
        assert "power" in result

    def test_contains_factorial(self) -> None:
        """get_scientific_operations must include 'factorial'."""
        result = get_scientific_operations()
        assert "factorial" in result

    def test_contains_square(self) -> None:
        """get_scientific_operations must include 'square'."""
        result = get_scientific_operations()
        assert "square" in result

    def test_contains_cube(self) -> None:
        """get_scientific_operations must include 'cube'."""
        result = get_scientific_operations()
        assert "cube" in result

    def test_contains_square_root(self) -> None:
        """get_scientific_operations must include 'square_root'."""
        result = get_scientific_operations()
        assert "square_root" in result

    def test_contains_cube_root(self) -> None:
        """get_scientific_operations must include 'cube_root'."""
        result = get_scientific_operations()
        assert "cube_root" in result

    def test_contains_log(self) -> None:
        """get_scientific_operations must include 'log'."""
        result = get_scientific_operations()
        assert "log" in result

    def test_contains_ln(self) -> None:
        """get_scientific_operations must include 'ln'."""
        result = get_scientific_operations()
        assert "ln" in result

    def test_all_strings(self) -> None:
        """All elements in get_scientific_operations must be strings."""
        result = get_scientific_operations()
        assert all(isinstance(op, str) for op in result)

    def test_consistent_across_calls(self) -> None:
        """get_scientific_operations must return the same set each time."""
        result1 = get_scientific_operations()
        result2 = get_scientific_operations()
        assert result1 == result2

    def test_superset_of_normal(self) -> None:
        """Scientific operations must be a true superset of normal operations."""
        scientific = get_scientific_operations()
        normal = get_normal_operations()
        assert scientific.issuperset(normal)
        assert scientific != normal

    def test_immutable_frozenset(self) -> None:
        """Returned frozenset must be immutable."""
        result = get_scientific_operations()
        with pytest.raises(AttributeError):
            result.add("invalid")

    def test_contains_expected_count(self) -> None:
        """Scientific operations should contain 8 additional ops beyond normal 4."""
        scientific = get_scientific_operations()
        normal = get_normal_operations()
        additional = scientific - normal
        assert len(additional) == 8


# ---------------------------------------------------------------------------
# get_operations_for_mode tests
# ---------------------------------------------------------------------------


class TestGetOperationsForMode:
    """Tests for get_operations_for_mode()."""

    def test_normal_mode_returns_normal_operations(self) -> None:
        """get_operations_for_mode(Mode.NORMAL) must return normal operations."""
        result = get_operations_for_mode(Mode.NORMAL)
        assert result == get_normal_operations()

    def test_scientific_mode_returns_scientific_operations(self) -> None:
        """get_operations_for_mode(Mode.SCIENTIFIC) must return scientific operations."""
        result = get_operations_for_mode(Mode.SCIENTIFIC)
        assert result == get_scientific_operations()

    def test_returns_frozenset_for_normal(self) -> None:
        """get_operations_for_mode(Mode.NORMAL) must return a frozenset."""
        result = get_operations_for_mode(Mode.NORMAL)
        assert isinstance(result, frozenset)

    def test_returns_frozenset_for_scientific(self) -> None:
        """get_operations_for_mode(Mode.SCIENTIFIC) must return a frozenset."""
        result = get_operations_for_mode(Mode.SCIENTIFIC)
        assert isinstance(result, frozenset)

    def test_raises_value_error_for_none(self) -> None:
        """get_operations_for_mode(None) must raise ValueError."""
        with pytest.raises(ValueError):
            get_operations_for_mode(None)  # type: ignore

    def test_raises_value_error_for_invalid_type(self) -> None:
        """get_operations_for_mode('normal') (string) must raise ValueError."""
        with pytest.raises(ValueError):
            get_operations_for_mode("normal")  # type: ignore

    def test_raises_value_error_for_int(self) -> None:
        """get_operations_for_mode(1) (int) must raise ValueError."""
        with pytest.raises(ValueError):
            get_operations_for_mode(1)  # type: ignore

    def test_error_message_contains_unknown_mode(self) -> None:
        """ValueError message must mention 'Unknown mode'."""
        with pytest.raises(ValueError, match="Unknown mode"):
            get_operations_for_mode("invalid")  # type: ignore

    def test_consistent_for_normal(self) -> None:
        """Multiple calls with Mode.NORMAL must return same set."""
        result1 = get_operations_for_mode(Mode.NORMAL)
        result2 = get_operations_for_mode(Mode.NORMAL)
        assert result1 == result2

    def test_consistent_for_scientific(self) -> None:
        """Multiple calls with Mode.SCIENTIFIC must return same set."""
        result1 = get_operations_for_mode(Mode.SCIENTIFIC)
        result2 = get_operations_for_mode(Mode.SCIENTIFIC)
        assert result1 == result2

    def test_normal_mode_four_operations(self) -> None:
        """Mode.NORMAL must provide exactly 4 operations."""
        result = get_operations_for_mode(Mode.NORMAL)
        assert len(result) == 4

    def test_scientific_mode_twelve_operations(self) -> None:
        """Mode.SCIENTIFIC must provide exactly 12 operations."""
        result = get_operations_for_mode(Mode.SCIENTIFIC)
        assert len(result) == 12

    def test_identity_with_get_normal_operations(self) -> None:
        """get_operations_for_mode(Mode.NORMAL) is get_normal_operations()."""
        mode_result = get_operations_for_mode(Mode.NORMAL)
        direct_result = get_normal_operations()
        # Should be the same object (singleton behavior)
        assert mode_result is direct_result

    def test_identity_with_get_scientific_operations(self) -> None:
        """get_operations_for_mode(Mode.SCIENTIFIC) is get_scientific_operations()."""
        mode_result = get_operations_for_mode(Mode.SCIENTIFIC)
        direct_result = get_scientific_operations()
        # Should be the same object (singleton behavior)
        assert mode_result is direct_result


# ---------------------------------------------------------------------------
# Internal constants tests
# ---------------------------------------------------------------------------


class TestInternalConstants:
    """Tests for internal _NORMAL_OPERATIONS and _SCIENTIFIC_OPERATIONS."""

    def test_normal_operations_is_frozenset(self) -> None:
        """_NORMAL_OPERATIONS must be a frozenset."""
        assert isinstance(_NORMAL_OPERATIONS, frozenset)

    def test_scientific_operations_is_frozenset(self) -> None:
        """_SCIENTIFIC_OPERATIONS must be a frozenset."""
        assert isinstance(_SCIENTIFIC_OPERATIONS, frozenset)

    def test_normal_operations_count(self) -> None:
        """_NORMAL_OPERATIONS must contain exactly 4 operations."""
        assert len(_NORMAL_OPERATIONS) == 4

    def test_scientific_operations_count(self) -> None:
        """_SCIENTIFIC_OPERATIONS must contain exactly 12 operations."""
        assert len(_SCIENTIFIC_OPERATIONS) == 12

    def test_normal_is_subset_of_scientific(self) -> None:
        """_NORMAL_OPERATIONS must be a subset of _SCIENTIFIC_OPERATIONS."""
        assert _NORMAL_OPERATIONS.issubset(_SCIENTIFIC_OPERATIONS)
