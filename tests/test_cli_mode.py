"""Tests for mode handling in CLIHandler.

Tests cover:
- CLI default mode initialization
- CLI mode synchronization with context
- CLI operation filtering by mode
- Trigonometric operation handling in CLI
- Mode-aware operation resolution in CLI
"""

import pytest
from src.interface.cli import CLIHandler
from src.calculator import Calculator
from src.context import CalculatorContext


@pytest.fixture
def calc():
    """Provide a Calculator instance."""
    return Calculator()


@pytest.fixture
def context():
    """Provide a fresh CalculatorContext."""
    return CalculatorContext()


@pytest.fixture
def cli(calc, context):
    """Provide a CLIHandler instance with a context."""
    return CLIHandler(calc, context=context)


@pytest.fixture
def cli_without_context(calc):
    """Provide a CLIHandler instance without explicit context."""
    return CLIHandler(calc)


class TestCLIModeInitialization:
    """Test mode initialization in CLIHandler."""

    def test_cli_with_context_starts_in_normal(self, calc):
        """Verify CLI with context starts in normal mode."""
        context = CalculatorContext()
        cli = CLIHandler(calc, context=context)
        assert cli._context.get_mode() == "normal"

    def test_cli_without_context_creates_fresh_context(self, cli_without_context):
        """Verify CLI creates fresh context when none provided."""
        assert cli_without_context._context is not None
        assert cli_without_context._context.get_mode() == "normal"

    def test_cli_context_synced_to_registry(self, calc, context):
        """Verify CLI syncs context mode to registry on initialization."""
        context.set_mode("scientific")
        cli = CLIHandler(calc, context=context)
        assert cli._registry._current_mode == "scientific"

    def test_cli_registry_mode_normal_default(self, cli):
        """Verify CLI registry starts in normal mode by default."""
        assert cli._registry._current_mode == "normal"


class TestCLIOperationMapping:
    """Test operation mapping respects mode in CLI."""

    def test_operation_mapping_normal_excludes_trig(self, cli):
        """Verify get_operation_mapping in normal mode excludes trig."""
        cli._context.set_mode("normal")
        cli._registry.set_mode("normal")
        mapping = cli.get_operation_mapping()
        assert "sin" not in mapping
        assert "cos" not in mapping
        assert "tan" not in mapping

    def test_operation_mapping_scientific_includes_trig(self, cli):
        """Verify get_operation_mapping in scientific mode includes trig."""
        cli._context.set_mode("scientific")
        cli._registry.set_mode("scientific")
        mapping = cli.get_operation_mapping()
        assert "sin" in mapping
        assert "cos" in mapping
        assert "tan" in mapping

    def test_operation_mapping_normal_includes_basic(self, cli):
        """Verify get_operation_mapping includes basic operations."""
        mapping = cli.get_operation_mapping()
        assert "add" in mapping
        assert "subtract" in mapping
        assert "multiply" in mapping
        assert "divide" in mapping

    def test_operation_mapping_includes_aliases(self, cli):
        """Verify get_operation_mapping includes operation aliases."""
        mapping = cli.get_operation_mapping()
        # Check for common aliases
        assert "+" in mapping
        assert "-" in mapping
        assert "*" in mapping
        assert "/" in mapping


class TestCLIParseArgsWithMode:
    """Test parse_args respects mode filtering."""

    def test_parse_add_in_normal_mode(self, cli):
        """Verify adding two numbers works in normal mode."""
        cli._registry.set_mode("normal")
        operation, operands = cli.parse_args(["add", "3", "4"])
        assert operation == "add"
        assert operands == [3.0, 4.0]

    def test_parse_sin_in_scientific_mode(self, cli):
        """Verify parsing sin in scientific mode."""
        cli._registry.set_mode("scientific")
        operation, operands = cli.parse_args(["sin", "1.57"])
        assert operation == "sin"
        assert operands == [1.57]

    def test_parse_sin_in_normal_mode_fails(self, cli):
        """Verify parsing sin in normal mode raises ValueError."""
        cli._registry.set_mode("normal")
        with pytest.raises(ValueError):
            cli.parse_args(["sin", "1.57"])

    def test_parse_cos_in_normal_mode_fails(self, cli):
        """Verify parsing cos in normal mode raises ValueError."""
        cli._registry.set_mode("normal")
        with pytest.raises(ValueError):
            cli.parse_args(["cos", "0"])

    def test_parse_tan_in_normal_mode_fails(self, cli):
        """Verify parsing tan in normal mode raises ValueError."""
        cli._registry.set_mode("normal")
        with pytest.raises(ValueError):
            cli.parse_args(["tan", "0.785"])

    def test_parse_alias_in_normal_mode(self, cli):
        """Verify parsing operation aliases works in normal mode."""
        cli._registry.set_mode("normal")
        operation, operands = cli.parse_args(["+", "5", "2"])
        assert operation == "add"
        assert operands == [5.0, 2.0]

    def test_parse_sqrt_alias_works(self, cli):
        """Verify sqrt alias resolves correctly."""
        cli._registry.set_mode("normal")
        operation, operands = cli.parse_args(["sqrt", "9"])
        assert operation == "square_root"
        assert operands == [9.0]


class TestCLIModeContextIntegration:
    """Integration tests for mode in CLI."""

    def test_shared_context_affects_operations(self, calc):
        """Verify shared context affects available operations."""
        context = CalculatorContext()
        cli = CLIHandler(calc, context=context)
        # Initially normal mode
        assert cli._registry._current_mode == "normal"
        # Change context
        context.set_mode("scientific")
        # Registry should still be normal (not auto-synced in real usage)
        # But we can manually sync
        cli._registry.set_mode(context.get_mode())
        # Now trig should work
        operation, operands = cli.parse_args(["sin", "0"])
        assert operation == "sin"

    def test_separate_cli_instances_have_separate_contexts(self, calc):
        """Verify separate CLI instances have separate contexts."""
        cli1 = CLIHandler(calc)
        cli2 = CLIHandler(calc)
        # Change mode in cli1
        cli1._context.set_mode("scientific")
        cli1._registry.set_mode("scientific")
        # cli2 should still be in normal
        assert cli1._context.get_mode() == "scientific"
        assert cli2._context.get_mode() == "normal"

    def test_explicit_context_is_used(self, calc):
        """Verify explicitly provided context is used."""
        context = CalculatorContext()
        context.set_mode("scientific")
        cli = CLIHandler(calc, context=context)
        assert cli._context is context
        assert cli._context.get_mode() == "scientific"


class TestCLIOperationResolution:
    """Test operation resolution respects mode."""

    def test_resolve_basic_operation_in_normal(self, cli):
        """Verify basic operations resolve in normal mode."""
        cli._registry.set_mode("normal")
        # All of these should work
        assert cli._registry.resolve("add") == "add"
        assert cli._registry.resolve("multiply") == "multiply"
        assert cli._registry.resolve("power") == "power"

    def test_resolve_sin_in_scientific(self, cli):
        """Verify sin resolves in scientific mode."""
        cli._registry.set_mode("scientific")
        assert cli._registry.resolve("sin") == "sin"

    def test_resolve_sin_in_normal_fails(self, cli):
        """Verify sin fails in normal mode."""
        cli._registry.set_mode("normal")
        with pytest.raises(ValueError):
            cli._registry.resolve("sin")

    def test_resolve_by_alias_in_scientific(self, cli):
        """Verify aliases work in scientific mode."""
        cli._registry.set_mode("scientific")
        assert cli._registry.resolve("sqrt") == "square_root"
        assert cli._registry.resolve("ln") == "natural_logarithm"
        assert cli._registry.resolve("log") == "logarithm"


class TestCLIArityWithMode:
    """Test arity checking respects mode."""

    def test_arity_basic_operation_in_normal(self, cli):
        """Verify arity works for basic operations."""
        cli._registry.set_mode("normal")
        assert cli._registry.arity("add") == 2
        assert cli._registry.arity("factorial") == 1

    def test_arity_sin_in_scientific(self, cli):
        """Verify arity for sin in scientific mode."""
        cli._registry.set_mode("scientific")
        assert cli._registry.arity("sin") == 1

    def test_arity_sin_in_normal_fails(self, cli):
        """Verify arity check fails for sin in normal mode."""
        cli._registry.set_mode("normal")
        with pytest.raises(ValueError):
            cli._registry.arity("sin")


class TestCLIErrorMessages:
    """Test that CLI provides clear error messages about mode."""

    def test_error_message_for_unavailable_operation(self, cli):
        """Verify error raised when trig op unavailable in normal mode."""
        cli._registry.set_mode("normal")
        with pytest.raises(ValueError):
            cli.parse_args(["sin", "0"])

    def test_error_raised_for_unknown_operation(self, cli):
        """Verify error raised for unknown operations."""
        cli._registry.set_mode("normal")
        with pytest.raises(ValueError):
            cli.parse_args(["nonexistent", "0"])


class TestCLIModeIndependentOperations:
    """Verify mode-independent operations work in both modes."""

    def test_basic_arithmetic_in_normal(self, cli):
        """Verify basic arithmetic in normal mode."""
        cli._registry.set_mode("normal")
        operation, operands = cli.parse_args(["add", "2", "3"])
        assert operation == "add"

    def test_basic_arithmetic_in_scientific(self, cli):
        """Verify basic arithmetic in scientific mode."""
        cli._registry.set_mode("scientific")
        operation, operands = cli.parse_args(["add", "2", "3"])
        assert operation == "add"

    def test_power_in_normal(self, cli):
        """Verify power operation in normal mode."""
        cli._registry.set_mode("normal")
        operation, operands = cli.parse_args(["power", "2", "3"])
        assert operation == "power"

    def test_power_in_scientific(self, cli):
        """Verify power operation in scientific mode."""
        cli._registry.set_mode("scientific")
        operation, operands = cli.parse_args(["power", "2", "3"])
        assert operation == "power"

    def test_logarithm_in_normal(self, cli):
        """Verify logarithm in normal mode."""
        cli._registry.set_mode("normal")
        operation, operands = cli.parse_args(["logarithm", "100", "10"])
        assert operation == "logarithm"

    def test_logarithm_in_scientific(self, cli):
        """Verify logarithm in scientific mode."""
        cli._registry.set_mode("scientific")
        operation, operands = cli.parse_args(["logarithm", "100", "10"])
        assert operation == "logarithm"
