"""Comprehensive test suite for calculator documentation.

Tests cover:
- Documentation files exist and are not empty
- All public classes and functions have docstrings
- Code examples in documentation are syntactically valid Python
- Specific functional requirements from documentation
- Edge cases mentioned in the API reference
"""

import ast
import logging
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from src.logic import Calculator
from src.presentation.cli import parse_and_evaluate
from src.logging_config import setup_logging


# ============================================================================
# DOCUMENTATION FILE EXISTENCE AND CONTENT TESTS
# ============================================================================

class TestDocumentationFilesExist:
    """Test that all documented files exist and are not empty."""

    def test_docs_readme_exists_and_not_empty(self):
        """Verify docs/README.md exists and has content."""
        docs_readme = Path("docs/README.md")
        assert docs_readme.exists(), "docs/README.md does not exist"
        assert docs_readme.stat().st_size > 0, "docs/README.md is empty"

    def test_docs_architecture_exists_and_not_empty(self):
        """Verify docs/ARCHITECTURE.md exists and has content."""
        arch_doc = Path("docs/ARCHITECTURE.md")
        assert arch_doc.exists(), "docs/ARCHITECTURE.md does not exist"
        assert arch_doc.stat().st_size > 0, "docs/ARCHITECTURE.md is empty"

    def test_docs_api_reference_exists_and_not_empty(self):
        """Verify docs/API_REFERENCE.md exists and has content."""
        api_doc = Path("docs/API_REFERENCE.md")
        assert api_doc.exists(), "docs/API_REFERENCE.md does not exist"
        assert api_doc.stat().st_size > 0, "docs/API_REFERENCE.md is empty"

    def test_docs_user_guide_exists_and_not_empty(self):
        """Verify docs/USER_GUIDE.md exists and has content."""
        user_guide = Path("docs/USER_GUIDE.md")
        assert user_guide.exists(), "docs/USER_GUIDE.md does not exist"
        assert user_guide.stat().st_size > 0, "docs/USER_GUIDE.md is empty"

    def test_docs_extending_exists_and_not_empty(self):
        """Verify docs/EXTENDING.md exists and has content."""
        extending_doc = Path("docs/EXTENDING.md")
        assert extending_doc.exists(), "docs/EXTENDING.md does not exist"
        assert extending_doc.stat().st_size > 0, "docs/EXTENDING.md is empty"

    def test_root_readme_exists_and_not_empty(self):
        """Verify root README.md exists and has content."""
        root_readme = Path("README.md")
        assert root_readme.exists(), "README.md does not exist"
        assert root_readme.stat().st_size > 0, "README.md is empty"


# ============================================================================
# PUBLIC DOCSTRING VERIFICATION TESTS
# ============================================================================

class TestPublicDocstrings:
    """Test that all public classes and functions have docstrings."""

    def _get_public_members(self, module_path):
        """Extract public classes and functions from a Python file."""
        with open(module_path, 'r') as f:
            tree = ast.parse(f.read())

        public_items = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                # Only top-level definitions (not nested)
                if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                    # Check if it's public (doesn't start with _)
                    if not node.name.startswith('_'):
                        public_items.append((node.name, type(node).__name__))

        return public_items

    def test_logic_calculator_has_docstrings(self):
        """Verify Calculator class and all public methods have docstrings."""
        module_path = Path("src/logic/state.py")
        with open(module_path, 'r') as f:
            tree = ast.parse(f.read())

        # Find Calculator class
        calculator_class = None
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "Calculator":
                calculator_class = node
                break

        assert calculator_class is not None, "Calculator class not found"
        assert ast.get_docstring(calculator_class), "Calculator class missing docstring"

        # Check public methods
        public_methods = [
            n.name for n in calculator_class.body
            if isinstance(n, ast.FunctionDef) and not n.name.startswith('_')
        ]
        assert len(public_methods) > 0, "No public methods found in Calculator"

        for method_name in public_methods:
            method = next(
                n for n in calculator_class.body
                if isinstance(n, ast.FunctionDef) and n.name == method_name
            )
            assert ast.get_docstring(method), f"Method Calculator.{method_name} missing docstring"

    def test_presentation_cli_has_docstrings(self):
        """Verify parse_and_evaluate and run_cli have docstrings."""
        module_path = Path("src/presentation/cli.py")
        with open(module_path, 'r') as f:
            tree = ast.parse(f.read())

        # Find public functions
        public_functions = {
            n.name: n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and not n.name.startswith('_')
        }

        assert "parse_and_evaluate" in public_functions, "parse_and_evaluate not found"
        assert "run_cli" in public_functions, "run_cli not found"

        for func_name in ["parse_and_evaluate", "run_cli"]:
            func = public_functions[func_name]
            docstring = ast.get_docstring(func)
            assert docstring, f"Function {func_name} missing docstring"

    def test_logging_config_has_docstrings(self):
        """Verify setup_logging function has a docstring."""
        module_path = Path("src/logging_config.py")
        with open(module_path, 'r') as f:
            tree = ast.parse(f.read())

        setup_logging_func = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "setup_logging":
                setup_logging_func = node
                break

        assert setup_logging_func is not None, "setup_logging function not found"
        assert ast.get_docstring(setup_logging_func), "setup_logging missing docstring"


# ============================================================================
# CODE EXAMPLES VALIDATION TESTS
# ============================================================================

class TestDocumentationCodeExamples:
    """Test that code examples in documentation are syntactically valid Python."""

    def _extract_executable_code_blocks(self, doc_path):
        """Extract executable Python code blocks from a markdown file.

        Filters out function/class signature blocks and other non-executable
        code snippets that are documentation artifacts.
        """
        with open(doc_path, 'r') as f:
            content = f.read()

        # Match ```python ... ``` blocks (with newlines)
        pattern = r'```python\n(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)

        # Filter out single-line signatures and incomplete code
        executable = []
        for block in matches:
            lines = [line.strip() for line in block.strip().split('\n') if line.strip()]

            if not lines:
                continue

            # Skip if it's just a function/class signature without implementation
            if len(lines) == 1 and (
                lines[0].startswith('def ') or
                lines[0].startswith('class ') or
                lines[0].startswith('@') or
                ('def ' in lines[0] and '->' in lines[0]) or
                ('class ' in lines[0])
            ):
                continue

            # Skip blocks that are just decorators + bare signature (no colon, no body)
            if len(lines) == 2:
                if lines[0].startswith('@') and ('def ' in lines[1] or 'class ' in lines[1]):
                    continue

            # Skip incomplete snippets
            if any(line.startswith('...') for line in lines):
                continue

            # Skip pure type declaration lines (like "logger: logging.Logger")
            if len(lines) == 1 and ':' in lines[0] and '=' not in lines[0] and 'def ' not in lines[0]:
                continue

            # Skip OPERATIONS constant type declaration
            if len(lines) == 1 and 'OPERATIONS' in lines[0] and 'dict' in lines[0]:
                continue

            # Skip multi-line function/class signatures without body
            # These end with ) -> Type or ) -> None without a colon
            last_line = lines[-1]
            if not last_line.endswith(':'):
                # Check if this looks like the end of a function signature
                if ('def ' in block and '->' in last_line) or (')' in last_line and '->' in last_line):
                    # This is likely a signature without body, skip it
                    continue

            executable.append(block)

        return executable

    def test_api_reference_examples_are_valid_python(self):
        """Verify executable Python code blocks in API_REFERENCE.md are syntactically valid."""
        code_blocks = self._extract_executable_code_blocks(Path("docs/API_REFERENCE.md"))
        # API_REFERENCE has many signature blocks, so just ensure we have some executable blocks
        assert len(code_blocks) > 0, "No executable code blocks found in API_REFERENCE.md"

        for i, code_block in enumerate(code_blocks):
            try:
                ast.parse(code_block)
            except SyntaxError as e:
                pytest.fail(f"Code block {i} in API_REFERENCE.md has syntax error: {e}\n{code_block}")

    def test_architecture_examples_are_valid_python(self):
        """Verify executable Python code blocks in ARCHITECTURE.md are syntactically valid."""
        code_blocks = self._extract_executable_code_blocks(Path("docs/ARCHITECTURE.md"))
        # ARCHITECTURE.md uses ASCII diagrams, so 0 executable blocks is OK
        for i, code_block in enumerate(code_blocks):
            try:
                ast.parse(code_block)
            except SyntaxError as e:
                pytest.fail(f"Code block {i} in ARCHITECTURE.md has syntax error: {e}\n{code_block}")

    def test_extending_examples_are_valid_python(self):
        """Verify executable Python code blocks in EXTENDING.md are syntactically valid."""
        code_blocks = self._extract_executable_code_blocks(Path("docs/EXTENDING.md"))
        assert len(code_blocks) > 0, "No executable code blocks found in EXTENDING.md"

        for i, code_block in enumerate(code_blocks):
            try:
                ast.parse(code_block)
            except SyntaxError as e:
                pytest.fail(f"Code block {i} in EXTENDING.md has syntax error: {e}\n{code_block}")


# ============================================================================
# CLI FUNCTIONAL TESTS FROM DOCUMENTATION
# ============================================================================

class TestCLIExamplesFromDocumentation:
    """Test the specific CLI examples mentioned in documentation."""

    def test_cli_simple_addition_3_plus_4(self):
        """Test the documented example: python -m src "3 + 4" prints 7."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "3 + 4"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"CLI failed with stderr: {result.stderr}"
        assert "7" in result.stdout, f"Expected '7' in output, got: {result.stdout}"

    def test_cli_power_and_division_2_power_10_div_8(self):
        """Test the documented example: python -m src "2 ** 10 / 8" prints 128.0."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "2 ** 10 / 8"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"CLI failed with stderr: {result.stderr}"
        assert "128.0" in result.stdout, f"Expected '128.0' in output, got: {result.stdout}"


# ============================================================================
# parse_and_evaluate FUNCTIONAL TESTS FROM API_REFERENCE
# ============================================================================

class TestParseAndEvaluateFunctionality:
    """Test parse_and_evaluate function with examples and edge cases from API_REFERENCE."""

    @pytest.fixture
    def calculator(self):
        """Provide a fresh Calculator instance."""
        return Calculator()

    def test_parse_and_evaluate_simple_expression(self, calculator):
        """Test parse_and_evaluate with simple expression."""
        result = parse_and_evaluate("2 + 3", calculator)
        assert result == 5, f"Expected 5, got {result}"

    def test_parse_and_evaluate_complex_expression(self, calculator):
        """Test parse_and_evaluate with parentheses and multiple operations."""
        result = parse_and_evaluate("(3 + 4) * 2", calculator)
        assert result == 14, f"Expected 14, got {result}"

    def test_parse_and_evaluate_power_expression(self, calculator):
        """Test parse_and_evaluate with power operator."""
        result = parse_and_evaluate("2 ** 10", calculator)
        assert result == 1024, f"Expected 1024, got {result}"

    def test_parse_and_evaluate_empty_string_raises_valueerror(self, calculator):
        """Test that empty expression raises ValueError."""
        with pytest.raises(ValueError, match="Expression must not be empty"):
            parse_and_evaluate("", calculator)

    def test_parse_and_evaluate_whitespace_only_raises_valueerror(self, calculator):
        """Test that whitespace-only expression raises ValueError."""
        with pytest.raises(ValueError, match="Expression must not be empty"):
            parse_and_evaluate("   ", calculator)

    def test_parse_and_evaluate_unsupported_operator_raises_valueerror(self, calculator):
        """Test that unsupported operator raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported"):
            parse_and_evaluate("5 % 3", calculator)

    def test_parse_and_evaluate_invalid_syntax_raises_valueerror(self, calculator):
        """Test that syntax error raises ValueError."""
        # Note: "5 + + 3" is actually valid (unary plus), so use truly invalid syntax
        with pytest.raises(ValueError):
            parse_and_evaluate("5 + * 3", calculator)


# ============================================================================
# CALCULATOR SPECIFIC FUNCTIONALITY TESTS
# ============================================================================

class TestCalculatorFactorialFromAPI:
    """Test Calculator.factorial with examples from API_REFERENCE."""

    @pytest.fixture
    def calculator(self):
        """Provide a fresh Calculator instance."""
        return Calculator()

    def test_factorial_5_returns_120(self, calculator):
        """Test the documented example: calc.factorial(5) returns 120."""
        result = calculator.factorial(5)
        assert result == 120, f"Expected 120, got {result}"

    def test_factorial_float_5_0_returns_120(self, calculator):
        """Test documented behavior: factorial(5.0) returns 120 (float with integer value accepted)."""
        result = calculator.factorial(5.0)
        assert result == 120, f"Expected 120, got {result}"

    def test_factorial_negative_1_raises_valueerror(self, calculator):
        """Test documented behavior: factorial(-1) raises ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(-1)


class TestCalculatorCubeRootFromAPI:
    """Test Calculator.cube_root with examples from API_REFERENCE."""

    @pytest.fixture
    def calculator(self):
        """Provide a fresh Calculator instance."""
        return Calculator()

    def test_cube_root_negative_27_returns_negative_3(self, calculator):
        """Test documented example: calc.cube_root(-8) returns -2.0 (negative support)."""
        result = calculator.cube_root(-8)
        assert result == pytest.approx(-2.0), f"Expected -2.0, got {result}"

    def test_cube_root_negative_27_preserves_sign(self, calculator):
        """Test documented behavior: cube_root preserves sign of x."""
        result = calculator.cube_root(-27)
        assert result == pytest.approx(-3.0), f"Expected -3.0, got {result}"
        assert result < 0, "Expected result to be negative"


class TestCalculatorAddFromAPI:
    """Test Calculator.add with examples from API_REFERENCE."""

    @pytest.fixture
    def calculator(self):
        """Provide a fresh Calculator instance."""
        return Calculator()

    def test_add_3_and_4(self, calculator):
        """Test documented example: calc.add(3, 4) returns 7."""
        result = calculator.add(3, 4)
        assert result == 7, f"Expected 7, got {result}"

    def test_add_1_5_and_2(self, calculator):
        """Test documented example: calc.add(1.5, 2) returns 3.5."""
        result = calculator.add(1.5, 2)
        assert result == 3.5, f"Expected 3.5, got {result}"


# ============================================================================
# LOGGING SETUP IDEMPOTENCY TESTS
# ============================================================================

class TestSetupLoggingIdempotency:
    """Test that setup_logging is idempotent and doesn't duplicate handlers."""

    def test_setup_logging_idempotent_no_duplicate_handlers(self):
        """Test that calling setup_logging twice doesn't add duplicate handlers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")

            # Call setup_logging twice
            logger1 = setup_logging(log_file)
            initial_handler_count = len(logger1.handlers)

            logger2 = setup_logging(log_file)
            second_handler_count = len(logger2.handlers)

            assert initial_handler_count == second_handler_count, (
                f"Expected {initial_handler_count} handlers after second call, "
                f"got {second_handler_count}. Duplicate handler was added."
            )

    def test_setup_logging_returns_logger(self):
        """Test that setup_logging returns a Logger instance."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            logger = setup_logging(log_file)
            assert isinstance(logger, logging.Logger), "setup_logging should return a Logger"

    def test_setup_logging_logger_name_is_calculator(self):
        """Test that setup_logging configures the 'calculator' logger."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "test.log")
            logger = setup_logging(log_file)
            assert logger.name == "calculator", f"Expected logger name 'calculator', got {logger.name}"


# ============================================================================
# EDGE CASE TESTS FOR DOCUMENTED BEHAVIORS
# ============================================================================

class TestEdgeCasesFromDocumentation:
    """Test edge cases and error conditions mentioned in the documentation."""

    @pytest.fixture
    def calculator(self):
        """Provide a fresh Calculator instance."""
        return Calculator()

    def test_divide_by_zero_raises_zerodivisionerror(self, calculator):
        """Test that divide by zero raises ZeroDivisionError as documented."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)

    def test_square_root_negative_raises_valueerror(self, calculator):
        """Test that square_root of negative raises ValueError as documented."""
        with pytest.raises(ValueError):
            calculator.square_root(-1)

    def test_log10_non_positive_raises_valueerror(self, calculator):
        """Test that log10 of non-positive value raises ValueError as documented."""
        with pytest.raises(ValueError):
            calculator.log10(0)
        with pytest.raises(ValueError):
            calculator.log10(-5)

    def test_natural_log_non_positive_raises_valueerror(self, calculator):
        """Test that natural_log of non-positive value raises ValueError as documented."""
        with pytest.raises(ValueError):
            calculator.natural_log(0)
        with pytest.raises(ValueError):
            calculator.natural_log(-1)

    def test_square_bool_raises_typeerror(self, calculator):
        """Test that bool operands are rejected as documented."""
        with pytest.raises(TypeError):
            calculator.square(True)
        with pytest.raises(TypeError):
            calculator.square(False)

    def test_cube_bool_raises_typeerror(self, calculator):
        """Test that bool operands are rejected as documented."""
        with pytest.raises(TypeError):
            calculator.cube(True)

    def test_power_bool_raises_typeerror(self, calculator):
        """Test that bool operands are rejected in power as documented."""
        with pytest.raises(TypeError):
            calculator.power(True, 2)
        with pytest.raises(TypeError):
            calculator.power(2, True)


# ============================================================================
# INTEGRATION TESTS - DOCUMENTATION CONSISTENCY
# ============================================================================

class TestDocumentationConsistency:
    """Test that documentation examples and descriptions are consistent with actual behavior."""

    def test_documented_operations_count_is_12(self):
        """Test that the documented 12 operations are actually available."""
        calc = Calculator()
        operations = [
            "add", "subtract", "multiply", "divide",
            "factorial", "square", "cube",
            "square_root", "cube_root", "power",
            "log10", "natural_log"
        ]
        for op in operations:
            assert hasattr(calc, op), f"Documented operation {op} not found on Calculator"

    def test_cli_supported_operators_match_documentation(self):
        """Test that all documented operators (+, -, *, /, **) work in CLI."""
        calc = Calculator()

        # Test + operator
        result = parse_and_evaluate("5 + 3", calc)
        assert result == 8

        # Test - operator
        result = parse_and_evaluate("5 - 3", calc)
        assert result == 2

        # Test * operator
        result = parse_and_evaluate("5 * 3", calc)
        assert result == 15

        # Test / operator
        result = parse_and_evaluate("6 / 2", calc)
        assert result == 3.0

        # Test ** operator
        result = parse_and_evaluate("2 ** 3", calc)
        assert result == 8.0

    def test_cli_unary_minus_supported_as_documented(self):
        """Test that unary minus is supported as documented."""
        calc = Calculator()
        result = parse_and_evaluate("-5 + 2", calc)
        assert result == -3

    def test_cli_parentheses_supported_as_documented(self):
        """Test that parentheses are supported as documented."""
        calc = Calculator()
        result = parse_and_evaluate("(5 + 3) * 2", calc)
        assert result == 16


# ============================================================================
# BACKWARD COMPATIBILITY SHIM TESTS
# ============================================================================

class TestBackwardCompatibilityShims:
    """Test that backward-compatibility shims (as mentioned in ARCHITECTURE.md) work."""

    def test_can_import_calculator_from_src(self):
        """Test that Calculator can be imported from src as documented in ARCHITECTURE.md."""
        from src.calculator import Calculator as ShimCalculator
        calc = ShimCalculator()
        assert isinstance(calc, Calculator), "Backward-compatibility shim failed"

    def test_can_import_parse_and_evaluate_from_cli(self):
        """Test that parse_and_evaluate can be imported from src.cli."""
        from src.cli import parse_and_evaluate as shim_parse_and_evaluate
        calc = Calculator()
        result = shim_parse_and_evaluate("2 + 3", calc)
        assert result == 5, "CLI shim failed"
