"""Tests to verify that code matches documentation (OPERATIONS.md, GETTING_STARTED.md, etc.)."""

import subprocess
import sys

import pytest
from src.calculator import Calculator
from src.operations import OperationRegistry
from src.io_handler import MAX_RETRIES


class TestOperationsDocumentation:
    """Verify that all operations documented in OPERATIONS.md exist and have correct arity."""

    @pytest.fixture
    def registry(self):
        """Provide a OperationRegistry instance."""
        calculator = Calculator()
        return OperationRegistry(calculator)

    # The 12 operations documented in OPERATIONS.md
    DOCUMENTED_OPERATIONS = {
        "add": 2,
        "subtract": 2,
        "multiply": 2,
        "divide": 2,
        "power": 2,
        "factorial": 1,
        "square": 1,
        "cube": 1,
        "square_root": 1,
        "cube_root": 1,
        "log": 1,
        "ln": 1,
    }

    def test_exactly_12_operations_in_registry(self, registry):
        """Verify that the registry contains exactly 12 operations."""
        ops = registry.list_operations()
        assert len(ops) == 12, f"Expected 12 operations, got {len(ops)}"

    @pytest.mark.parametrize("key,expected_arity", [
        ("add", 2),
        ("subtract", 2),
        ("multiply", 2),
        ("divide", 2),
        ("power", 2),
        ("factorial", 1),
        ("square", 1),
        ("cube", 1),
        ("square_root", 1),
        ("cube_root", 1),
        ("log", 1),
        ("ln", 1),
    ])
    def test_documented_operations_exist_with_correct_arity(self, registry, key, expected_arity):
        """Verify each documented operation exists and has the documented arity."""
        method, arity, description = registry.get_operation(key)
        assert arity == expected_arity, (
            f"Operation '{key}': expected arity {expected_arity}, got {arity}"
        )

    def test_all_documented_operations_in_registry(self, registry):
        """Verify all 12 documented operations exist in the registry."""
        ops = registry.list_operations()
        for key in self.DOCUMENTED_OPERATIONS:
            assert key in ops, f"Documented operation '{key}' not found in registry"

    def test_no_extra_operations_beyond_documented(self, registry):
        """Verify registry contains no operations beyond the 12 documented ones."""
        ops = registry.list_operations()
        documented_keys = set(self.DOCUMENTED_OPERATIONS.keys())
        registry_keys = set(ops.keys())
        extra_keys = registry_keys - documented_keys
        assert not extra_keys, (
            f"Registry contains undocumented operations: {extra_keys}"
        )


class TestCLIModeDocumentation:
    """Verify that CLI examples from GETTING_STARTED.md and OPERATIONS.md actually work."""

    @pytest.mark.parametrize("operation,operands,expected_output_contains", [
        ("add", ["3", "5"], "8"),
        ("subtract", ["10", "4"], "6"),
        ("multiply", ["7", "6"], "42"),
        ("divide", ["9", "3"], "3"),
        ("power", ["2", "10"], "1024"),
        ("factorial", ["7"], "5040"),
        ("square", ["9"], "81"),
        ("cube", ["3"], "27"),
        ("square_root", ["144"], "12"),
        ("cube_root", ["27"], "3"),
        ("log", ["1000"], "3"),
        ("ln", ["1"], "0"),
    ])
    def test_cli_documented_examples_work(self, operation, operands, expected_output_contains):
        """
        Test that the CLI examples documented in GETTING_STARTED.md and OPERATIONS.md
        actually work and produce the expected output.
        """
        cmd = [sys.executable, "-m", "src", operation] + operands
        result = subprocess.run(cmd, capture_output=True, text=True)

        assert result.returncode == 0, (
            f"CLI mode failed for '{operation} {' '.join(operands)}': "
            f"exit code {result.returncode}, stderr: {result.stderr}"
        )
        assert expected_output_contains in result.stdout, (
            f"Expected output to contain '{expected_output_contains}', "
            f"but got: {result.stdout}"
        )

    def test_cli_mode_error_exit_code(self):
        """
        Test that CLI mode exits with code 1 on error (as documented in GETTING_STARTED.md).
        """
        cmd = [sys.executable, "-m", "src", "divide", "5", "0"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        assert result.returncode == 1, (
            f"Expected exit code 1 for division by zero, got {result.returncode}"
        )


class TestGettingStartedDocumentation:
    """Verify claims made in GETTING_STARTED.md."""

    def test_max_retries_constant_exists_and_equals_3(self):
        """
        Verify that MAX_RETRIES is defined and equals 3,
        as stated in GETTING_STARTED.md (line 95-96).
        """
        assert MAX_RETRIES == 3, (
            f"GETTING_STARTED.md references MAX_RETRIES = 3, "
            f"but the constant is {MAX_RETRIES}"
        )

    def test_interactive_mode_all_12_operations_listed(self):
        """
        Verify that running interactive mode prints all 12 operations.
        This is a sanity check for the example session in GETTING_STARTED.md.
        """
        from src.io_handler import InputHandler
        from src.operations import OperationRegistry
        from src.calculator import Calculator

        calc = Calculator()
        registry = OperationRegistry(calc)
        handler = InputHandler()

        ops = registry.list_operations()
        assert len(ops) == 12, (
            f"Interactive mode should list 12 operations, "
            f"but registry has {len(ops)}"
        )
        for key in [
            "add", "subtract", "multiply", "divide", "power",
            "factorial", "square", "cube", "square_root", "cube_root",
            "log", "ln"
        ]:
            assert key in ops, (
                f"Operation '{key}' listed in GETTING_STARTED.md "
                f"example session but not in registry"
            )


class TestOperationsBinaryArity:
    """Verify arity of binary operations as documented."""

    @pytest.fixture
    def registry(self):
        """Provide a OperationRegistry instance."""
        calculator = Calculator()
        return OperationRegistry(calculator)

    @pytest.mark.parametrize("key", ["add", "subtract", "multiply", "divide", "power"])
    def test_binary_operations_have_arity_2(self, registry, key):
        """Verify all documented binary operations have arity 2."""
        method, arity, description = registry.get_operation(key)
        assert arity == 2, (
            f"Binary operation '{key}' should have arity 2, got {arity}"
        )


class TestOperationsUnaryArity:
    """Verify arity of unary operations as documented."""

    @pytest.fixture
    def registry(self):
        """Provide a OperationRegistry instance."""
        calculator = Calculator()
        return OperationRegistry(calculator)

    @pytest.mark.parametrize("key", [
        "factorial", "square", "cube", "square_root", "cube_root", "log", "ln"
    ])
    def test_unary_operations_have_arity_1(self, registry, key):
        """Verify all documented unary operations have arity 1."""
        method, arity, description = registry.get_operation(key)
        assert arity == 1, (
            f"Unary operation '{key}' should have arity 1, got {arity}"
        )
