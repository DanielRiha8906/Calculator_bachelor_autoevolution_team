"""test_input_handler.py — comprehensive unit and integration tests for input handling.

Tests cover:
- InputValidator: operation name validation and operand count checking
- ExpressionParser: parsing expressions and coercing numeric types
- CalculatorREPL: execution, error handling, and exit conditions
- RetryConfig: configuration for bad-input retry behavior
- Retry logic: REPL re-prompts user on invalid input up to max_retries times
"""

import pytest
from io import StringIO
from unittest.mock import patch, MagicMock

from src import Calculator, InputValidator, ExpressionParser, CalculatorREPL
from src.input_handler import (
    SUPPORTED_OPERATIONS,
    _ONE_OPERAND_OPS,
    _TWO_OPERAND_OPS,
    RetryConfig,
)


# =============================================================================
# TestRetryConfig
# =============================================================================


class TestRetryConfig:
    """Unit tests for RetryConfig dataclass."""

    def test_default_max_retries_is_three(self):
        """Test that RetryConfig() has max_retries == 3 by default."""
        config = RetryConfig()
        assert config.max_retries == 3

    def test_max_retries_can_be_customized(self):
        """Test that RetryConfig(max_retries=5) has max_retries == 5."""
        config = RetryConfig(max_retries=5)
        assert config.max_retries == 5

    @pytest.mark.parametrize("custom_max", [1, 2, 5, 10])
    def test_max_retries_can_be_set_to_various_values(self, custom_max):
        """Test that max_retries can be set to various positive integers."""
        config = RetryConfig(max_retries=custom_max)
        assert config.max_retries == custom_max


# =============================================================================
# TestInputValidator
# =============================================================================


class TestInputValidator:
    """Unit tests for InputValidator class."""

    @pytest.fixture
    def validator(self):
        """Provide a fresh InputValidator instance."""
        return InputValidator()

    # -------------------------------------------------------------------------
    # validate_operation tests
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize("operation", sorted(SUPPORTED_OPERATIONS))
    def test_validate_operation_all_supported_operations_pass(self, validator, operation):
        """Test that validate_operation accepts all supported operation names."""
        # Should not raise
        validator.validate_operation(operation)

    @pytest.mark.parametrize("invalid_op", [
        "unknown",
        "sqrt",  # Not 'square_root'
        "ln",    # Not 'natural_log'
        "log",   # Not 'log_base_10'
        "sin",
        "cos",
        "tan",
        "",
        "ADD",  # Wrong case (but this is already lowercased by parser)
        "123",
        "!",
        " add",  # Whitespace
        "add ",  # Trailing whitespace
    ])
    def test_validate_operation_unsupported_operations_raise_valueerror(
        self, validator, invalid_op
    ):
        """Test that validate_operation raises ValueError for unknown operations."""
        with pytest.raises(ValueError) as exc_info:
            validator.validate_operation(invalid_op)
        assert "Unknown operation" in str(exc_info.value)
        assert invalid_op in str(exc_info.value) or invalid_op.strip() in str(exc_info.value)

    # -------------------------------------------------------------------------
    # validate_operand_count tests
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize("operation,operands", [
        ("add", [5, 3]),
        ("subtract", [10, 4]),
        ("multiply", [2, 3]),
        ("divide", [10, 2]),
        ("power", [2, 8]),
        ("factorial", [5]),
        ("square", [7]),
        ("cube", [3]),
        ("square_root", [16]),
        ("cube_root", [8]),
        ("natural_log", [2.718]),
        ("log_base_10", [100]),
    ])
    def test_validate_operand_count_correct_operand_counts_pass(
        self, validator, operation, operands
    ):
        """Test that validate_operand_count accepts correct operand counts."""
        # Should not raise
        validator.validate_operand_count(operation, operands)

    @pytest.mark.parametrize("operation,operands", [
        ("add", []),           # 0 operands for 2-operand op
        ("add", [5]),          # 1 operand for 2-operand op
        ("add", [5, 3, 2]),    # 3 operands for 2-operand op
        ("divide", [10]),      # 1 operand for 2-operand op
        ("factorial", []),     # 0 operands for 1-operand op
        ("factorial", [5, 3]), # 2 operands for 1-operand op
        ("square", [5, 3]),    # 2 operands for 1-operand op
        ("square_root", [16, 2]),  # 2 operands for 1-operand op
    ])
    def test_validate_operand_count_wrong_counts_raise_valueerror(
        self, validator, operation, operands
    ):
        """Test that validate_operand_count raises ValueError for incorrect counts."""
        with pytest.raises(ValueError) as exc_info:
            validator.validate_operand_count(operation, operands)
        assert "expects" in str(exc_info.value).lower()

    # -------------------------------------------------------------------------
    # validate (combined) tests
    # -------------------------------------------------------------------------

    def test_validate_combined_valid_expression(self, validator):
        """Test validate method with valid operation and operands."""
        # Should not raise
        validator.validate("add", [5, 3])
        validator.validate("factorial", [5])

    def test_validate_combined_invalid_operation_raises_valueerror(self, validator):
        """Test validate method raises on invalid operation before checking operands."""
        with pytest.raises(ValueError) as exc_info:
            validator.validate("unknown_op", [5, 3])
        assert "Unknown operation" in str(exc_info.value)

    def test_validate_combined_invalid_operand_count_raises_valueerror(self, validator):
        """Test validate method raises on invalid operand count after operation is valid."""
        with pytest.raises(ValueError) as exc_info:
            validator.validate("add", [5])  # Valid operation, wrong operand count
        assert "expects" in str(exc_info.value).lower()


# =============================================================================
# TestExpressionParser
# =============================================================================


class TestExpressionParser:
    """Unit tests for ExpressionParser class."""

    @pytest.fixture
    def parser(self):
        """Provide a fresh ExpressionParser instance."""
        return ExpressionParser()

    # -------------------------------------------------------------------------
    # _coerce_numeric tests
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize("token,expected_type,expected_value", [
        ("5", int, 5),
        ("0", int, 0),
        ("-3", int, -3),
        ("42", int, 42),
        ("3.14", float, 3.14),
        ("0.5", float, 0.5),
        ("-2.5", float, -2.5),
        ("1.0", float, 1.0),  # Explicit decimal -> float
        ("1e5", float, 1e5),   # Scientific notation -> float
        ("1e-3", float, 1e-3), # Negative exponent -> float
    ])
    def test_coerce_numeric_valid_numeric_strings(
        self, parser, token, expected_type, expected_value
    ):
        """Test that _coerce_numeric correctly parses valid numeric strings."""
        result = parser._coerce_numeric(token)
        assert isinstance(result, expected_type)
        assert result == expected_value

    @pytest.mark.parametrize("invalid_token", [
        "abc",
        "12.34.56",
        "1.2.3",
        "",
        " ",
        "1a",
        "a1",
        "hello",
        "5.0.0",
    ])
    def test_coerce_numeric_invalid_strings_raise_valueerror(
        self, parser, invalid_token
    ):
        """Test that _coerce_numeric raises ValueError for non-numeric strings."""
        with pytest.raises(ValueError) as exc_info:
            parser._coerce_numeric(invalid_token)
        assert "not a valid number" in str(exc_info.value) or "is not a valid number" in str(exc_info.value)

    @pytest.mark.parametrize("special_float_token", [
        "NaN",
        "inf",
        "-inf",
    ])
    def test_coerce_numeric_special_float_values_accepted(
        self, parser, special_float_token
    ):
        """Test that _coerce_numeric accepts Python's special float values (NaN, inf).

        Note: Python's float() function accepts these as valid,
        so they parse successfully even though they're mathematically special.
        """
        result = parser._coerce_numeric(special_float_token)
        assert isinstance(result, float)

    # -------------------------------------------------------------------------
    # parse tests
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize("raw_input,expected_op,expected_operands", [
        ("add 5 3", "add", [5, 3]),
        ("subtract 10 4", "subtract", [10, 4]),
        ("multiply 2 3", "multiply", [2, 3]),
        ("divide 10 2", "divide", [10, 2]),
        ("power 2 8", "power", [2, 8]),
        ("factorial 5", "factorial", [5]),
        ("square 7", "square", [7]),
        ("cube 3", "cube", [3]),
        ("square_root 16", "square_root", [16]),
        ("cube_root 8", "cube_root", [8]),
        ("natural_log 2.718", "natural_log", [2.718]),
        ("log_base_10 100", "log_base_10", [100]),
    ])
    def test_parse_valid_expressions_all_operations(
        self, parser, raw_input, expected_op, expected_operands
    ):
        """Test parse with valid expressions for all supported operations."""
        operation, operands = parser.parse(raw_input)
        assert operation == expected_op
        assert operands == expected_operands

    def test_parse_case_insensitivity(self, parser):
        """Test that parse lowercases the operation token."""
        operation, operands = parser.parse("ADD 5 3")
        assert operation == "add"
        assert operands == [5, 3]

        operation, operands = parser.parse("FaCtOrIaL 5")
        assert operation == "factorial"
        assert operands == [5]

    def test_parse_extra_whitespace(self, parser):
        """Test that parse handles extra whitespace correctly."""
        operation, operands = parser.parse("  add   5   3  ")
        assert operation == "add"
        assert operands == [5, 3]

        operation, operands = parser.parse("square  7")
        assert operation == "square"
        assert operands == [7]

    def test_parse_integer_valued_tokens_coerce_to_int(self, parser):
        """Test that integer-valued tokens are coerced to int type."""
        operation, operands = parser.parse("factorial 5")
        assert isinstance(operands[0], int)
        assert operands[0] == 5

        operation, operands = parser.parse("add 10 20")
        assert all(isinstance(op, int) for op in operands)

    def test_parse_fractional_tokens_coerce_to_float(self, parser):
        """Test that fractional tokens are coerced to float type."""
        operation, operands = parser.parse("natural_log 2.718")
        assert isinstance(operands[0], float)

        operation, operands = parser.parse("add 3.14 1.5")
        assert all(isinstance(op, float) for op in operands)

    def test_parse_scientific_notation_coerces_to_float(self, parser):
        """Test that scientific notation is coerced to float."""
        operation, operands = parser.parse("multiply 1e5 2e3")
        assert all(isinstance(op, float) for op in operands)
        assert operands == [1e5, 2e3]

    @pytest.mark.parametrize("empty_input", [
        "",
        "   ",
        "\t",
        "\n",
    ])
    def test_parse_empty_input_raises_valueerror(self, parser, empty_input):
        """Test that parse raises ValueError on empty input."""
        with pytest.raises(ValueError) as exc_info:
            parser.parse(empty_input)
        assert "Empty input" in str(exc_info.value)

    @pytest.mark.parametrize("invalid_input", [
        "add 5 abc",
        "multiply 3.14 hello",
        "square xyz",
        "divide 10 2.3.4",
    ])
    def test_parse_non_numeric_operands_raise_valueerror(
        self, parser, invalid_input
    ):
        """Test that parse raises ValueError when operands are not numeric."""
        with pytest.raises(ValueError) as exc_info:
            parser.parse(invalid_input)
        # Error from _coerce_numeric
        assert "not a valid number" in str(exc_info.value) or "is not a valid number" in str(exc_info.value)


# =============================================================================
# TestCalculatorREPL
# =============================================================================


class TestCalculatorREPL:
    """Unit and integration tests for CalculatorREPL class."""

    @pytest.fixture
    def calculator(self):
        """Provide a fresh Calculator instance."""
        return Calculator()

    @pytest.fixture
    def repl(self, calculator):
        """Provide a fresh CalculatorREPL instance."""
        return CalculatorREPL(calculator)

    # -------------------------------------------------------------------------
    # _evaluate tests
    # -------------------------------------------------------------------------

    def test_evaluate_valid_addition(self, repl):
        """Test _evaluate with valid addition expression."""
        result = repl._evaluate("add 5 3")
        assert result == "Result: 8"

    def test_evaluate_valid_subtraction(self, repl):
        """Test _evaluate with valid subtraction expression."""
        result = repl._evaluate("subtract 10 4")
        assert result == "Result: 6"

    def test_evaluate_valid_multiplication(self, repl):
        """Test _evaluate with valid multiplication expression."""
        result = repl._evaluate("multiply 2 3")
        assert result == "Result: 6"

    def test_evaluate_valid_division(self, repl):
        """Test _evaluate with valid division expression."""
        result = repl._evaluate("divide 10 2")
        assert result == "Result: 5.0"

    def test_evaluate_valid_power(self, repl):
        """Test _evaluate with valid power expression."""
        result = repl._evaluate("power 2 8")
        assert result == "Result: 256"

    def test_evaluate_valid_factorial(self, repl):
        """Test _evaluate with valid factorial expression."""
        result = repl._evaluate("factorial 5")
        assert result == "Result: 120"

    def test_evaluate_valid_square(self, repl):
        """Test _evaluate with valid square expression."""
        result = repl._evaluate("square 7")
        assert result == "Result: 49"

    def test_evaluate_valid_cube(self, repl):
        """Test _evaluate with valid cube expression."""
        result = repl._evaluate("cube 3")
        assert result == "Result: 27"

    def test_evaluate_valid_square_root(self, repl):
        """Test _evaluate with valid square root expression."""
        result = repl._evaluate("square_root 16")
        assert result == "Result: 4.0"

    def test_evaluate_valid_cube_root(self, repl):
        """Test _evaluate with valid cube root expression."""
        result = repl._evaluate("cube_root 8")
        assert result == "Result: 2.0"

    @pytest.mark.parametrize("raw_input,expected_prefix", [
        ("add 5 3", "Result:"),
        ("factorial 5", "Result:"),
        ("square 7", "Result:"),
    ])
    def test_evaluate_successful_expressions_start_with_result_prefix(
        self, repl, raw_input, expected_prefix
    ):
        """Test that successful evaluations return strings starting with 'Result:'."""
        result = repl._evaluate(raw_input)
        assert result.startswith(expected_prefix)

    def test_evaluate_division_by_zero_returns_math_error(self, repl):
        """Test that division by zero returns a 'Math error:' message."""
        result = repl._evaluate("divide 10 0")
        assert result.startswith("Math error:")
        assert "division by zero" in result.lower()

    def test_evaluate_empty_input_returns_input_error(self, repl):
        """Test that empty input returns an 'Input error:' message."""
        result = repl._evaluate("")
        assert result.startswith("Input error:")

    def test_evaluate_non_numeric_operand_returns_input_error(self, repl):
        """Test that non-numeric operands return an 'Input error:' message."""
        result = repl._evaluate("add 5 abc")
        assert result.startswith("Input error:")

    def test_evaluate_unknown_operation_returns_validation_error(self, repl):
        """Test that unknown operations return a 'Validation error:' message."""
        result = repl._evaluate("unknown 5 3")
        assert result.startswith("Validation error:")

    def test_evaluate_wrong_operand_count_returns_validation_error(self, repl):
        """Test that wrong operand count returns a 'Validation error:' message."""
        result = repl._evaluate("add 5")
        assert result.startswith("Validation error:")

        result = repl._evaluate("factorial 5 3")
        assert result.startswith("Validation error:")

    def test_evaluate_factorial_with_float_returns_type_error(self, repl):
        """Test that factorial with float operand returns a 'Type error:' message."""
        result = repl._evaluate("factorial 5.5")
        assert result.startswith("Type error:")

    def test_evaluate_square_root_negative_returns_math_error(self, repl):
        """Test that square root of negative number returns a 'Math error:' message."""
        result = repl._evaluate("square_root -1")
        assert result.startswith("Math error:")

    def test_evaluate_natural_log_zero_returns_math_error(self, repl):
        """Test that natural log of zero returns a 'Math error:' message."""
        result = repl._evaluate("natural_log 0")
        assert result.startswith("Math error:")

    def test_evaluate_log_base_10_negative_returns_math_error(self, repl):
        """Test that log base 10 of negative number returns a 'Math error:' message."""
        result = repl._evaluate("log_base_10 -5")
        assert result.startswith("Math error:")

    # -------------------------------------------------------------------------
    # Type preservation test (factorial must receive int, not float)
    # -------------------------------------------------------------------------

    def test_evaluate_factorial_receives_int_not_float(self, repl):
        """Test that 'factorial 5' sends int(5) to Calculator.factorial, not float(5.0)."""
        # This is critical: factorial requires int type, not float.
        # The parser must coerce "5" to int, not float.
        result = repl._evaluate("factorial 5")
        assert result.startswith("Result:")
        assert "120" in result  # 5! = 120

    def test_parse_integer_operand_preserves_int_type(self, repl):
        """Test that parsing "5" results in int(5), which factorial needs."""
        # Use _parser directly to verify type preservation
        operation, operands = repl._parser.parse("factorial 5")
        assert isinstance(operands[0], int)
        assert operands[0] == 5

    # -------------------------------------------------------------------------
    # run (integration) tests with mocked stdin
    # -------------------------------------------------------------------------

    def test_run_with_exit_command_terminates_cleanly(self, repl, capsys):
        """Test that 'exit' command terminates the REPL cleanly."""
        with patch("builtins.input", side_effect=["exit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    def test_run_with_quit_command_terminates_cleanly(self, repl, capsys):
        """Test that 'quit' command terminates the REPL cleanly."""
        with patch("builtins.input", side_effect=["quit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    def test_run_with_keyboard_interrupt_terminates_cleanly(self, repl, capsys):
        """Test that KeyboardInterrupt terminates the REPL cleanly."""
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            repl.run()

        captured = capsys.readouterr()
        assert "Interrupted" in captured.out or "Goodbye" in captured.out

    def test_run_with_eof_terminates_cleanly(self, repl, capsys):
        """Test that EOFError (piped input exhausted) terminates cleanly."""
        with patch("builtins.input", side_effect=EOFError):
            repl.run()

        captured = capsys.readouterr()
        # Should terminate without error, output may vary

    def test_run_with_valid_operation_prints_result(self, repl, capsys):
        """Test that valid operations print their results."""
        with patch("builtins.input", side_effect=["add 5 3", "exit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "Result: 8" in captured.out

    def test_run_with_invalid_operation_prints_error(self, repl, capsys):
        """Test that invalid operations print error messages."""
        with patch("builtins.input", side_effect=["unknown 5 3", "exit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "Validation error:" in captured.out or "Unknown operation" in captured.out

    def test_run_with_empty_line_skips_to_next_input(self, repl, capsys):
        """Test that empty lines are skipped without printing errors."""
        with patch("builtins.input", side_effect=["", "add 5 3", "exit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "Result: 8" in captured.out
        # Empty line should not produce error output

    def test_run_multiple_valid_operations_in_sequence(self, repl, capsys):
        """Test that REPL handles multiple valid operations correctly."""
        inputs = [
            "add 5 3",
            "multiply 2 3",
            "square 4",
            "exit",
        ]
        with patch("builtins.input", side_effect=inputs):
            repl.run()

        captured = capsys.readouterr()
        assert "Result: 8" in captured.out
        assert "Result: 6" in captured.out
        assert "Result: 16" in captured.out
        assert "Goodbye!" in captured.out

    def test_run_prints_welcome_message_with_supported_operations(self, repl, capsys):
        """Test that REPL prints welcome message and lists supported operations."""
        with patch("builtins.input", side_effect=["exit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "Calculator REPL" in captured.out
        assert "Supported operations" in captured.out
        assert "add" in captured.out
        assert "factorial" in captured.out

    # -------------------------------------------------------------------------
    # _dispatch tests
    # -------------------------------------------------------------------------

    def test_dispatch_calls_correct_method_for_binary_operations(self, repl):
        """Test that _dispatch calls the correct method for two-operand ops."""
        result = repl._dispatch("add", [5, 3])
        assert result == 8

        result = repl._dispatch("multiply", [2, 3])
        assert result == 6

    def test_dispatch_calls_correct_method_for_unary_operations(self, repl):
        """Test that _dispatch calls the correct method for one-operand ops."""
        result = repl._dispatch("factorial", [5])
        assert result == 120

        result = repl._dispatch("square", [7])
        assert result == 49

    def test_dispatch_propagates_calculator_exceptions(self, repl):
        """Test that _dispatch propagates exceptions from Calculator methods."""
        with pytest.raises(ZeroDivisionError):
            repl._dispatch("divide", [10, 0])

        with pytest.raises(TypeError):
            repl._dispatch("factorial", [5.5])

        with pytest.raises(ValueError):
            repl._dispatch("factorial", [-1])

    # -------------------------------------------------------------------------
    # Retry logic tests
    # -------------------------------------------------------------------------

    def test_repl_accepts_custom_retry_config(self, calculator):
        """Test that CalculatorREPL accepts and stores a custom RetryConfig."""
        config = RetryConfig(max_retries=5)
        repl = CalculatorREPL(calculator, retry_config=config)
        assert repl._retry_config.max_retries == 5

    def test_repl_uses_default_retry_config_when_not_provided(self, repl):
        """Test that CalculatorREPL uses default RetryConfig when none is provided."""
        assert repl._retry_config.max_retries == 3

    def test_valid_input_on_first_attempt_no_retry_prompts(self, repl, capsys):
        """Test that valid expression on first try produces no retry prompts."""
        with patch("builtins.input", side_effect=["add 5 3", "exit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "Result: 8" in captured.out
        assert "Attempt" not in captured.out
        assert "Invalid input" not in captured.out

    def test_invalid_input_triggers_retry_prompt(self, repl, capsys):
        """Test that invalid input triggers a retry prompt."""
        with patch("builtins.input", side_effect=["invalid_op 5", "exit"]) as mock_input:
            repl.run()

        captured = capsys.readouterr()
        # Error message should be printed
        assert "Validation error:" in captured.out
        # input() should be called at least twice: main prompt and retry prompt
        assert mock_input.call_count >= 2
        # Second call should be the retry prompt with "Attempt 1/3"
        retry_prompt = mock_input.call_args_list[1][0][0]
        assert "Attempt 1/3" in retry_prompt
        assert "Please try again:" in retry_prompt

    def test_max_retries_exceeded_prints_exhaustion_message(self, repl, capsys):
        """Test that three consecutive invalid inputs prints exhaustion message."""
        # First invalid input triggers retry loop
        # Attempts 1, 2, 3 all fail, then we're back at main loop and exit
        inputs = ["badop", "badop2", "badop3", "badop4", "exit"]
        with patch("builtins.input", side_effect=inputs):
            repl.run()

        captured = capsys.readouterr()
        assert "Too many invalid attempts" in captured.out
        assert "Returning to main prompt" in captured.out

    def test_retry_succeeds_on_second_attempt(self, repl, capsys):
        """Test that invalid then valid input succeeds, prints result, no exhaustion."""
        inputs = ["invalid_op 5", "add 5 3", "exit"]
        with patch("builtins.input", side_effect=inputs) as mock_input:
            repl.run()

        captured = capsys.readouterr()
        assert "Result: 8" in captured.out
        assert "Validation error:" in captured.out
        assert "Too many invalid attempts" not in captured.out
        # Verify retry prompt was triggered
        assert mock_input.call_count >= 2
        retry_prompt = mock_input.call_args_list[1][0][0]
        assert "Attempt 1/3" in retry_prompt

    def test_exit_during_retry_terminates_cleanly(self, repl, capsys):
        """Test that typing 'exit' at a retry prompt terminates cleanly."""
        inputs = ["invalid_op 5", "exit"]
        with patch("builtins.input", side_effect=inputs):
            repl.run()

        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    def test_quit_during_retry_terminates_cleanly(self, repl, capsys):
        """Test that typing 'quit' at a retry prompt terminates cleanly."""
        inputs = ["invalid_op 5", "quit"]
        with patch("builtins.input", side_effect=inputs):
            repl.run()

        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    def test_keyboard_interrupt_during_retry_exits(self, repl, capsys):
        """Test that KeyboardInterrupt during retry exits cleanly."""
        # First input is invalid (triggers retry), then KeyboardInterrupt
        def input_sequence(prompt):
            if "Attempt" in prompt:
                raise KeyboardInterrupt()
            return "invalid_op 5"

        with patch("builtins.input", side_effect=input_sequence):
            repl.run()

        captured = capsys.readouterr()
        assert "Interrupted" in captured.out or "Goodbye" in captured.out

    def test_eof_during_retry_exits_cleanly(self, repl, capsys):
        """Test that EOFError (piped input) during retry exits cleanly."""
        # First input is invalid (triggers retry), then EOFError
        def input_sequence(prompt):
            if "Attempt" in prompt:
                raise EOFError()
            return "invalid_op 5"

        with patch("builtins.input", side_effect=input_sequence):
            repl.run()

        captured = capsys.readouterr()
        # Should exit without error

    def test_custom_max_retries_limits_attempts(self, calculator, capsys):
        """Test that custom max_retries limits retry attempts correctly."""
        config = RetryConfig(max_retries=2)
        repl = CalculatorREPL(calculator, retry_config=config)

        # First invalid input, then 2 retry attempts, then back to main loop, exit
        inputs = ["badop1", "badop2", "badop3", "exit"]
        with patch("builtins.input", side_effect=inputs) as mock_input:
            repl.run()

        captured = capsys.readouterr()
        # Should show Attempt 1/2 and Attempt 2/2, but not Attempt 3/2
        assert "Too many invalid attempts" in captured.out
        # Verify from mock calls
        retry_calls = [call for call in mock_input.call_args_list
                       if "Attempt" in call[0][0]]
        assert len(retry_calls) == 2
        assert "Attempt 1/2" in retry_calls[0][0][0]
        assert "Attempt 2/2" in retry_calls[1][0][0]

    def test_retry_loop_shows_correct_attempt_numbers(self, repl, capsys):
        """Test that retry loop shows correct attempt numbers."""
        inputs = ["bad1", "bad2", "add 5 3", "exit"]
        with patch("builtins.input", side_effect=inputs) as mock_input:
            repl.run()

        captured = capsys.readouterr()
        # Verify from mock calls that we got the right attempt prompts
        retry_calls = [call for call in mock_input.call_args_list
                       if "Attempt" in call[0][0]]
        assert len(retry_calls) == 2
        assert "Attempt 1/3" in retry_calls[0][0][0]
        assert "Attempt 2/3" in retry_calls[1][0][0]
        # Should not try a 3rd time since it succeeds on the 2nd retry
        assert not any("Attempt 3/3" in call[0][0] for call in retry_calls)

    def test_successful_retry_breaks_from_retry_loop(self, repl, capsys):
        """Test that a successful evaluation breaks from the retry loop."""
        inputs = ["badop", "factorial 5", "exit"]
        with patch("builtins.input", side_effect=inputs) as mock_input:
            repl.run()

        captured = capsys.readouterr()
        assert "Result: 120" in captured.out
        # Verify only 1 retry attempt was made (success on first retry)
        retry_calls = [call for call in mock_input.call_args_list
                       if "Attempt" in call[0][0]]
        assert len(retry_calls) == 1
        assert "Attempt 1/3" in retry_calls[0][0][0]
        # Should not continue to Attempt 2/3
        assert not any("Attempt 2/3" in call[0][0] for call in retry_calls)

    def test_retry_counts_each_failed_attempt(self, repl, capsys):
        """Test that retry counter increments for each invalid attempt."""
        inputs = ["bad1", "bad2", "bad3", "bad4", "exit"]
        with patch("builtins.input", side_effect=inputs) as mock_input:
            repl.run()

        captured = capsys.readouterr()
        # Verify all three attempt prompts appear
        retry_calls = [call for call in mock_input.call_args_list
                       if "Attempt" in call[0][0]]
        assert len(retry_calls) == 3
        assert "Attempt 1/3" in retry_calls[0][0][0]
        assert "Attempt 2/3" in retry_calls[1][0][0]
        assert "Attempt 3/3" in retry_calls[2][0][0]

    def test_different_error_types_all_trigger_retry(self, repl, capsys):
        """Test that different error types (validation, input, math) all trigger retry."""
        inputs = [
            "unknown 5 3",  # Validation error
            "add 5",  # Validation error (wrong operand count)
            "add 5 abc",  # Input error
            "divide 10 0",  # Math error
            "exit",
        ]
        with patch("builtins.input", side_effect=inputs) as mock_input:
            repl.run()

        captured = capsys.readouterr()
        # Verify retry was triggered
        retry_calls = [call for call in mock_input.call_args_list
                       if "Attempt" in call[0][0]]
        assert len(retry_calls) >= 1
        assert "Attempt 1" in retry_calls[0][0][0]

    def test_run_invalid_then_valid_succeeds_on_retry(self, calculator, capsys):
        """Integration: User enters invalid expression, then valid one on retry."""
        repl = CalculatorREPL(calculator)
        inputs = ["unknown_operation 5", "add 10 20", "exit"]
        with patch("builtins.input", side_effect=inputs) as mock_input:
            repl.run()

        captured = capsys.readouterr()
        assert "Validation error:" in captured.out
        assert "Result: 30" in captured.out
        # Verify retry prompt was triggered
        retry_calls = [call for call in mock_input.call_args_list
                       if "Attempt" in call[0][0]]
        assert len(retry_calls) >= 1
        assert "Attempt 1/3" in retry_calls[0][0][0]

    def test_run_exhausts_retries_then_continues_at_prompt(self, calculator, capsys):
        """Integration: User exhausts retries, then gets back to main prompt."""
        repl = CalculatorREPL(calculator)
        inputs = [
            "badop1",
            "badop2",
            "badop3",
            "badop4",
            "add 5 3",
            "exit",
        ]
        with patch("builtins.input", side_effect=inputs):
            repl.run()

        captured = capsys.readouterr()
        assert "Too many invalid attempts" in captured.out
        assert "Returning to main prompt" in captured.out
        # Should return to main prompt and accept the valid input
        assert "Result: 8" in captured.out


# =============================================================================
# Integration: Exports
# =============================================================================


class TestModuleExports:
    """Test that the module exports are correct."""

    def test_imports_from_src_package(self):
        """Test that InputValidator, ExpressionParser, CalculatorREPL are exported."""
        from src import InputValidator, ExpressionParser, CalculatorREPL

        assert InputValidator is not None
        assert ExpressionParser is not None
        assert CalculatorREPL is not None

    def test_supported_operations_contains_all_operations(self):
        """Test that SUPPORTED_OPERATIONS includes both one and two operand ops."""
        assert _ONE_OPERAND_OPS.issubset(SUPPORTED_OPERATIONS)
        assert _TWO_OPERAND_OPS.issubset(SUPPORTED_OPERATIONS)
        assert SUPPORTED_OPERATIONS == _ONE_OPERAND_OPS | _TWO_OPERAND_OPS

    def test_supported_operations_contains_expected_names(self):
        """Test that SUPPORTED_OPERATIONS contains the expected operation names."""
        expected_ops = {
            "add", "subtract", "multiply", "divide", "power",
            "factorial", "square", "cube", "square_root", "cube_root",
            "natural_log", "log_base_10",
        }
        assert SUPPORTED_OPERATIONS == expected_ops
