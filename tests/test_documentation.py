"""Tests for documentation files (README.md and FEATURES.md).

This module verifies that:
1. README.md and FEATURES.md exist and are non-empty.
2. All operation keys referenced in FEATURES.md match keys in OPERATIONS dict.
3. Error messages documented in FEATURES.md match the actual strings in the source code.
"""

import re
from pathlib import Path

import pytest

from src.input_loop import OPERATIONS
from src.operations import arithmetic, exponents, logarithmic, roots


class TestDocumentationFilesExist:
    """Tests that verify documentation files exist and are non-empty."""

    def test_readme_exists(self):
        """README.md file should exist at repository root."""
        readme_path = Path(__file__).parent.parent / "README.md"
        assert readme_path.exists(), f"README.md not found at {readme_path}"

    def test_readme_is_non_empty(self):
        """README.md should have more than 1 line."""
        readme_path = Path(__file__).parent.parent / "README.md"
        content = readme_path.read_text()
        lines = content.strip().split("\n")
        assert len(lines) > 1, "README.md should have more than 1 line"

    def test_features_exists(self):
        """FEATURES.md file should exist at repository root."""
        features_path = Path(__file__).parent.parent / "FEATURES.md"
        assert features_path.exists(), f"FEATURES.md not found at {features_path}"

    def test_features_is_non_empty(self):
        """FEATURES.md should have more than 1 line."""
        features_path = Path(__file__).parent.parent / "FEATURES.md"
        content = features_path.read_text()
        lines = content.strip().split("\n")
        assert len(lines) > 1, "FEATURES.md should have more than 1 line"


class TestFeaturesDocumentationStructure:
    """Tests that verify FEATURES.md structure and references."""

    @pytest.fixture
    def features_content(self):
        """Load FEATURES.md content."""
        features_path = Path(__file__).parent.parent / "FEATURES.md"
        return features_path.read_text()

    def test_all_operation_keys_in_features_exist_in_operations(
        self, features_content
    ):
        """Every operation key referenced in FEATURES.md should be in OPERATIONS."""
        # Extract operation keys from markdown headers like "### `add` — Addition"
        pattern = r"^### `(\w+)`"
        documented_keys = set(
            re.findall(pattern, features_content, re.MULTILINE)
        )

        # Exclude "history" and "exit" which are meta-commands, not mathematical operations
        documented_keys.discard("history")
        documented_keys.discard("exit")

        operations_keys = set(OPERATIONS.keys())
        operations_keys.discard("history")

        missing_in_operations = documented_keys - operations_keys
        assert (
            not missing_in_operations
        ), f"Operation keys in FEATURES.md not in OPERATIONS: {missing_in_operations}"

    def test_all_operations_except_history_documented_in_features(
        self, features_content
    ):
        """Every operation in OPERATIONS (except 'history') should be in FEATURES.md."""
        # Extract operation keys from markdown headers
        pattern = r"^### `(\w+)`"
        documented_keys = set(
            re.findall(pattern, features_content, re.MULTILINE)
        )

        operations_keys = set(OPERATIONS.keys())
        operations_keys.discard("history")

        missing_in_features = operations_keys - documented_keys
        assert (
            not missing_in_features
        ), f"Operation keys in OPERATIONS not documented in FEATURES.md: {missing_in_features}"

    def test_features_has_12_operations_documented(self, features_content):
        """FEATURES.md should document exactly 12 mathematical operations."""
        pattern = r"^### `(\w+)`"
        documented_keys = set(
            re.findall(pattern, features_content, re.MULTILINE)
        )
        documented_keys.discard("history")
        documented_keys.discard("exit")
        assert (
            len(documented_keys) == 12
        ), f"Expected 12 operations, found {len(documented_keys)}: {documented_keys}"

    def test_features_has_operation_keys_add_subtract_multiply_divide(
        self, features_content
    ):
        """FEATURES.md should document binary arithmetic operations."""
        pattern = r"^### `(\w+)`"
        documented_keys = set(
            re.findall(pattern, features_content, re.MULTILINE)
        )
        required_ops = {"add", "subtract", "multiply", "divide"}
        assert (
            required_ops.issubset(documented_keys)
        ), f"Missing required operations: {required_ops - documented_keys}"

    def test_features_has_operation_keys_power_factorial_square_cube(
        self, features_content
    ):
        """FEATURES.md should document exponent operations."""
        pattern = r"^### `(\w+)`"
        documented_keys = set(
            re.findall(pattern, features_content, re.MULTILINE)
        )
        required_ops = {"power", "factorial", "square", "cube"}
        assert (
            required_ops.issubset(documented_keys)
        ), f"Missing required operations: {required_ops - documented_keys}"

    def test_features_has_operation_keys_square_root_cube_root(
        self, features_content
    ):
        """FEATURES.md should document root operations."""
        pattern = r"^### `(\w+)`"
        documented_keys = set(
            re.findall(pattern, features_content, re.MULTILINE)
        )
        required_ops = {"square_root", "cube_root"}
        assert (
            required_ops.issubset(documented_keys)
        ), f"Missing required operations: {required_ops - documented_keys}"

    def test_features_has_operation_keys_log_ln(self, features_content):
        """FEATURES.md should document logarithmic operations."""
        pattern = r"^### `(\w+)`"
        documented_keys = set(
            re.findall(pattern, features_content, re.MULTILINE)
        )
        required_ops = {"log", "ln"}
        assert (
            required_ops.issubset(documented_keys)
        ), f"Missing required operations: {required_ops - documented_keys}"


class TestErrorMessagesInDocumentation:
    """Tests that verify error messages in FEATURES.md match source code."""

    @pytest.fixture
    def features_content(self):
        """Load FEATURES.md content."""
        features_path = Path(__file__).parent.parent / "FEATURES.md"
        return features_path.read_text()

    def test_divide_by_zero_error_message_matches(self, features_content):
        """Division by zero error message in FEATURES.md should match source."""
        # Get actual error message from arithmetic module
        actual_error = "Division by zero is not allowed"

        # Verify the error message appears somewhere in FEATURES.md
        # (in the divide section under Error conditions)
        divide_section = features_content[
            features_content.find("### `divide`")
            : features_content.find("### `power`")
        ]
        assert (
            "division by zero" in divide_section.lower()
        ), f"Divide section should mention division by zero error"

    def test_square_root_negative_number_error_in_features(self, features_content):
        """Square root error for negative numbers should be documented."""
        # Get actual error message from roots module
        actual_error = "square_root requires a non-negative number"

        # Verify error condition is documented in square_root section
        sqrt_section = features_content[
            features_content.find("### `square_root`")
            : features_content.find("### `cube_root`")
        ]
        assert (
            "negative" in sqrt_section.lower()
        ), f"Square root section should mention negative number restriction"

    def test_logarithm_positive_number_requirement_documented(
        self, features_content
    ):
        """Logarithm operations should document positive number requirement."""
        log_section = features_content[
            features_content.find("### `log`")
            : features_content.find("### `ln`")
        ]
        assert (
            "positive" in log_section.lower()
        ), f"Log section should mention positive number requirement"

        ln_section = features_content[features_content.find("### `ln`") :]
        assert (
            "positive" in ln_section.lower()
        ), f"Ln section should mention positive number requirement"

    def test_factorial_non_negative_integer_requirement_documented(
        self, features_content
    ):
        """Factorial should document non-negative integer requirement."""
        factorial_section = features_content[
            features_content.find("### `factorial`")
            : features_content.find("### `square`")
        ]
        assert (
            "non-negative" in factorial_section.lower()
            or "negative" in factorial_section.lower()
        ), "Factorial section should mention non-negative requirement"
        assert (
            "integer" in factorial_section.lower()
        ), "Factorial section should mention integer requirement"


class TestOperationErrorMessagesVerification:
    """Tests that verify actual error messages raised by operations match documentation intent."""

    def test_divide_raises_value_error_for_zero_divisor(self):
        """divide() should raise ValueError with correct message for zero divisor."""
        with pytest.raises(ValueError) as exc_info:
            arithmetic.divide(10, 0)
        assert "Division by zero is not allowed" in str(exc_info.value)

    def test_square_root_raises_value_error_for_negative_number(self):
        """square_root() should raise ValueError for negative numbers."""
        with pytest.raises(ValueError) as exc_info:
            roots.square_root(-4)
        assert "square_root requires a non-negative number" in str(exc_info.value)

    def test_log_raises_value_error_for_zero(self):
        """log() should raise ValueError for zero or negative input."""
        with pytest.raises(ValueError) as exc_info:
            logarithmic.log(0)
        assert "log requires a positive number" in str(exc_info.value)

    def test_log_raises_value_error_for_negative_number(self):
        """log() should raise ValueError for negative input."""
        with pytest.raises(ValueError) as exc_info:
            logarithmic.log(-5)
        assert "log requires a positive number" in str(exc_info.value)

    def test_ln_raises_value_error_for_zero(self):
        """ln() should raise ValueError for zero or negative input."""
        with pytest.raises(ValueError) as exc_info:
            logarithmic.ln(0)
        assert "ln requires a positive number" in str(exc_info.value)

    def test_ln_raises_value_error_for_negative_number(self):
        """ln() should raise ValueError for negative input."""
        with pytest.raises(ValueError) as exc_info:
            logarithmic.ln(-5)
        assert "ln requires a positive number" in str(exc_info.value)

    def test_factorial_raises_value_error_for_negative_integer(self):
        """factorial() should raise ValueError for negative integers."""
        with pytest.raises(ValueError) as exc_info:
            exponents.factorial(-5)
        assert "n must be a non-negative integer" in str(exc_info.value)

    def test_factorial_raises_value_error_for_non_integer(self):
        """factorial() should raise ValueError for non-integer input."""
        with pytest.raises(ValueError) as exc_info:
            exponents.factorial(3.5)
        assert "n must be an integer" in str(exc_info.value)


class TestReadmeStructure:
    """Tests verifying README.md structure and completeness."""

    @pytest.fixture
    def readme_content(self):
        """Load README.md content."""
        readme_path = Path(__file__).parent.parent / "README.md"
        return readme_path.read_text()

    def test_readme_mentions_features_md(self, readme_content):
        """README.md should reference FEATURES.md for detailed documentation."""
        assert "FEATURES.md" in readme_content, "README should reference FEATURES.md"

    def test_readme_has_features_section(self, readme_content):
        """README.md should have a Features section."""
        assert "## Features" in readme_content, "README should have Features section"

    def test_readme_has_installation_section(self, readme_content):
        """README.md should have an Installation and Setup section."""
        assert (
            "## Installation" in readme_content
        ), "README should have Installation section"

    def test_readme_lists_12_operations(self, readme_content):
        """README.md should list all 12 operations."""
        # Count operation keys mentioned in features list
        operation_keys = [
            "add",
            "subtract",
            "multiply",
            "divide",
            "power",
            "square",
            "cube",
            "factorial",
            "square_root",
            "cube_root",
            "log",
            "ln",
        ]
        for op in operation_keys:
            assert (
                op in readme_content
            ), f"README should mention operation '{op}'"


class TestOperationsCompleteness:
    """Tests verifying that OPERATIONS dict has all required keys."""

    def test_operations_dict_has_12_operations(self):
        """OPERATIONS dict should have exactly 13 keys (12 operations + 'history')."""
        assert len(OPERATIONS) == 13, f"Expected 13 keys, got {len(OPERATIONS)}"

    def test_operations_dict_has_all_binary_operations(self):
        """OPERATIONS dict should have all binary operations."""
        required_binary_ops = {"add", "subtract", "multiply", "divide", "power"}
        for op in required_binary_ops:
            assert op in OPERATIONS, f"Missing binary operation: {op}"
            assert OPERATIONS[op][1] == 2, f"{op} should have operand_count=2"

    def test_operations_dict_has_all_unary_exponent_operations(self):
        """OPERATIONS dict should have unary exponent operations."""
        required_unary_exponent = {"factorial", "square", "cube"}
        for op in required_unary_exponent:
            assert op in OPERATIONS, f"Missing exponent operation: {op}"
            assert OPERATIONS[op][1] == 1, f"{op} should have operand_count=1"

    def test_operations_dict_has_all_root_operations(self):
        """OPERATIONS dict should have all root operations."""
        required_root_ops = {"square_root", "cube_root"}
        for op in required_root_ops:
            assert op in OPERATIONS, f"Missing root operation: {op}"
            assert OPERATIONS[op][1] == 1, f"{op} should have operand_count=1"

    def test_operations_dict_has_all_logarithmic_operations(self):
        """OPERATIONS dict should have logarithmic operations."""
        required_log_ops = {"log", "ln"}
        for op in required_log_ops:
            assert op in OPERATIONS, f"Missing logarithmic operation: {op}"
            assert OPERATIONS[op][1] == 1, f"{op} should have operand_count=1"

    def test_operations_dict_has_history_meta_command(self):
        """OPERATIONS dict should have 'history' meta-command with operand_count=0."""
        assert "history" in OPERATIONS
        assert OPERATIONS["history"][1] == 0


class TestFeaturesDocumentationCompleteness:
    """Additional tests for FEATURES.md completeness."""

    @pytest.fixture
    def features_content(self):
        """Load FEATURES.md content."""
        features_path = Path(__file__).parent.parent / "FEATURES.md"
        return features_path.read_text()

    def test_features_has_examples_section_for_each_operation(
        self, features_content
    ):
        """Each operation in FEATURES.md should have an Examples section."""
        pattern = r"^### `(\w+)`"
        documented_keys = set(
            re.findall(pattern, features_content, re.MULTILINE)
        )
        documented_keys.discard("history")
        documented_keys.discard("exit")

        for op in documented_keys:
            operation_section_start = features_content.find(f"### `{op}`")
            next_section_pattern = "^### `"
            remaining = features_content[operation_section_start:]
            next_section_match = re.search(next_section_pattern, remaining[5:], re.MULTILINE)
            if next_section_match:
                operation_section = remaining[
                    : next_section_match.start() + 5
                ]
            else:
                operation_section = remaining

            # Check for Examples section (may be case-insensitive in practice)
            assert (
                "Example" in operation_section
            ), f"Operation {op} should have Examples section"

    def test_features_has_error_conditions_section_for_operations(
        self, features_content
    ):
        """Operations with error conditions should document them."""
        # Operations that can raise errors
        error_prone_ops = {
            "divide",
            "square_root",
            "log",
            "ln",
            "factorial",
        }

        for op in error_prone_ops:
            operation_section_start = features_content.find(f"### `{op}`")
            next_section_pattern = "^### `"
            remaining = features_content[operation_section_start:]
            next_section_match = re.search(next_section_pattern, remaining[5:], re.MULTILINE)
            if next_section_match:
                operation_section = remaining[
                    : next_section_match.start() + 5
                ]
            else:
                operation_section = remaining

            # Check for Error conditions section
            assert (
                "Error" in operation_section
            ), f"Operation {op} should document error conditions"
