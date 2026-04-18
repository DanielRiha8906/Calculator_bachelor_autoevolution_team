"""Comprehensive tests for scientific operations.

Tests cover ScientificOperations module, ModeManager, scientific_parser,
Calculator's scientific delegation, CalculatorWithHistory's scientific
recording, dispatcher's unary dispatch, and retry handler for scientific input.

All methods are tested for:
  - Happy path / normal execution with known values
  - Edge cases (zero, negative, special values, whitespace)
  - Error handling (ValueError for out-of-domain inputs)
  - Float precision using pytest.approx()
"""

import math
import pytest
from src.operations.scientific import ScientificOperations
from src.mode_manager import ModeManager
from src.scientific_parser import parse_unary_function, UNARY_FUNCTIONS
from src.calculator import Calculator
from src.calculator_with_history import CalculatorWithHistory
from src.dispatcher import run_unary_calculation
from src.retry_handler import get_scientific_unary_input_with_retries


# ============================================================================
# SCIENTIFIC OPERATIONS TESTS
# ============================================================================

class TestScientificOperations:
    """Test ScientificOperations module in isolation."""

    def test_scientific_operations_instantiation(self):
        """Verify ScientificOperations can be instantiated."""
        ops = ScientificOperations()
        assert ops is not None

    # ========================================================================
    # SIN METHOD TESTS
    # ========================================================================

    def test_sin_zero(self):
        """Happy path: sin(0) = 0."""
        ops = ScientificOperations()
        assert ops.sin(0) == pytest.approx(0.0)

    def test_sin_pi_over_2(self):
        """Happy path: sin(π/2) = 1."""
        ops = ScientificOperations()
        assert ops.sin(math.pi / 2) == pytest.approx(1.0)

    def test_sin_pi(self):
        """Happy path: sin(π) ≈ 0."""
        ops = ScientificOperations()
        assert ops.sin(math.pi) == pytest.approx(0.0, abs=1e-10)

    def test_sin_negative_angle(self):
        """Happy path: sin(-π/2) = -1."""
        ops = ScientificOperations()
        assert ops.sin(-math.pi / 2) == pytest.approx(-1.0)

    def test_sin_small_angle(self):
        """Happy path: sin with small angle."""
        ops = ScientificOperations()
        assert ops.sin(0.1) == pytest.approx(math.sin(0.1))

    def test_sin_large_angle(self):
        """Happy path: sin with large angle (periodicity)."""
        ops = ScientificOperations()
        assert ops.sin(10 * math.pi) == pytest.approx(0.0, abs=1e-10)

    def test_sin_infinity(self):
        """Edge case: sin(inf) raises ValueError (domain error)."""
        ops = ScientificOperations()
        with pytest.raises(ValueError):
            ops.sin(float("inf"))

    def test_sin_nan(self):
        """Edge case: sin(NaN) returns NaN."""
        ops = ScientificOperations()
        result = ops.sin(float("nan"))
        assert math.isnan(result)

    # ========================================================================
    # COS METHOD TESTS
    # ========================================================================

    def test_cos_zero(self):
        """Happy path: cos(0) = 1."""
        ops = ScientificOperations()
        assert ops.cos(0) == pytest.approx(1.0)

    def test_cos_pi_over_2(self):
        """Happy path: cos(π/2) ≈ 0."""
        ops = ScientificOperations()
        assert ops.cos(math.pi / 2) == pytest.approx(0.0, abs=1e-10)

    def test_cos_pi(self):
        """Happy path: cos(π) = -1."""
        ops = ScientificOperations()
        assert ops.cos(math.pi) == pytest.approx(-1.0)

    def test_cos_negative_angle(self):
        """Happy path: cos(-π) = -1."""
        ops = ScientificOperations()
        assert ops.cos(-math.pi) == pytest.approx(-1.0)

    def test_cos_small_angle(self):
        """Happy path: cos with small angle."""
        ops = ScientificOperations()
        assert ops.cos(0.1) == pytest.approx(math.cos(0.1))

    def test_cos_periodicity(self):
        """Happy path: cos with large angle (periodicity)."""
        ops = ScientificOperations()
        assert ops.cos(2 * math.pi) == pytest.approx(1.0)

    def test_cos_infinity(self):
        """Edge case: cos(inf) raises ValueError (domain error)."""
        ops = ScientificOperations()
        with pytest.raises(ValueError):
            ops.cos(float("inf"))

    def test_cos_nan(self):
        """Edge case: cos(NaN) returns NaN."""
        ops = ScientificOperations()
        result = ops.cos(float("nan"))
        assert math.isnan(result)

    # ========================================================================
    # TAN METHOD TESTS
    # ========================================================================

    def test_tan_zero(self):
        """Happy path: tan(0) = 0."""
        ops = ScientificOperations()
        assert ops.tan(0) == pytest.approx(0.0)

    def test_tan_pi_over_4(self):
        """Happy path: tan(π/4) = 1."""
        ops = ScientificOperations()
        assert ops.tan(math.pi / 4) == pytest.approx(1.0)

    def test_tan_pi(self):
        """Happy path: tan(π) ≈ 0."""
        ops = ScientificOperations()
        assert ops.tan(math.pi) == pytest.approx(0.0, abs=1e-10)

    def test_tan_negative_angle(self):
        """Happy path: tan(-π/4) = -1."""
        ops = ScientificOperations()
        assert ops.tan(-math.pi / 4) == pytest.approx(-1.0)

    def test_tan_small_angle(self):
        """Happy path: tan with small angle."""
        ops = ScientificOperations()
        assert ops.tan(0.1) == pytest.approx(math.tan(0.1))

    def test_tan_near_discontinuity(self):
        """Edge case: tan approaches discontinuity (but doesn't reach it)."""
        ops = ScientificOperations()
        # Close to π/2 but not equal
        result = ops.tan(math.pi / 2 - 0.01)
        assert isinstance(result, float)
        assert not math.isnan(result)

    def test_tan_infinity(self):
        """Edge case: tan(inf) raises ValueError (domain error)."""
        ops = ScientificOperations()
        with pytest.raises(ValueError):
            ops.tan(float("inf"))

    def test_tan_nan(self):
        """Edge case: tan(NaN) returns NaN."""
        ops = ScientificOperations()
        result = ops.tan(float("nan"))
        assert math.isnan(result)

    # ========================================================================
    # LOG METHOD TESTS (base-10)
    # ========================================================================

    def test_log_one(self):
        """Happy path: log(1) = 0."""
        ops = ScientificOperations()
        assert ops.log(1) == pytest.approx(0.0)

    def test_log_ten(self):
        """Happy path: log(10) = 1."""
        ops = ScientificOperations()
        assert ops.log(10) == pytest.approx(1.0)

    def test_log_hundred(self):
        """Happy path: log(100) = 2."""
        ops = ScientificOperations()
        assert ops.log(100) == pytest.approx(2.0)

    def test_log_fraction(self):
        """Happy path: log(0.1) = -1."""
        ops = ScientificOperations()
        assert ops.log(0.1) == pytest.approx(-1.0)

    def test_log_small_positive(self):
        """Happy path: log with small positive number."""
        ops = ScientificOperations()
        assert ops.log(0.01) == pytest.approx(-2.0)

    def test_log_large_number(self):
        """Happy path: log with large number."""
        ops = ScientificOperations()
        result = ops.log(1e6)
        assert result == pytest.approx(6.0)

    def test_log_zero_raises_error(self):
        """Error: log(0) raises ValueError."""
        ops = ScientificOperations()
        with pytest.raises(ValueError, match="log requires a positive number"):
            ops.log(0)

    def test_log_negative_raises_error(self):
        """Error: log(negative) raises ValueError."""
        ops = ScientificOperations()
        with pytest.raises(ValueError, match="log requires a positive number"):
            ops.log(-5)
        with pytest.raises(ValueError, match="log requires a positive number"):
            ops.log(-0.1)

    def test_log_very_small_positive(self):
        """Happy path: log with very small positive number."""
        ops = ScientificOperations()
        result = ops.log(1e-10)
        assert result == pytest.approx(-10.0)

    def test_log_infinity(self):
        """Edge case: log(inf) = inf."""
        ops = ScientificOperations()
        result = ops.log(float("inf"))
        assert result == float("inf")

    # ========================================================================
    # LN METHOD TESTS (natural logarithm)
    # ========================================================================

    def test_ln_one(self):
        """Happy path: ln(1) = 0."""
        ops = ScientificOperations()
        assert ops.ln(1) == pytest.approx(0.0)

    def test_ln_e(self):
        """Happy path: ln(e) = 1."""
        ops = ScientificOperations()
        assert ops.ln(math.e) == pytest.approx(1.0)

    def test_ln_e_squared(self):
        """Happy path: ln(e²) = 2."""
        ops = ScientificOperations()
        assert ops.ln(math.e ** 2) == pytest.approx(2.0)

    def test_ln_fraction(self):
        """Happy path: ln(1/e) = -1."""
        ops = ScientificOperations()
        assert ops.ln(1 / math.e) == pytest.approx(-1.0)

    def test_ln_small_positive(self):
        """Happy path: ln with small positive number."""
        ops = ScientificOperations()
        assert ops.ln(0.01) == pytest.approx(math.log(0.01))

    def test_ln_large_number(self):
        """Happy path: ln with large number."""
        ops = ScientificOperations()
        result = ops.ln(1e6)
        assert result == pytest.approx(math.log(1e6))

    def test_ln_zero_raises_error(self):
        """Error: ln(0) raises ValueError."""
        ops = ScientificOperations()
        with pytest.raises(ValueError, match="ln requires a positive number"):
            ops.ln(0)

    def test_ln_negative_raises_error(self):
        """Error: ln(negative) raises ValueError."""
        ops = ScientificOperations()
        with pytest.raises(ValueError, match="ln requires a positive number"):
            ops.ln(-5)
        with pytest.raises(ValueError, match="ln requires a positive number"):
            ops.ln(-0.1)

    def test_ln_infinity(self):
        """Edge case: ln(inf) = inf."""
        ops = ScientificOperations()
        result = ops.ln(float("inf"))
        assert result == float("inf")

    # ========================================================================
    # EXP METHOD TESTS
    # ========================================================================

    def test_exp_zero(self):
        """Happy path: exp(0) = 1."""
        ops = ScientificOperations()
        assert ops.exp(0) == pytest.approx(1.0)

    def test_exp_one(self):
        """Happy path: exp(1) = e."""
        ops = ScientificOperations()
        assert ops.exp(1) == pytest.approx(math.e)

    def test_exp_two(self):
        """Happy path: exp(2) = e²."""
        ops = ScientificOperations()
        assert ops.exp(2) == pytest.approx(math.e ** 2)

    def test_exp_negative_one(self):
        """Happy path: exp(-1) = 1/e."""
        ops = ScientificOperations()
        assert ops.exp(-1) == pytest.approx(1 / math.e)

    def test_exp_small_positive(self):
        """Happy path: exp with small positive number."""
        ops = ScientificOperations()
        assert ops.exp(0.1) == pytest.approx(math.exp(0.1))

    def test_exp_small_negative(self):
        """Happy path: exp with small negative number."""
        ops = ScientificOperations()
        assert ops.exp(-0.1) == pytest.approx(math.exp(-0.1))

    def test_exp_negative_large(self):
        """Happy path: exp with large negative (approaches zero)."""
        ops = ScientificOperations()
        result = ops.exp(-100)
        assert result == pytest.approx(0.0, abs=1e-40)

    def test_exp_infinity(self):
        """Edge case: exp(inf) = inf."""
        ops = ScientificOperations()
        result = ops.exp(float("inf"))
        assert result == float("inf")

    def test_exp_negative_infinity(self):
        """Edge case: exp(-inf) = 0."""
        ops = ScientificOperations()
        result = ops.exp(float("-inf"))
        assert result == pytest.approx(0.0)

    def test_exp_nan(self):
        """Edge case: exp(NaN) returns NaN."""
        ops = ScientificOperations()
        result = ops.exp(float("nan"))
        assert math.isnan(result)

    # ========================================================================
    # SQRT METHOD TESTS
    # ========================================================================

    def test_sqrt_zero(self):
        """Happy path: sqrt(0) = 0."""
        ops = ScientificOperations()
        assert ops.sqrt(0) == pytest.approx(0.0)

    def test_sqrt_one(self):
        """Happy path: sqrt(1) = 1."""
        ops = ScientificOperations()
        assert ops.sqrt(1) == pytest.approx(1.0)

    def test_sqrt_four(self):
        """Happy path: sqrt(4) = 2."""
        ops = ScientificOperations()
        assert ops.sqrt(4) == pytest.approx(2.0)

    def test_sqrt_nine(self):
        """Happy path: sqrt(9) = 3."""
        ops = ScientificOperations()
        assert ops.sqrt(9) == pytest.approx(3.0)

    def test_sqrt_two(self):
        """Happy path: sqrt(2) ≈ 1.414."""
        ops = ScientificOperations()
        assert ops.sqrt(2) == pytest.approx(math.sqrt(2))

    def test_sqrt_fraction(self):
        """Happy path: sqrt(0.25) = 0.5."""
        ops = ScientificOperations()
        assert ops.sqrt(0.25) == pytest.approx(0.5)

    def test_sqrt_small_positive(self):
        """Happy path: sqrt with small positive number."""
        ops = ScientificOperations()
        assert ops.sqrt(0.01) == pytest.approx(0.1)

    def test_sqrt_large_number(self):
        """Happy path: sqrt with large number."""
        ops = ScientificOperations()
        result = ops.sqrt(1e6)
        assert result == pytest.approx(1e3)

    def test_sqrt_negative_raises_error(self):
        """Error: sqrt(negative) raises ValueError."""
        ops = ScientificOperations()
        with pytest.raises(ValueError, match="sqrt requires a non-negative number"):
            ops.sqrt(-1)
        with pytest.raises(ValueError, match="sqrt requires a non-negative number"):
            ops.sqrt(-0.5)
        with pytest.raises(ValueError, match="sqrt requires a non-negative number"):
            ops.sqrt(-1e6)

    def test_sqrt_infinity(self):
        """Edge case: sqrt(inf) = inf."""
        ops = ScientificOperations()
        result = ops.sqrt(float("inf"))
        assert result == float("inf")

    # ========================================================================
    # PARAMETRIZED TESTS FOR ALL SCIENTIFIC OPERATIONS
    # ========================================================================

    @pytest.mark.parametrize("angle,expected", [
        (0, 0),
        (math.pi / 2, 1),
        (math.pi, 0),
        (-math.pi / 2, -1),
    ])
    def test_sin_parametrized(self, angle, expected):
        """Parametrized test for sin with known values."""
        ops = ScientificOperations()
        assert ops.sin(angle) == pytest.approx(expected, abs=1e-10)

    @pytest.mark.parametrize("angle,expected", [
        (0, 1),
        (math.pi / 2, 0),
        (math.pi, -1),
        (2 * math.pi, 1),
    ])
    def test_cos_parametrized(self, angle, expected):
        """Parametrized test for cos with known values."""
        ops = ScientificOperations()
        assert ops.cos(angle) == pytest.approx(expected, abs=1e-10)

    @pytest.mark.parametrize("angle,expected", [
        (0, 0),
        (math.pi / 4, 1),
        (math.pi, 0),
    ])
    def test_tan_parametrized(self, angle, expected):
        """Parametrized test for tan with known values."""
        ops = ScientificOperations()
        assert ops.tan(angle) == pytest.approx(expected, abs=1e-10)

    @pytest.mark.parametrize("x,expected", [
        (1, 0),
        (10, 1),
        (100, 2),
        (0.1, -1),
        (0.01, -2),
    ])
    def test_log_parametrized(self, x, expected):
        """Parametrized test for log (base-10)."""
        ops = ScientificOperations()
        assert ops.log(x) == pytest.approx(expected)

    @pytest.mark.parametrize("x,expected", [
        (1, 0),
        (math.e, 1),
        (math.e ** 2, 2),
        (1 / math.e, -1),
    ])
    def test_ln_parametrized(self, x, expected):
        """Parametrized test for ln (natural log)."""
        ops = ScientificOperations()
        assert ops.ln(x) == pytest.approx(expected)

    @pytest.mark.parametrize("x,expected", [
        (0, 1),
        (1, math.e),
        (2, math.e ** 2),
        (-1, 1 / math.e),
    ])
    def test_exp_parametrized(self, x, expected):
        """Parametrized test for exp."""
        ops = ScientificOperations()
        assert ops.exp(x) == pytest.approx(expected)

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (1, 1),
        (4, 2),
        (9, 3),
        (0.25, 0.5),
    ])
    def test_sqrt_parametrized(self, x, expected):
        """Parametrized test for sqrt."""
        ops = ScientificOperations()
        assert ops.sqrt(x) == pytest.approx(expected)


# ============================================================================
# MODE MANAGER TESTS
# ============================================================================

class TestModeManager:
    """Test ModeManager for mode switching and validation."""

    def test_mode_manager_instantiation(self):
        """Verify ModeManager initializes with default mode."""
        manager = ModeManager()
        assert manager is not None

    def test_default_mode_is_normal(self):
        """Test that default mode is 'normal'."""
        manager = ModeManager()
        assert manager.get_mode() == "normal"

    def test_is_scientific_default_false(self):
        """Test that is_scientific() returns False in default mode."""
        manager = ModeManager()
        assert manager.is_scientific() is False

    def test_set_mode_to_scientific(self):
        """Test switching to scientific mode."""
        manager = ModeManager()
        manager.set_mode("scientific")
        assert manager.get_mode() == "scientific"

    def test_is_scientific_after_switch(self):
        """Test is_scientific() returns True after switching."""
        manager = ModeManager()
        manager.set_mode("scientific")
        assert manager.is_scientific() is True

    def test_set_mode_back_to_normal(self):
        """Test switching from scientific back to normal."""
        manager = ModeManager()
        manager.set_mode("scientific")
        manager.set_mode("normal")
        assert manager.get_mode() == "normal"
        assert manager.is_scientific() is False

    def test_set_mode_invalid_raises_error(self):
        """Test that invalid mode raises ValueError."""
        manager = ModeManager()
        with pytest.raises(ValueError, match="Unknown mode"):
            manager.set_mode("invalid")

    def test_set_mode_case_sensitive(self):
        """Test that mode names are case-sensitive."""
        manager = ModeManager()
        with pytest.raises(ValueError):
            manager.set_mode("NORMAL")
        with pytest.raises(ValueError):
            manager.set_mode("SCIENTIFIC")
        with pytest.raises(ValueError):
            manager.set_mode("Scientific")

    def test_set_mode_empty_string_raises_error(self):
        """Test that empty string raises ValueError."""
        manager = ModeManager()
        with pytest.raises(ValueError, match="Unknown mode"):
            manager.set_mode("")

    def test_set_mode_whitespace_raises_error(self):
        """Test that whitespace-only mode raises ValueError."""
        manager = ModeManager()
        with pytest.raises(ValueError, match="Unknown mode"):
            manager.set_mode("  ")

    def test_mode_persistence_multiple_calls(self):
        """Test that mode persists correctly across multiple calls."""
        manager = ModeManager()
        manager.set_mode("scientific")
        assert manager.get_mode() == "scientific"
        assert manager.get_mode() == "scientific"
        assert manager.is_scientific() is True

    def test_mode_repeated_set_same(self):
        """Test setting mode repeatedly to the same value."""
        manager = ModeManager()
        manager.set_mode("scientific")
        manager.set_mode("scientific")
        assert manager.get_mode() == "scientific"

    @pytest.mark.parametrize("mode", ["normal", "scientific"])
    def test_set_mode_valid_modes(self, mode):
        """Parametrized test for all valid modes."""
        manager = ModeManager()
        manager.set_mode(mode)
        assert manager.get_mode() == mode


# ============================================================================
# SCIENTIFIC PARSER TESTS
# ============================================================================

class TestScientificParser:
    """Test parse_unary_function parser."""

    def test_parse_sin_zero(self):
        """Happy path: parse 'sin(0)'."""
        method_name, operand = parse_unary_function("sin(0)")
        assert method_name == "sin"
        assert operand == pytest.approx(0.0)

    def test_parse_cos_pi_over_two(self):
        """Happy path: parse 'cos(1.57)'."""
        method_name, operand = parse_unary_function("cos(1.57)")
        assert method_name == "cos"
        assert operand == pytest.approx(1.57)

    def test_parse_tan_small_value(self):
        """Happy path: parse 'tan(0.5)'."""
        method_name, operand = parse_unary_function("tan(0.5)")
        assert method_name == "tan"
        assert operand == pytest.approx(0.5)

    def test_parse_log_hundred(self):
        """Happy path: parse 'log(100)'."""
        method_name, operand = parse_unary_function("log(100)")
        assert method_name == "log"
        assert operand == pytest.approx(100.0)

    def test_parse_ln_one(self):
        """Happy path: parse 'ln(1)'."""
        method_name, operand = parse_unary_function("ln(1)")
        assert method_name == "ln"
        assert operand == pytest.approx(1.0)

    def test_parse_exp_zero(self):
        """Happy path: parse 'exp(0)'."""
        method_name, operand = parse_unary_function("exp(0)")
        assert method_name == "exp"
        assert operand == pytest.approx(0.0)

    def test_parse_sqrt_four(self):
        """Happy path: parse 'sqrt(4)'."""
        method_name, operand = parse_unary_function("sqrt(4)")
        assert method_name == "sqrt"
        assert operand == pytest.approx(4.0)

    def test_parse_negative_operand(self):
        """Happy path: parse function with negative operand."""
        method_name, operand = parse_unary_function("sin(-1.57)")
        assert method_name == "sin"
        assert operand == pytest.approx(-1.57)

    def test_parse_large_operand(self):
        """Happy path: parse function with large operand."""
        method_name, operand = parse_unary_function("log(1000000)")
        assert method_name == "log"
        assert operand == pytest.approx(1000000.0)

    def test_parse_small_positive_operand(self):
        """Happy path: parse function with small positive operand."""
        method_name, operand = parse_unary_function("sqrt(0.01)")
        assert method_name == "sqrt"
        assert operand == pytest.approx(0.01)

    def test_parse_with_leading_whitespace(self):
        """Happy path: parse with leading whitespace."""
        method_name, operand = parse_unary_function("  sin(0)")
        assert method_name == "sin"
        assert operand == pytest.approx(0.0)

    def test_parse_with_trailing_whitespace(self):
        """Happy path: parse with trailing whitespace."""
        method_name, operand = parse_unary_function("sin(0)  ")
        assert method_name == "sin"
        assert operand == pytest.approx(0.0)

    def test_parse_with_whitespace_around_operand(self):
        """Happy path: parse with whitespace around operand."""
        method_name, operand = parse_unary_function("sin( 0 )")
        assert method_name == "sin"
        assert operand == pytest.approx(0.0)

    def test_parse_with_whitespace_after_function(self):
        """Happy path: parse with whitespace after function name."""
        method_name, operand = parse_unary_function("sin (0)")
        assert method_name == "sin"
        assert operand == pytest.approx(0.0)

    def test_parse_missing_opening_paren_raises_error(self):
        """Error: missing opening parenthesis."""
        with pytest.raises(ValueError, match="Invalid expression"):
            parse_unary_function("sin0)")

    def test_parse_missing_closing_paren_raises_error(self):
        """Error: missing closing parenthesis."""
        with pytest.raises(ValueError, match="Invalid expression"):
            parse_unary_function("sin(0")

    def test_parse_no_parentheses_raises_error(self):
        """Error: no parentheses."""
        with pytest.raises(ValueError, match="Invalid expression"):
            parse_unary_function("sin0")

    def test_parse_empty_parens_raises_error(self):
        """Error: empty parentheses (no operand)."""
        with pytest.raises(ValueError, match="Invalid expression"):
            parse_unary_function("sin()")

    def test_parse_whitespace_only_parens_raises_error(self):
        """Error: whitespace-only inside parentheses."""
        with pytest.raises(ValueError, match="Invalid argument"):
            parse_unary_function("sin(  )")

    def test_parse_invalid_function_name_raises_error(self):
        """Error: unknown function name."""
        with pytest.raises(ValueError, match="Unknown function"):
            parse_unary_function("asin(0)")

    def test_parse_uppercase_function_raises_error(self):
        """Error: function name case sensitivity."""
        with pytest.raises(ValueError, match="Unknown function"):
            parse_unary_function("SIN(0)")

    def test_parse_non_numeric_operand_raises_error(self):
        """Error: non-numeric operand."""
        with pytest.raises(ValueError, match="Invalid argument"):
            parse_unary_function("sin(abc)")

    def test_parse_operand_with_letters_raises_error(self):
        """Error: operand with embedded letters."""
        with pytest.raises(ValueError, match="Invalid argument"):
            parse_unary_function("sin(1.5x)")

    def test_parse_multiple_commas_raises_error(self):
        """Error: multiple operands (comma-separated)."""
        with pytest.raises(ValueError, match="Invalid argument"):
            parse_unary_function("sin(1, 2)")

    def test_parse_empty_string_raises_error(self):
        """Error: empty input string."""
        with pytest.raises(ValueError, match="Invalid expression"):
            parse_unary_function("")

    def test_parse_whitespace_only_raises_error(self):
        """Error: whitespace-only input."""
        with pytest.raises(ValueError, match="Invalid expression"):
            parse_unary_function("   ")

    def test_parse_extra_characters_after_close_paren_raises_error(self):
        """Error: extra characters after closing paren."""
        with pytest.raises(ValueError, match="Invalid expression"):
            parse_unary_function("sin(0)extra")

    def test_parse_extra_characters_before_function_raises_error(self):
        """Error: extra characters before function name (parsed as unknown function)."""
        with pytest.raises(ValueError, match="Unknown function"):
            parse_unary_function("xsin(0)")

    def test_parse_scientific_notation(self):
        """Happy path: parse operand in scientific notation."""
        method_name, operand = parse_unary_function("log(1e6)")
        assert method_name == "log"
        assert operand == pytest.approx(1e6)

    def test_parse_negative_scientific_notation(self):
        """Happy path: parse operand in negative scientific notation."""
        method_name, operand = parse_unary_function("exp(-1e2)")
        assert method_name == "exp"
        assert operand == pytest.approx(-1e2)

    def test_parse_float_with_leading_dot(self):
        """Happy path: parse float starting with decimal point."""
        method_name, operand = parse_unary_function("sqrt(.25)")
        assert method_name == "sqrt"
        assert operand == pytest.approx(0.25)

    def test_parse_float_with_trailing_dot(self):
        """Happy path: parse float ending with decimal point."""
        method_name, operand = parse_unary_function("log(100.)")
        assert method_name == "log"
        assert operand == pytest.approx(100.0)

    def test_parse_double_dot_raises_error(self):
        """Error: operand with double decimal point."""
        with pytest.raises(ValueError, match="Invalid argument"):
            parse_unary_function("sin(1..5)")

    @pytest.mark.parametrize("func_name", list(UNARY_FUNCTIONS.keys()))
    def test_parse_all_supported_functions(self, func_name):
        """Parametrized test for all supported function names."""
        method_name, operand = parse_unary_function(f"{func_name}(1.0)")
        assert method_name == UNARY_FUNCTIONS[func_name]
        assert operand == pytest.approx(1.0)


# ============================================================================
# CALCULATOR SCIENTIFIC DELEGATION TESTS
# ============================================================================

class TestCalculatorScientific:
    """Test Calculator delegation to ScientificOperations."""

    def test_calculator_sin(self):
        """Test Calculator.sin delegates correctly."""
        calc = Calculator()
        result = calc.sin(0)
        assert result == pytest.approx(0.0)

    def test_calculator_cos(self):
        """Test Calculator.cos delegates correctly."""
        calc = Calculator()
        result = calc.cos(0)
        assert result == pytest.approx(1.0)

    def test_calculator_tan(self):
        """Test Calculator.tan delegates correctly."""
        calc = Calculator()
        result = calc.tan(0)
        assert result == pytest.approx(0.0)

    def test_calculator_exp(self):
        """Test Calculator.exp delegates correctly."""
        calc = Calculator()
        result = calc.exp(0)
        assert result == pytest.approx(1.0)

    def test_calculator_sqrt(self):
        """Test Calculator.sqrt delegates correctly."""
        calc = Calculator()
        result = calc.sqrt(4)
        assert result == pytest.approx(2.0)

    def test_calculator_sqrt_negative_raises_error(self):
        """Test Calculator.sqrt raises error for negative input."""
        calc = Calculator()
        with pytest.raises(ValueError):
            calc.sqrt(-1)

    def test_calculator_sin_with_pi_over_2(self):
        """Test Calculator.sin with π/2."""
        calc = Calculator()
        result = calc.sin(math.pi / 2)
        assert result == pytest.approx(1.0)

    def test_calculator_cos_with_pi(self):
        """Test Calculator.cos with π."""
        calc = Calculator()
        result = calc.cos(math.pi)
        assert result == pytest.approx(-1.0)

    def test_calculator_exp_with_one(self):
        """Test Calculator.exp with 1."""
        calc = Calculator()
        result = calc.exp(1)
        assert result == pytest.approx(math.e)

    def test_calculator_sqrt_with_fraction(self):
        """Test Calculator.sqrt with fractional input."""
        calc = Calculator()
        result = calc.sqrt(0.25)
        assert result == pytest.approx(0.5)


# ============================================================================
# CALCULATOR WITH HISTORY SCIENTIFIC TESTS
# ============================================================================

class TestCalculatorWithHistoryScientific:
    """Test CalculatorWithHistory recording of scientific operations."""

    def test_history_sin_recorded(self):
        """Test sin operation is recorded in history."""
        calc = CalculatorWithHistory()
        result = calc.sin(0)
        history = calc.get_history()
        assert len(history) == 1
        assert "sin(0)" in history[0]
        assert str(result) in history[0] or f"{result}" in history[0]

    def test_history_cos_recorded(self):
        """Test cos operation is recorded in history."""
        calc = CalculatorWithHistory()
        result = calc.cos(0)
        history = calc.get_history()
        assert len(history) == 1
        assert "cos(0)" in history[0]

    def test_history_tan_recorded(self):
        """Test tan operation is recorded in history."""
        calc = CalculatorWithHistory()
        result = calc.tan(0)
        history = calc.get_history()
        assert len(history) == 1
        assert "tan(0)" in history[0]

    def test_history_exp_recorded(self):
        """Test exp operation is recorded in history."""
        calc = CalculatorWithHistory()
        result = calc.exp(0)
        history = calc.get_history()
        assert len(history) == 1
        assert "exp(0)" in history[0]

    def test_history_sqrt_recorded(self):
        """Test sqrt operation is recorded in history."""
        calc = CalculatorWithHistory()
        result = calc.sqrt(4)
        history = calc.get_history()
        assert len(history) == 1
        assert "sqrt(4)" in history[0]

    def test_history_multiple_scientific_operations(self):
        """Test multiple scientific operations are recorded in order."""
        calc = CalculatorWithHistory()
        calc.sin(0)
        calc.cos(0)
        calc.sqrt(4)
        history = calc.get_history()
        assert len(history) == 3
        assert "sin(0)" in history[0]
        assert "cos(0)" in history[1]
        assert "sqrt(4)" in history[2]

    def test_history_failed_operation_not_recorded(self):
        """Test that failed operations are not recorded."""
        calc = CalculatorWithHistory()
        calc.sin(0)
        try:
            calc.sqrt(-1)
        except ValueError:
            pass
        history = calc.get_history()
        assert len(history) == 1
        assert "sin(0)" in history[0]

    def test_history_sqrt_negative_raises_error(self):
        """Test sqrt with negative raises error."""
        calc = CalculatorWithHistory()
        with pytest.raises(ValueError):
            calc.sqrt(-5)

    def test_history_format_sin(self):
        """Test sin history format is correct."""
        calc = CalculatorWithHistory()
        calc.sin(math.pi)
        history = calc.get_history()
        # Format should be "sin(x) = result"
        assert "=" in history[0]
        assert "sin" in history[0]

    def test_history_format_sqrt(self):
        """Test sqrt history format is correct."""
        calc = CalculatorWithHistory()
        calc.sqrt(9)
        history = calc.get_history()
        # Format should be "sqrt(x) = result"
        assert "=" in history[0]
        assert "sqrt" in history[0]


# ============================================================================
# DISPATCHER TESTS
# ============================================================================

class TestDispatcherUnary:
    """Test run_unary_calculation dispatcher."""

    def test_dispatch_sin(self):
        """Test dispatching sin method."""
        result, calc = run_unary_calculation(0, "sin")
        assert result == pytest.approx(0.0)
        assert isinstance(calc, CalculatorWithHistory)

    def test_dispatch_cos(self):
        """Test dispatching cos method."""
        result, calc = run_unary_calculation(0, "cos")
        assert result == pytest.approx(1.0)

    def test_dispatch_tan(self):
        """Test dispatching tan method."""
        result, calc = run_unary_calculation(0, "tan")
        assert result == pytest.approx(0.0)

    def test_dispatch_exp(self):
        """Test dispatching exp method."""
        result, calc = run_unary_calculation(0, "exp")
        assert result == pytest.approx(1.0)

    def test_dispatch_sqrt(self):
        """Test dispatching sqrt method."""
        result, calc = run_unary_calculation(4, "sqrt")
        assert result == pytest.approx(2.0)

    def test_dispatch_sin_pi_over_2(self):
        """Test dispatching sin with π/2."""
        result, calc = run_unary_calculation(math.pi / 2, "sin")
        assert result == pytest.approx(1.0)

    def test_dispatch_sqrt_error_propagation(self):
        """Test that errors are propagated from dispatcher."""
        with pytest.raises(ValueError):
            run_unary_calculation(-1, "sqrt")

    def test_dispatch_result_in_history(self):
        """Test that dispatched operation appears in history."""
        result, calc = run_unary_calculation(4, "sqrt")
        history = calc.get_history()
        assert len(history) == 1
        assert "sqrt(4)" in history[0]

    def test_dispatch_invalid_method_name_raises_error(self):
        """Test dispatching non-existent method raises AttributeError."""
        with pytest.raises(AttributeError):
            run_unary_calculation(1, "nonexistent_method")

    def test_dispatch_returns_tuple(self):
        """Test dispatcher returns (result, calculator) tuple."""
        result, calc = run_unary_calculation(4, "sqrt")
        assert isinstance(result, float)
        assert isinstance(calc, CalculatorWithHistory)


# ============================================================================
# RETRY HANDLER TESTS FOR SCIENTIFIC INPUT
# ============================================================================

class TestGetScientificUnaryInputWithRetries:
    """Test get_scientific_unary_input_with_retries with mocked input."""

    def test_valid_input_first_try(self, monkeypatch):
        """Test successful parsing on first try."""
        inputs = iter(["sin(0)"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        result = get_scientific_unary_input_with_retries(max_retries=3)
        assert result is not None
        assert result[0] == "sin"
        assert result[1] == pytest.approx(0.0)

    def test_valid_log_input(self, monkeypatch):
        """Test parsing log(100)."""
        inputs = iter(["log(100)"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        result = get_scientific_unary_input_with_retries(max_retries=3)
        assert result is not None
        assert result[0] == "log"
        assert result[1] == pytest.approx(100.0)

    def test_valid_sqrt_input(self, monkeypatch):
        """Test parsing sqrt(4)."""
        inputs = iter(["sqrt(4)"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        result = get_scientific_unary_input_with_retries(max_retries=3)
        assert result is not None
        assert result[0] == "sqrt"
        assert result[1] == pytest.approx(4.0)

    def test_empty_input_first_try_then_valid(self, monkeypatch):
        """Test recovery from empty input on first try."""
        inputs = iter(["", "sin(0)"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        result = get_scientific_unary_input_with_retries(max_retries=3)
        assert result is not None
        assert result[0] == "sin"

    def test_invalid_syntax_first_try_then_valid(self, monkeypatch):
        """Test recovery from invalid syntax on first try."""
        inputs = iter(["invalid", "sin(0)"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        result = get_scientific_unary_input_with_retries(max_retries=3)
        assert result is not None
        assert result[0] == "sin"

    def test_max_retries_exhausted_returns_none(self, monkeypatch):
        """Test returns None when max retries exhausted."""
        inputs = iter(["invalid", "invalid", "invalid", "invalid"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        result = get_scientific_unary_input_with_retries(max_retries=3)
        assert result is None

    def test_empty_input_all_retries_returns_none(self, monkeypatch):
        """Test returns None when all retries are empty input."""
        inputs = iter(["", "", "", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        result = get_scientific_unary_input_with_retries(max_retries=3)
        assert result is None

    def test_whitespace_input_treated_as_empty(self, monkeypatch):
        """Test whitespace-only input is treated as empty."""
        inputs = iter(["   ", "sin(0)"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        result = get_scientific_unary_input_with_retries(max_retries=3)
        assert result is not None
        assert result[0] == "sin"

    def test_single_retry_limit(self, monkeypatch):
        """Test with max_retries=1."""
        inputs = iter(["invalid", "sin(0)"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        result = get_scientific_unary_input_with_retries(max_retries=1)
        assert result is None  # No retries allowed after first failure

    def test_non_numeric_argument_retry(self, monkeypatch):
        """Test retry after non-numeric argument."""
        inputs = iter(["sin(abc)", "sin(0)"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        result = get_scientific_unary_input_with_retries(max_retries=3)
        assert result is not None
        assert result[0] == "sin"

    def test_missing_paren_retry(self, monkeypatch):
        """Test retry after missing parenthesis."""
        inputs = iter(["sin(0", "sin(0)"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        result = get_scientific_unary_input_with_retries(max_retries=3)
        assert result is not None
        assert result[0] == "sin"

    def test_unknown_function_retry(self, monkeypatch):
        """Test retry after unknown function name."""
        inputs = iter(["asin(0)", "sin(0)"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        result = get_scientific_unary_input_with_retries(max_retries=3)
        assert result is not None
        assert result[0] == "sin"

    def test_negative_operand_handling(self, monkeypatch):
        """Test handling negative operand."""
        inputs = iter(["sin(-1.57)"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        result = get_scientific_unary_input_with_retries(max_retries=3)
        assert result is not None
        assert result[0] == "sin"
        assert result[1] == pytest.approx(-1.57)

    def test_scientific_notation_operand(self, monkeypatch):
        """Test handling scientific notation."""
        inputs = iter(["log(1e6)"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        result = get_scientific_unary_input_with_retries(max_retries=3)
        assert result is not None
        assert result[0] == "log"
        assert result[1] == pytest.approx(1e6)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestScientificIntegration:
    """Integration tests combining parser, dispatcher, and calculator."""

    def test_parse_and_dispatch_sin(self):
        """Test parsing 'sin(0)' and dispatching to calculator."""
        method_name, operand = parse_unary_function("sin(0)")
        result, calc = run_unary_calculation(operand, method_name)
        assert result == pytest.approx(0.0)
        history = calc.get_history()
        assert len(history) == 1
        # History records the actual float values, so 0 becomes 0.0
        assert "sin" in history[0] and "=" in history[0]

    def test_parse_and_dispatch_sqrt(self):
        """Test parsing 'sqrt(4)' and dispatching to calculator."""
        method_name, operand = parse_unary_function("sqrt(4)")
        result, calc = run_unary_calculation(operand, method_name)
        assert result == pytest.approx(2.0)
        history = calc.get_history()
        assert len(history) == 1
        # History records the actual float values, so 4 becomes 4.0
        assert "sqrt" in history[0] and "=" in history[0]

    def test_parse_and_dispatch_log(self):
        """Test parsing 'log(100)' and dispatching to calculator."""
        method_name, operand = parse_unary_function("log(100)")
        result, calc = run_unary_calculation(operand, method_name)
        assert result == pytest.approx(2.0)

    def test_parse_invalid_then_dispatch_raises_error(self):
        """Test that parsing error prevents dispatcher call."""
        with pytest.raises(ValueError):
            parse_unary_function("invalid")

    def test_parse_valid_then_dispatch_domain_error(self):
        """Test parsing succeeds but dispatcher raises domain error."""
        method_name, operand = parse_unary_function("sqrt(-1)")
        with pytest.raises(ValueError):
            run_unary_calculation(operand, method_name)

    def test_mode_manager_affects_calculator_behavior(self):
        """Test that ModeManager state doesn't affect Calculator (for documentation)."""
        manager = ModeManager()
        calc = Calculator()

        # Both modes should allow scientific operations
        manager.set_mode("scientific")
        result1 = calc.sin(0)

        manager.set_mode("normal")
        result2 = calc.sin(0)

        assert result1 == pytest.approx(result2)

    def test_all_scientific_operations_with_history(self):
        """Test all scientific operations recorded in history."""
        calc = CalculatorWithHistory()

        ops = [
            ("sin", 0, 0),
            ("cos", 0, 1),
            ("sqrt", 4, 2),
            ("exp", 0, 1),
        ]

        for method_name, operand, expected in ops:
            result = getattr(calc, method_name)(operand)
            assert result == pytest.approx(expected)

        history = calc.get_history()
        assert len(history) == 4
        for method_name, _, _ in ops:
            assert any(method_name in h for h in history)
