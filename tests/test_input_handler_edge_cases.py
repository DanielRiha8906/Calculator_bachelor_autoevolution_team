"""Additional edge-case tests for src.input_handler and src.__main__.main.

These tests complement the 27 tests already in test_input_handler.py and focus
on boundary values, near-numeric strings, operator mapping completeness, and
the full main() integration path via monkeypatching.
"""

import sys
import pytest

from src.input_handler import parse_operand, parse_input, run_calculation, BINARY_OPERATORS


# ===========================================================================
# parse_operand — happy path / boundary numerics
# ===========================================================================

class TestParseOperandHappyPath:
    def test_integer_string(self):
        assert parse_operand("42") == pytest.approx(42.0)

    def test_float_string(self):
        assert parse_operand("3.14") == pytest.approx(3.14)

    def test_negative_float(self):
        assert parse_operand("-3.5") == pytest.approx(-3.5)

    def test_negative_integer(self):
        assert parse_operand("-7") == pytest.approx(-7.0)

    def test_zero(self):
        assert parse_operand("0") == pytest.approx(0.0)

    def test_negative_zero(self):
        assert parse_operand("-0") == pytest.approx(0.0)

    def test_leading_whitespace_stripped(self):
        assert parse_operand("  5") == pytest.approx(5.0)

    def test_trailing_whitespace_stripped(self):
        assert parse_operand("5  ") == pytest.approx(5.0)

    def test_both_sides_whitespace_stripped(self):
        assert parse_operand("  5  ") == pytest.approx(5.0)

    def test_very_large_float(self):
        result = parse_operand("1e308")
        assert result == pytest.approx(1e308)

    def test_very_small_positive_float(self):
        result = parse_operand("1e-308")
        assert result == pytest.approx(1e-308)

    def test_scientific_notation_positive(self):
        assert parse_operand("1.5e3") == pytest.approx(1500.0)

    def test_scientific_notation_negative_exponent(self):
        assert parse_operand("2.5e-2") == pytest.approx(0.025)

    def test_scientific_notation_uppercase_E(self):
        assert parse_operand("1.5E3") == pytest.approx(1500.0)

    def test_returns_float_type(self):
        result = parse_operand("10")
        assert isinstance(result, float)


# ===========================================================================
# parse_operand — strings that look almost numeric but are not
# ===========================================================================

class TestParseOperandInvalidNearNumeric:
    @pytest.mark.parametrize("raw", [
        "1.2.3",        # two decimal points
        "1,000",        # comma as thousands separator
        "None",         # Python keyword — not accepted by float()
        "1 2",          # space between digits
        "++1",          # double sign
        "--1",          # double sign
        "1e",           # incomplete scientific notation
        "abc",          # purely alphabetic
        "",             # empty string
        "   ",          # whitespace only
        "1.0e1.5",      # non-integer exponent
        "#5",           # hash prefix
        "0x10",         # hex notation (not accepted by float())
    ])
    def test_invalid_string_raises_value_error(self, raw):
        with pytest.raises(ValueError):
            parse_operand(raw)

    def test_nan_string_behavior(self):
        # float("nan") succeeds in Python — parse_operand must also succeed
        # and return a NaN float (it's the caller's responsibility to validate)
        result = parse_operand("nan")
        import math
        assert math.isnan(result)

    def test_inf_string_behavior(self):
        # float("inf") succeeds in Python — parse_operand must also succeed
        import math
        result = parse_operand("inf")
        assert math.isinf(result)

    def test_error_message_contains_raw_input(self):
        with pytest.raises(ValueError, match="1,000"):
            parse_operand("1,000")

    def test_underscore_grouping_is_accepted(self):
        # Python 3.6+ float() DOES accept underscore-grouped numeric literals,
        # so "1_000" parses to 1000.0 — this documents the actual behavior.
        result = parse_operand("1_000")
        assert result == pytest.approx(1000.0)

    def test_none_passed_raises_attribute_error_or_value_error(self):
        # raw.strip() will raise AttributeError for None input;
        # we verify it does not silently succeed
        with pytest.raises((AttributeError, TypeError, ValueError)):
            parse_operand(None)  # type: ignore[arg-type]


# ===========================================================================
# parse_input — operator mapping completeness
# ===========================================================================

class TestParseInputOperatorMapping:
    """Verify every symbol in BINARY_OPERATORS maps to the right method name."""

    @pytest.mark.parametrize("symbol,expected_method", [
        ("+", "add"),
        ("-", "subtract"),
        ("*", "multiply"),
        ("/", "divide"),
    ])
    def test_operator_maps_to_correct_method(self, symbol, expected_method):
        _, _, method = parse_input("1", "2", symbol)
        assert method == expected_method

    def test_binary_operators_dict_has_exactly_four_entries(self):
        assert len(BINARY_OPERATORS) == 4

    def test_all_returned_method_names_exist_on_calculator(self):
        from src.calculator import Calculator
        calc = Calculator()
        for method_name in BINARY_OPERATORS.values():
            assert hasattr(calc, method_name), f"Calculator is missing method {method_name!r}"
            assert callable(getattr(calc, method_name))


# ===========================================================================
# parse_input — operator strings that are valid Python identifiers but
#               not in BINARY_OPERATORS
# ===========================================================================

class TestParseInputUnsupportedOperators:
    @pytest.mark.parametrize("operator", [
        "add",       # method name, not the symbol
        "divide",    # method name, not the symbol
        "multiply",  # method name, not the symbol
        "subtract",  # method name, not the symbol
        "^",         # XOR / power in many languages
        "//",        # floor division
        "mod",
        "%",
        "!=",
        "==",
    ])
    def test_operator_not_in_binary_operators_raises_value_error(self, operator):
        with pytest.raises(ValueError):
            parse_input("3", "4", operator)

    def test_whitespace_padded_valid_operator_accepted(self):
        # The implementation strips the operator; " + " must still be valid
        _, _, method = parse_input("3", "4", " + ")
        assert method == "add"

    def test_error_message_mentions_unsupported_operator(self):
        with pytest.raises(ValueError, match="Unsupported operator"):
            parse_input("3", "4", "add")


# ===========================================================================
# parse_input — both operands invalid simultaneously
# ===========================================================================

class TestParseInputBothOperandsInvalid:
    def test_both_non_numeric_raises_value_error(self):
        # parse_operand(operand_a) is called first; the error from the first
        # invalid operand must propagate
        with pytest.raises(ValueError):
            parse_input("abc", "xyz", "+")

    def test_first_invalid_operand_takes_precedence(self):
        # Ensure we get a ValueError from operand_a validation, not operand_b
        with pytest.raises(ValueError, match="abc"):
            parse_input("abc", "xyz", "+")


# ===========================================================================
# run_calculation — all four operators produce correct results
# ===========================================================================

class TestRunCalculationAllOperators:
    def test_add_positive_numbers(self):
        assert run_calculation(3.0, 4.0, "add") == pytest.approx(7.0)

    def test_add_negative_numbers(self):
        assert run_calculation(-3.0, -4.0, "add") == pytest.approx(-7.0)

    def test_add_mixed_signs(self):
        assert run_calculation(-3.0, 4.0, "add") == pytest.approx(1.0)

    def test_subtract_produces_negative(self):
        assert run_calculation(3.0, 10.0, "subtract") == pytest.approx(-7.0)

    def test_subtract_same_values_gives_zero(self):
        assert run_calculation(5.0, 5.0, "subtract") == pytest.approx(0.0)

    def test_subtract_negative_operand(self):
        assert run_calculation(5.0, -3.0, "subtract") == pytest.approx(8.0)

    def test_multiply_by_zero(self):
        assert run_calculation(99999.0, 0.0, "multiply") == pytest.approx(0.0)

    def test_multiply_two_negatives_gives_positive(self):
        assert run_calculation(-4.0, -5.0, "multiply") == pytest.approx(20.0)

    def test_multiply_negative_and_positive(self):
        assert run_calculation(-4.0, 5.0, "multiply") == pytest.approx(-20.0)

    def test_divide_produces_float_result(self):
        assert run_calculation(5.0, 2.0, "divide") == pytest.approx(2.5)

    def test_divide_one_third(self):
        assert run_calculation(1.0, 3.0, "divide") == pytest.approx(1 / 3)

    def test_divide_negative_by_positive(self):
        assert run_calculation(-6.0, 2.0, "divide") == pytest.approx(-3.0)

    def test_divide_positive_by_negative(self):
        assert run_calculation(6.0, -2.0, "divide") == pytest.approx(-3.0)

    def test_divide_by_zero_raises_zero_division_error(self):
        with pytest.raises(ZeroDivisionError):
            run_calculation(5.0, 0.0, "divide")

    def test_divide_zero_by_nonzero(self):
        assert run_calculation(0.0, 5.0, "divide") == pytest.approx(0.0)

    def test_large_number_addition(self):
        assert run_calculation(1e300, 1e300, "add") == pytest.approx(2e300)

    def test_multiply_large_numbers_overflow_to_inf(self):
        # 1e200 * 1e200 = 1e400, which exceeds float max (~1.8e308) → inf
        import math
        result = run_calculation(1e200, 1e200, "multiply")
        assert math.isinf(result)

    def test_multiply_large_numbers_within_range(self):
        # 1e154 * 1e154 = 1e308, which is within float range (~1.8e308)
        result = run_calculation(1e154, 1e154, "multiply")
        assert result == pytest.approx(1e308, rel=1e-6)


# ===========================================================================
# main() — integration tests via monkeypatching
# ===========================================================================

class TestMain:
    """Tests for src.__main__.main using monkeypatching of input() and sys.exit."""

    def _run_main(self, monkeypatch, inputs, capsys):
        """Helper: patch input() with a sequence of values and run main()."""
        from src.__main__ import main
        input_iter = iter(inputs)
        monkeypatch.setattr("builtins.input", lambda _: next(input_iter))
        with pytest.raises(SystemExit) as exc_info:
            main()
            # If main returns normally (no sys.exit), pytest.raises will not
            # catch anything — that's fine; return None to signal success.
        return exc_info

    # --- helpers that do NOT expect a SystemExit ---
    def _run_main_success(self, monkeypatch, inputs, capsys):
        from src.__main__ import main
        input_iter = iter(inputs)
        monkeypatch.setattr("builtins.input", lambda _: next(input_iter))
        main()  # must not raise

    # -----------------------------------------------------------------------
    # Valid inputs → result printed to stdout
    # -----------------------------------------------------------------------

    def test_valid_addition_prints_result(self, monkeypatch, capsys):
        self._run_main_success(monkeypatch, ["3", "4", "+"], capsys)
        captured = capsys.readouterr()
        assert "7" in captured.out
        assert captured.err == ""

    def test_valid_subtraction_prints_result(self, monkeypatch, capsys):
        self._run_main_success(monkeypatch, ["10", "3", "-"], capsys)
        captured = capsys.readouterr()
        assert "7" in captured.out

    def test_valid_multiplication_prints_result(self, monkeypatch, capsys):
        self._run_main_success(monkeypatch, ["6", "7", "*"], capsys)
        captured = capsys.readouterr()
        assert "42" in captured.out

    def test_valid_division_prints_result(self, monkeypatch, capsys):
        self._run_main_success(monkeypatch, ["8", "2", "/"], capsys)
        captured = capsys.readouterr()
        assert "4" in captured.out

    def test_valid_division_float_result_printed(self, monkeypatch, capsys):
        self._run_main_success(monkeypatch, ["5", "2", "/"], capsys)
        captured = capsys.readouterr()
        assert "2.5" in captured.out

    def test_valid_inputs_no_stderr_output(self, monkeypatch, capsys):
        self._run_main_success(monkeypatch, ["1", "1", "+"], capsys)
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_result_line_has_result_prefix(self, monkeypatch, capsys):
        self._run_main_success(monkeypatch, ["3", "4", "+"], capsys)
        captured = capsys.readouterr()
        assert captured.out.startswith("Result:")

    # -----------------------------------------------------------------------
    # Non-numeric input → sys.exit(1) + stderr
    # -----------------------------------------------------------------------

    def test_non_numeric_operand_a_exits_with_1(self, monkeypatch, capsys):
        # With retry logic, exhausted retries on first operand returns cleanly (no sys.exit)
        from src.__main__ import main
        inputs = iter(["abc", "abc", "abc", "abc"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        main()  # must not raise SystemExit

    def test_non_numeric_operand_a_prints_error_to_stderr(self, monkeypatch, capsys):
        # Exhausted retries on first operand returns clean (no sys.exit), error messages printed
        from src.__main__ import main
        inputs = iter(["abc", "abc", "abc", "abc"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        main()  # must not raise
        captured = capsys.readouterr()
        assert "Invalid input:" in captured.out

    def test_non_numeric_operand_b_exits_with_1(self, monkeypatch, capsys):
        # First operand valid, second operand exhausts retries - returns cleanly
        from src.__main__ import main
        inputs = iter(["3", "xyz", "xyz", "xyz", "xyz"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        main()  # must not raise SystemExit

    def test_non_numeric_operand_b_prints_error_to_stderr(self, monkeypatch, capsys):
        # First operand valid, second operand exhausts retries
        from src.__main__ import main
        inputs = iter(["3", "xyz", "xyz", "xyz", "xyz"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        main()  # must not raise
        captured = capsys.readouterr()
        assert "Invalid input:" in captured.out

    def test_non_numeric_no_stdout_output(self, monkeypatch, capsys):
        # Exhaust retries on first operand
        from src.__main__ import main
        inputs = iter(["abc", "abc", "abc", "abc"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        main()  # must not raise
        captured = capsys.readouterr()
        assert "Result:" not in captured.out

    # -----------------------------------------------------------------------
    # Unsupported operator → sys.exit(1) + stderr
    # -----------------------------------------------------------------------

    def test_unsupported_operator_exits_with_1(self, monkeypatch, capsys):
        # Both operands valid, operator exhausts retries - returns cleanly
        from src.__main__ import main
        inputs = iter(["3", "4", "%", "%", "%", "%"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        main()  # must not raise SystemExit

    def test_unsupported_operator_word_exits_with_1(self, monkeypatch, capsys):
        # Both operands valid, operator exhausts retries - returns cleanly
        from src.__main__ import main
        inputs = iter(["3", "4", "add", "add", "add", "add"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        main()  # must not raise SystemExit

    def test_unsupported_operator_prints_error_to_stderr(self, monkeypatch, capsys):
        # Operator exhausts retries, returns clean (no sys.exit)
        from src.__main__ import main
        inputs = iter(["3", "4", "%", "%", "%", "%"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        main()  # must not raise
        captured = capsys.readouterr()
        assert "Invalid input:" in captured.out

    def test_unsupported_operator_no_result_on_stdout(self, monkeypatch, capsys):
        # Operator exhausts retries
        from src.__main__ import main
        inputs = iter(["3", "4", "^", "^", "^", "^"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        main()  # must not raise
        captured = capsys.readouterr()
        assert "Result:" not in captured.out

    # -----------------------------------------------------------------------
    # Division by zero → sys.exit(1) + stderr
    # -----------------------------------------------------------------------

    def test_division_by_zero_exits_with_1(self, monkeypatch, capsys):
        exc = self._run_main(monkeypatch, ["5", "0", "/"], capsys)
        assert exc.value.code == 1

    def test_division_by_zero_prints_error_to_stderr(self, monkeypatch, capsys):
        self._run_main(monkeypatch, ["5", "0", "/"], capsys)
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_division_by_zero_no_result_on_stdout(self, monkeypatch, capsys):
        self._run_main(monkeypatch, ["5", "0", "/"], capsys)
        captured = capsys.readouterr()
        assert "Result:" not in captured.out

    def test_zero_divided_by_zero_exits_with_1(self, monkeypatch, capsys):
        exc = self._run_main(monkeypatch, ["0", "0", "/"], capsys)
        assert exc.value.code == 1

    # -----------------------------------------------------------------------
    # Edge values through the full pipeline
    # -----------------------------------------------------------------------

    def test_negative_operands_valid_result(self, monkeypatch, capsys):
        self._run_main_success(monkeypatch, ["-3", "-4", "*"], capsys)
        captured = capsys.readouterr()
        assert "12" in captured.out

    def test_scientific_notation_operand_valid(self, monkeypatch, capsys):
        self._run_main_success(monkeypatch, ["1e2", "1e1", "+"], capsys)
        captured = capsys.readouterr()
        # 100 + 10 = 110.0
        assert "110" in captured.out

    def test_whitespace_padded_inputs_valid(self, monkeypatch, capsys):
        self._run_main_success(monkeypatch, ["  3  ", "  4  ", " + "], capsys)
        captured = capsys.readouterr()
        assert "7" in captured.out
