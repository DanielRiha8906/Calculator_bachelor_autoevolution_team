"""test_error_logging.py — Comprehensive tests for error logging feature.

Tests verify that:
1. Logger initialization is correct and handlers are not duplicated
2. Calculator methods log errors before raising exceptions
3. Input handlers log warnings for validation/parsing failures
4. CLI and REPL handlers log errors on dispatch failures
5. Successful operations generate no error logs
"""

import logging
import pytest
from src.logger import get_logger
from src.calculator import Calculator
from src.input_handler import ExpressionParser, InputValidator, CalculatorREPL
from src.cli import CLIHandler


# ============================================================================
# Logger Initialization Tests
# ============================================================================


class TestLoggerInitialization:
    """Tests for the get_logger() factory and handler configuration."""

    def test_get_logger_returns_logger_instance(self):
        """Test that get_logger returns a logging.Logger instance."""
        logger = get_logger("test_module")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_module"

    def test_get_logger_no_duplicate_handlers(self):
        """Test that calling get_logger twice doesn't duplicate handlers."""
        # Get logger twice with same name
        logger1 = get_logger("test_no_dup_1")
        logger2 = get_logger("test_no_dup_1")

        # Both should be the same logger instance
        assert logger1 is logger2

        # Count handlers on root logger before third call
        root = logging.getLogger()
        initial_handler_count = len(root.handlers)

        # Call get_logger a third time
        logger3 = get_logger("test_no_dup_2")

        # Handler count should not have changed
        assert len(root.handlers) == initial_handler_count

    def test_get_logger_different_module_names(self):
        """Test that get_logger returns different loggers for different names."""
        logger1 = get_logger("module.a")
        logger2 = get_logger("module.b")

        assert logger1 is not logger2
        assert logger1.name == "module.a"
        assert logger2.name == "module.b"

    def test_root_logger_has_handlers_configured(self):
        """Test that root logger has both console and file handlers."""
        root = logging.getLogger()
        # Ensure initialization by calling get_logger
        get_logger("test_handlers_init")

        # Root logger should have handlers (console and file)
        assert len(root.handlers) >= 2

    def test_console_handler_level_is_warning(self):
        """Test that console handler is set to WARNING level."""
        root = logging.getLogger()
        get_logger("test_console_level")

        # Find StreamHandler
        stream_handlers = [h for h in root.handlers if isinstance(h, logging.StreamHandler)]
        assert len(stream_handlers) > 0
        # StreamHandler should be set to WARNING or higher
        stream_handler = stream_handlers[0]
        assert stream_handler.level >= logging.WARNING or stream_handler.level == logging.WARNING

    def test_file_handler_level_is_debug(self):
        """Test that file handler is set to DEBUG level."""
        root = logging.getLogger()
        get_logger("test_file_level")

        # Find FileHandler
        file_handlers = [h for h in root.handlers if isinstance(h, logging.FileHandler)]
        assert len(file_handlers) > 0
        file_handler = file_handlers[0]
        assert file_handler.level == logging.DEBUG


# ============================================================================
# Calculator Error Logging Tests
# ============================================================================


class TestCalculatorDivisionLogging:
    """Tests that division errors generate error logs."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a fresh Calculator instance."""
        return Calculator()

    def test_divide_by_zero_raises_and_logs_error(self, calculator, caplog):
        """Test that divide(a, 0) raises ZeroDivisionError and logs ERROR."""
        caplog.set_level(logging.DEBUG)

        with pytest.raises(ZeroDivisionError):
            calculator.divide(1, 0)

        # Check that an ERROR log record was generated
        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) > 0
        assert "divide() failed" in error_records[0].message

    def test_divide_success_no_error_logs(self, calculator, caplog):
        """Test that successful division generates no ERROR logs."""
        caplog.set_level(logging.DEBUG)

        result = calculator.divide(10, 2)
        assert result == 5

        # Check that no ERROR logs were generated
        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) == 0

    @pytest.mark.parametrize("a,b", [
        (5, 2),
        (0, 5),
        (10.5, 3),
        (1, 0.5),
    ])
    def test_divide_valid_operands_no_error_logs(self, calculator, caplog, a, b):
        """Test that divide with valid operands generates no error logs."""
        caplog.set_level(logging.DEBUG)

        result = calculator.divide(a, b)
        assert result == a / b

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) == 0


class TestCalculatorFactorialLogging:
    """Tests that factorial errors generate error logs."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a fresh Calculator instance."""
        return Calculator()

    @pytest.mark.parametrize("n", [-1, -5, -100])
    def test_factorial_negative_raises_and_logs_error(self, calculator, caplog, n):
        """Test that factorial(negative) raises ValueError and logs ERROR."""
        caplog.set_level(logging.DEBUG)

        with pytest.raises(ValueError):
            calculator.factorial(n)

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) > 0
        assert "factorial() failed" in error_records[0].message

    @pytest.mark.parametrize("n", [1.5, 2.0, "5", None, [], {}])
    def test_factorial_non_integer_raises_and_logs_error(self, calculator, caplog, n):
        """Test that factorial(non-int) raises TypeError and logs ERROR."""
        caplog.set_level(logging.DEBUG)

        with pytest.raises(TypeError):
            calculator.factorial(n)

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) > 0
        assert "factorial() failed" in error_records[0].message

    @pytest.mark.parametrize("n,expected", [
        (0, 1),
        (1, 1),
        (5, 120),
        (10, 3628800),
    ])
    def test_factorial_valid_input_no_error_logs(self, calculator, caplog, n, expected):
        """Test that factorial with valid input generates no error logs."""
        caplog.set_level(logging.DEBUG)

        result = calculator.factorial(n)
        assert result == expected

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) == 0


class TestCalculatorSquareRootLogging:
    """Tests that square_root errors generate error logs."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a fresh Calculator instance."""
        return Calculator()

    @pytest.mark.parametrize("x", [-1, -0.5, -100])
    def test_square_root_negative_raises_and_logs_error(self, calculator, caplog, x):
        """Test that square_root(negative) raises ValueError and logs ERROR."""
        caplog.set_level(logging.DEBUG)

        with pytest.raises(ValueError):
            calculator.square_root(x)

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) > 0
        assert "square_root() failed" in error_records[0].message

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (4, 2),
        (9, 3),
        (0.25, 0.5),
    ])
    def test_square_root_valid_input_no_error_logs(self, calculator, caplog, x, expected):
        """Test that square_root with valid input generates no error logs."""
        caplog.set_level(logging.DEBUG)

        result = calculator.square_root(x)
        assert result == pytest.approx(expected)

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) == 0


class TestCalculatorNaturalLogLogging:
    """Tests that natural_log errors generate error logs."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a fresh Calculator instance."""
        return Calculator()

    @pytest.mark.parametrize("x", [0, -1, -0.5])
    def test_natural_log_non_positive_raises_and_logs_error(self, calculator, caplog, x):
        """Test that natural_log(non-positive) raises ValueError and logs ERROR."""
        caplog.set_level(logging.DEBUG)

        with pytest.raises(ValueError):
            calculator.natural_log(x)

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) > 0
        assert "natural_log() failed" in error_records[0].message

    @pytest.mark.parametrize("x", [1, 2.5, 10])
    def test_natural_log_valid_input_no_error_logs(self, calculator, caplog, x):
        """Test that natural_log with valid input generates no error logs."""
        caplog.set_level(logging.DEBUG)

        result = calculator.natural_log(x)
        assert result == pytest.approx(__import__('math').log(x))

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) == 0


class TestCalculatorLogBase10Logging:
    """Tests that log_base_10 errors generate error logs."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a fresh Calculator instance."""
        return Calculator()

    @pytest.mark.parametrize("x", [0, -1, -0.5])
    def test_log_base_10_non_positive_raises_and_logs_error(self, calculator, caplog, x):
        """Test that log_base_10(non-positive) raises ValueError and logs ERROR."""
        caplog.set_level(logging.DEBUG)

        with pytest.raises(ValueError):
            calculator.log_base_10(x)

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) > 0
        assert "log_base_10() failed" in error_records[0].message

    @pytest.mark.parametrize("x", [1, 10, 100])
    def test_log_base_10_valid_input_no_error_logs(self, calculator, caplog, x):
        """Test that log_base_10 with valid input generates no error logs."""
        caplog.set_level(logging.DEBUG)

        result = calculator.log_base_10(x)
        assert result == pytest.approx(__import__('math').log10(x))

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) == 0


# ============================================================================
# Input Handler Parsing Logging Tests
# ============================================================================


class TestExpressionParserLogging:
    """Tests that expression parser failures generate warning logs."""

    @pytest.fixture
    def parser(self):
        """Fixture providing a fresh ExpressionParser instance."""
        return ExpressionParser()

    def test_parse_empty_input_raises_and_logs_warning(self, parser, caplog):
        """Test that parse('') raises ValueError and logs WARNING."""
        caplog.set_level(logging.DEBUG)

        with pytest.raises(ValueError):
            parser.parse("")

        warning_records = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warning_records) > 0
        assert "parse() failed" in warning_records[0].message

    def test_coerce_numeric_invalid_string_raises_and_logs_warning(self, parser, caplog):
        """Test that _coerce_numeric('abc') raises ValueError and logs WARNING."""
        caplog.set_level(logging.DEBUG)

        with pytest.raises(ValueError):
            parser._coerce_numeric("abc")

        warning_records = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warning_records) > 0
        assert "_coerce_numeric() failed" in warning_records[0].message

    @pytest.mark.parametrize("invalid_token", ["abc", "12.34.56", "1e2e3", "xyz123"])
    def test_parse_invalid_operands_raises_and_logs_warning(self, parser, caplog, invalid_token):
        """Test that parse with invalid operands logs WARNING."""
        caplog.set_level(logging.DEBUG)

        with pytest.raises(ValueError):
            parser.parse(f"add 5 {invalid_token}")

        warning_records = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warning_records) > 0

    @pytest.mark.parametrize("valid_input,expected_op,expected_count", [
        ("add 5 3", "add", 2),
        ("square 7", "square", 1),
        ("divide 10 2", "divide", 2),
    ])
    def test_parse_valid_input_no_warning_logs(self, parser, caplog, valid_input, expected_op, expected_count):
        """Test that parse with valid input generates no WARNING logs."""
        caplog.set_level(logging.DEBUG)

        operation, operands = parser.parse(valid_input)
        assert operation == expected_op
        assert len(operands) == expected_count

        warning_records = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warning_records) == 0


# ============================================================================
# Input Validator Logging Tests
# ============================================================================


class TestInputValidatorLogging:
    """Tests that input validation failures generate warning logs."""

    @pytest.fixture
    def validator(self):
        """Fixture providing a fresh InputValidator instance."""
        return InputValidator()

    def test_validate_operation_unknown_op_raises_and_logs_warning(self, validator, caplog):
        """Test that validate_operation('unknown_op') raises ValueError and logs WARNING."""
        caplog.set_level(logging.DEBUG)

        with pytest.raises(ValueError):
            validator.validate_operation("unknown_op")

        warning_records = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warning_records) > 0
        assert "validate_operation() failed" in warning_records[0].message

    def test_validate_operand_count_wrong_count_raises_and_logs_warning(self, validator, caplog):
        """Test that validate_operand_count with wrong count raises ValueError and logs WARNING."""
        caplog.set_level(logging.DEBUG)

        with pytest.raises(ValueError):
            validator.validate_operand_count("add", [1])

        warning_records = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warning_records) > 0
        assert "validate_operand_count() failed" in warning_records[0].message

    @pytest.mark.parametrize("operation,operands", [
        ("add", [1, 2]),
        ("square", [5]),
        ("divide", [10, 2]),
        ("factorial", [5]),
    ])
    def test_validate_valid_operation_and_operands_no_warning_logs(self, validator, caplog, operation, operands):
        """Test that validate with valid inputs generates no WARNING logs."""
        caplog.set_level(logging.DEBUG)

        validator.validate(operation, operands)

        warning_records = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warning_records) == 0


# ============================================================================
# REPL Error Logging Tests
# ============================================================================


class TestCalculatorREPLLogging:
    """Tests that CalculatorREPL._evaluate() logs errors during dispatch."""

    @pytest.fixture
    def repl(self):
        """Fixture providing a fresh CalculatorREPL instance."""
        return CalculatorREPL(Calculator())

    def test_evaluate_divide_by_zero_logs_error(self, repl, caplog):
        """Test that _evaluate('divide 1 0') logs ERROR record."""
        caplog.set_level(logging.DEBUG)

        result = repl._evaluate("divide 1 0")

        # Should return error message, not raise
        assert "division by zero" in result.lower()

        # Should have logged at least one ERROR (from divide() and from _evaluate())
        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) > 0
        # Check that the REPL logged the dispatch error
        repl_error_records = [r for r in error_records if "_evaluate() dispatch error" in r.message]
        assert len(repl_error_records) > 0

    def test_evaluate_invalid_operand_count_no_dispatch_error_logs(self, repl, caplog):
        """Test that _evaluate with wrong operand count doesn't log dispatch error."""
        caplog.set_level(logging.DEBUG)

        result = repl._evaluate("add 5")

        # Should return validation error message
        assert "Validation error" in result

        # No ERROR logs from dispatch (validation fails before dispatch)
        error_records = [r for r in caplog.records if r.levelno == logging.ERROR and "_evaluate() dispatch" in r.message]
        assert len(error_records) == 0

    def test_evaluate_valid_expression_no_error_logs(self, repl, caplog):
        """Test that _evaluate with valid expression generates no ERROR logs."""
        caplog.set_level(logging.DEBUG)

        result = repl._evaluate("add 5 3")

        assert "Result: 8" in result

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) == 0

    @pytest.mark.parametrize("expression", [
        "add 5 3",
        "multiply 4 5",
        "divide 10 2",
        "square 5",
    ])
    def test_evaluate_various_valid_expressions_no_error_logs(self, repl, caplog, expression):
        """Test that various valid expressions generate no error logs."""
        caplog.set_level(logging.DEBUG)

        result = repl._evaluate(expression)

        assert result.startswith("Result:")

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) == 0


# ============================================================================
# CLI Handler Error Logging Tests
# ============================================================================


class TestCLIHandlerLogging:
    """Tests that CLIHandler.run() logs errors during execution."""

    def test_cli_divide_by_zero_logs_error(self, caplog):
        """Test that CLIHandler on 'divide 1 0' logs ERROR."""
        caplog.set_level(logging.DEBUG)

        handler = CLIHandler("divide 1 0")
        exit_code = handler.run()

        # Should return exit code 1
        assert exit_code == 1

        # Should have logged at least one ERROR (from divide() and from CLIHandler.run())
        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) > 0
        # Check that CLIHandler logged the error
        cli_error_records = [r for r in error_records if "CLIHandler.run()" in r.message]
        assert len(cli_error_records) > 0

    def test_cli_valid_expression_no_error_logs(self, caplog):
        """Test that CLIHandler with valid expression generates no error logs."""
        caplog.set_level(logging.DEBUG)

        handler = CLIHandler("add 5 3")
        exit_code = handler.run()

        assert exit_code == 0

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) == 0

    @pytest.mark.parametrize("expression,expected_exit_code", [
        ("add 5 3", 0),
        ("multiply 4 5", 0),
        ("square 7", 0),
    ])
    def test_cli_various_valid_expressions_no_error_logs(self, caplog, expression, expected_exit_code):
        """Test that various valid expressions generate no error logs."""
        caplog.set_level(logging.DEBUG)

        handler = CLIHandler(expression)
        exit_code = handler.run()

        assert exit_code == expected_exit_code

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) == 0


# ============================================================================
# Edge Case Tests
# ============================================================================


class TestEdgeCases:
    """Additional edge case tests for comprehensive coverage."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a fresh Calculator instance."""
        return Calculator()

    def test_divide_zero_by_nonzero_no_error_logs(self, calculator, caplog):
        """Test that 0 ÷ 5 succeeds and generates no error logs."""
        caplog.set_level(logging.DEBUG)

        result = calculator.divide(0, 5)
        assert result == 0

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) == 0

    def test_natural_log_negative_one_raises_and_logs_error(self, calculator, caplog):
        """Test that natural_log(-1) raises ValueError and logs ERROR."""
        caplog.set_level(logging.DEBUG)

        with pytest.raises(ValueError):
            calculator.natural_log(-1)

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) > 0
        assert "natural_log() failed" in error_records[0].message

    def test_factorial_zero_succeeds_no_error_logs(self, calculator, caplog):
        """Test that factorial(0) succeeds and generates no error logs."""
        caplog.set_level(logging.DEBUG)

        result = calculator.factorial(0)
        assert result == 1

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) == 0

    def test_log_base_10_zero_raises_and_logs_error(self, calculator, caplog):
        """Test that log_base_10(0) raises ValueError and logs ERROR."""
        caplog.set_level(logging.DEBUG)

        with pytest.raises(ValueError):
            calculator.log_base_10(0)

        error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(error_records) > 0
        assert "log_base_10() failed" in error_records[0].message
