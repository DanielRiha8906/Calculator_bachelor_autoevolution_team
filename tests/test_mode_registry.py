"""Tests for mode-aware operation registry and registry size.

Tests that _build_registry() correctly builds registries with the right
operations for normal mode (13 operations) and scientific mode (25 operations).

These tests verify the correct mode split where:
- Normal mode: 13 operations (5 arithmetic + 8 scientific: add, subtract,
  multiply, divide, modulo, factorial, square, cube, square_root, cube_root,
  power, log10, ln)
- Scientific mode: 25 operations (all 13 normal + 12 new: sin, cos, tan, asin,
  acos, atan, sinh, cosh, tanh, exp, pi, e)

See Issue #411 for scientific mode feature details.
"""

import pytest
from src.calculator.main import _build_registry, MODE_NORMAL, MODE_SCIENTIFIC


class TestModeRegistrySize:
    """Tests for registry size in each mode."""

    def test_normal_mode_has_13_operations(self):
        """Test that normal mode registry has exactly 13 operations.

        Input: _build_registry(MODE_NORMAL)
        Expected: Registry contains exactly 13 operation names

        The 13 operations are:
        - Arithmetic: add, subtract, multiply, divide, modulo
        - Advanced: factorial, square, cube, square_root, cube_root, power, log10, ln
        """
        registry = _build_registry(MODE_NORMAL)
        ops = registry.list_all()
        assert len(ops) == 13, (
            f"Normal mode should have 13 operations, got {len(ops)}: {ops}"
        )

    def test_scientific_mode_has_25_operations(self):
        """Test that scientific mode registry has exactly 25 operations.

        Input: _build_registry(MODE_SCIENTIFIC)
        Expected: Registry contains exactly 25 operation names

        The 25 operations are:
        - 13 normal operations
        - 12 new scientific: sin, cos, tan, asin, acos, atan, sinh, cosh,
          tanh, exp, pi, e
        """
        registry = _build_registry(MODE_SCIENTIFIC)
        ops = registry.list_all()
        assert len(ops) == 25, (
            f"Scientific mode should have 25 operations, got {len(ops)}: {ops}"
        )

    def test_default_mode_is_scientific(self):
        """Test that _build_registry() defaults to scientific mode.

        Input: _build_registry() with no mode argument
        Expected: Registry contains 25 operations (scientific mode)

        This ensures backward compatibility with tests that call
        _build_registry() without arguments and expect all operations.
        """
        registry = _build_registry()
        ops = registry.list_all()
        assert len(ops) == 25, (
            f"Default mode should be scientific (25 ops), got {len(ops)}: {ops}"
        )


class TestNormalModeOperations:
    """Tests for operation inclusion in normal mode."""

    def test_normal_mode_includes_basic_arithmetic(self):
        """Test that normal mode includes basic arithmetic operations.

        Input: _build_registry(MODE_NORMAL)
        Expected: Registry contains add, subtract, multiply, divide, modulo
        """
        registry = _build_registry(MODE_NORMAL)
        ops = registry.list_all()
        required_ops = ["add", "subtract", "multiply", "divide", "modulo"]
        for op in required_ops:
            assert op in ops, f"Normal mode missing '{op}'"

    def test_normal_mode_includes_advanced_operations(self):
        """Test that normal mode includes advanced operations.

        Input: _build_registry(MODE_NORMAL)
        Expected: Registry contains factorial, square, cube, square_root,
                 cube_root, power, log10, ln
        """
        registry = _build_registry(MODE_NORMAL)
        ops = registry.list_all()
        required_ops = [
            "factorial", "square", "cube", "square_root", "cube_root",
            "power", "log10", "ln"
        ]
        for op in required_ops:
            assert op in ops, f"Normal mode missing '{op}'"

    def test_normal_mode_excludes_trigonometric_operations(self):
        """Test that normal mode excludes trigonometric operations.

        Input: _build_registry(MODE_NORMAL)
        Expected: Registry does not contain sin, cos, tan, asin, acos, atan
        """
        registry = _build_registry(MODE_NORMAL)
        ops = registry.list_all()
        excluded_ops = ["sin", "cos", "tan", "asin", "acos", "atan"]
        for op in excluded_ops:
            assert op not in ops, f"Normal mode should not have '{op}'"

    def test_normal_mode_excludes_hyperbolic_operations(self):
        """Test that normal mode excludes hyperbolic operations.

        Input: _build_registry(MODE_NORMAL)
        Expected: Registry does not contain sinh, cosh, tanh
        """
        registry = _build_registry(MODE_NORMAL)
        ops = registry.list_all()
        excluded_ops = ["sinh", "cosh", "tanh"]
        for op in excluded_ops:
            assert op not in ops, f"Normal mode should not have '{op}'"

    def test_normal_mode_excludes_exponential_and_constants(self):
        """Test that normal mode excludes exponential and constant operations.

        Input: _build_registry(MODE_NORMAL)
        Expected: Registry does not contain exp, pi, e
        """
        registry = _build_registry(MODE_NORMAL)
        ops = registry.list_all()
        excluded_ops = ["exp", "pi", "e"]
        for op in excluded_ops:
            assert op not in ops, f"Normal mode should not have '{op}'"


class TestScientificModeOperations:
    """Tests for operation inclusion in scientific mode."""

    def test_scientific_mode_includes_all_13_normal_operations(self):
        """Test that scientific mode includes all 13 normal operations.

        Input: _build_registry(MODE_SCIENTIFIC)
        Expected: Registry contains all 13 normal-mode operations
        """
        registry = _build_registry(MODE_SCIENTIFIC)
        ops = registry.list_all()
        required_ops = [
            "add", "subtract", "multiply", "divide", "modulo",
            "factorial", "square", "cube", "square_root", "cube_root",
            "power", "log10", "ln"
        ]
        for op in required_ops:
            assert op in ops, f"Scientific mode missing normal op '{op}'"

    def test_scientific_mode_includes_trigonometric_operations(self):
        """Test that scientific mode includes trigonometric operations.

        Input: _build_registry(MODE_SCIENTIFIC)
        Expected: Registry contains sin, cos, tan, asin, acos, atan
        """
        registry = _build_registry(MODE_SCIENTIFIC)
        ops = registry.list_all()
        required_ops = ["sin", "cos", "tan", "asin", "acos", "atan"]
        for op in required_ops:
            assert op in ops, f"Scientific mode missing '{op}'"

    def test_scientific_mode_includes_hyperbolic_operations(self):
        """Test that scientific mode includes hyperbolic operations.

        Input: _build_registry(MODE_SCIENTIFIC)
        Expected: Registry contains sinh, cosh, tanh
        """
        registry = _build_registry(MODE_SCIENTIFIC)
        ops = registry.list_all()
        required_ops = ["sinh", "cosh", "tanh"]
        for op in required_ops:
            assert op in ops, f"Scientific mode missing '{op}'"

    def test_scientific_mode_includes_exponential_and_constants(self):
        """Test that scientific mode includes exponential and constant operations.

        Input: _build_registry(MODE_SCIENTIFIC)
        Expected: Registry contains exp, pi, e
        """
        registry = _build_registry(MODE_SCIENTIFIC)
        ops = registry.list_all()
        required_ops = ["exp", "pi", "e"]
        for op in required_ops:
            assert op in ops, f"Scientific mode missing '{op}'"


class TestModeRegistrySeparation:
    """Tests for correct separation between modes."""

    def test_all_12_new_operations_not_in_normal_mode(self):
        """Test that all 12 new scientific operations are absent from normal mode.

        Input: _build_registry(MODE_NORMAL)
        Expected: Registry does not contain any of the 12 new operations
        """
        registry = _build_registry(MODE_NORMAL)
        ops = registry.list_all()
        new_ops = [
            "sin", "cos", "tan", "asin", "acos", "atan",
            "sinh", "cosh", "tanh", "exp", "pi", "e"
        ]
        for op in new_ops:
            assert op not in ops, (
                f"Normal mode should not include '{op}' "
                "(it's one of the 12 new scientific operations)"
            )

    def test_all_12_new_operations_in_scientific_mode(self):
        """Test that all 12 new scientific operations are in scientific mode.

        Input: _build_registry(MODE_SCIENTIFIC)
        Expected: Registry contains all 12 new operations
        """
        registry = _build_registry(MODE_SCIENTIFIC)
        ops = registry.list_all()
        new_ops = [
            "sin", "cos", "tan", "asin", "acos", "atan",
            "sinh", "cosh", "tanh", "exp", "pi", "e"
        ]
        for op in new_ops:
            assert op in ops, (
                f"Scientific mode missing '{op}' "
                "(one of the 12 new scientific operations)"
            )

    def test_scientific_mode_has_exactly_12_more_operations_than_normal(self):
        """Test that scientific mode has exactly 12 more operations than normal.

        Input: _build_registry(MODE_NORMAL) and _build_registry(MODE_SCIENTIFIC)
        Expected: len(scientific_ops) - len(normal_ops) == 12
        """
        normal_ops = set(_build_registry(MODE_NORMAL).list_all())
        scientific_ops = set(_build_registry(MODE_SCIENTIFIC).list_all())

        extra_ops = scientific_ops - normal_ops
        assert len(extra_ops) == 12, (
            f"Scientific mode should have 12 more ops than normal mode, "
            f"got {len(extra_ops)}: {sorted(extra_ops)}"
        )

    def test_scientific_mode_contains_all_normal_operations(self):
        """Test that scientific mode contains all normal mode operations.

        Input: _build_registry(MODE_NORMAL) and _build_registry(MODE_SCIENTIFIC)
        Expected: All normal operations are subset of scientific operations
        """
        normal_ops = set(_build_registry(MODE_NORMAL).list_all())
        scientific_ops = set(_build_registry(MODE_SCIENTIFIC).list_all())

        missing_in_scientific = normal_ops - scientific_ops
        assert not missing_in_scientific, (
            f"Scientific mode missing normal operations: {missing_in_scientific}"
        )
