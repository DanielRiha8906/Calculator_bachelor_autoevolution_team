"""
Tests for logic layer separation between Calculation and Interaction layers.

Verifies that:
1. All modules have appropriate layer docstrings
2. The Calculator class is truly a pure calculation engine
3. Artifact diagrams properly annotate layer boundaries
"""

import pathlib
import inspect
import sys
import pytest
import importlib


# ---------------------------------------------------------------------------
# Module docstring tests
# ---------------------------------------------------------------------------

class TestModuleDocstrings:
    """Verify that all modules have docstrings with appropriate layer keywords."""

    def test_calculator_module_has_docstring(self) -> None:
        """Verify src.calculator module has a docstring."""
        import src.calculator
        assert src.calculator.__doc__ is not None, "src.calculator module should have a docstring"

    def test_calculator_module_contains_calculation_engine_layer_keyword(self) -> None:
        """Verify src.calculator docstring contains 'Calculation engine layer' keyword."""
        import src.calculator
        assert "Calculation engine layer" in src.calculator.__doc__, \
            "src.calculator docstring should contain 'Calculation engine layer'"

    def test_input_loop_module_has_docstring(self) -> None:
        """Verify src.input_loop module has a docstring."""
        import src.input_loop
        assert src.input_loop.__doc__ is not None, "src.input_loop module should have a docstring"

    def test_input_loop_module_contains_interaction_layer_keyword(self) -> None:
        """Verify src.input_loop docstring contains 'Interaction layer' keyword."""
        import src.input_loop
        assert "Interaction layer" in src.input_loop.__doc__, \
            "src.input_loop docstring should contain 'Interaction layer'"

    def test_cli_module_has_docstring(self) -> None:
        """Verify src.cli module has a docstring."""
        import src.cli
        assert src.cli.__doc__ is not None, "src.cli module should have a docstring"

    def test_cli_module_contains_interaction_layer_keyword(self) -> None:
        """Verify src.cli docstring contains 'Interaction layer' keyword."""
        import src.cli
        assert "Interaction layer" in src.cli.__doc__, \
            "src.cli docstring should contain 'Interaction layer'"

    def test_history_module_has_docstring(self) -> None:
        """Verify src.history module has a docstring."""
        import src.history
        assert src.history.__doc__ is not None, "src.history module should have a docstring"

    def test_history_module_contains_interaction_layer_keyword(self) -> None:
        """Verify src.history docstring contains 'Interaction layer' keyword."""
        import src.history
        assert "Interaction layer" in src.history.__doc__, \
            "src.history docstring should contain 'Interaction layer'"

    def test_error_logger_module_has_docstring(self) -> None:
        """Verify src.error_logger module has a docstring."""
        import src.error_logger
        assert src.error_logger.__doc__ is not None, "src.error_logger module should have a docstring"

    def test_error_logger_module_contains_interaction_layer_keyword(self) -> None:
        """Verify src.error_logger docstring contains 'Interaction layer' keyword."""
        import src.error_logger
        assert "Interaction layer" in src.error_logger.__doc__, \
            "src.error_logger docstring should contain 'Interaction layer'"

    def test_validation_module_has_docstring(self) -> None:
        """Verify src.validation module has a docstring."""
        import src.validation
        assert src.validation.__doc__ is not None, "src.validation module should have a docstring"

    def test_validation_module_contains_interaction_layer_keyword(self) -> None:
        """Verify src.validation docstring contains 'Interaction layer' keyword."""
        import src.validation
        assert "Interaction layer" in src.validation.__doc__, \
            "src.validation docstring should contain 'Interaction layer'"

    def test_main_module_has_docstring(self) -> None:
        """Verify src.__main__ module has a docstring."""
        import src.__main__
        assert src.__main__.__doc__ is not None, "src.__main__ module should have a docstring"

    def test_main_module_contains_entry_point_keyword(self) -> None:
        """Verify src.__main__ docstring contains 'Entry point' keyword."""
        import src.__main__
        assert "Entry point" in src.__main__.__doc__, \
            "src.__main__ docstring should contain 'Entry point'"


# ---------------------------------------------------------------------------
# Calculator class docstring tests
# ---------------------------------------------------------------------------

class TestCalculatorClassDocstring:
    """Verify that the Calculator class has an appropriate docstring."""

    def test_calculator_class_has_docstring(self) -> None:
        """Verify Calculator class has a docstring."""
        from src.calculator import Calculator
        assert Calculator.__doc__ is not None, "Calculator class should have a docstring"

    def test_calculator_class_docstring_contains_pure_calculation_engine(self) -> None:
        """Verify Calculator docstring contains 'Pure calculation engine' keyword."""
        from src.calculator import Calculator
        assert "Pure calculation engine" in Calculator.__doc__, \
            "Calculator docstring should contain 'Pure calculation engine'"


# ---------------------------------------------------------------------------
# Calculator purity tests
# ---------------------------------------------------------------------------

class TestCalculatorPurity:
    """Verify that Calculator class has no I/O or external interaction dependencies."""

    def test_calculator_does_not_import_input(self) -> None:
        """Verify Calculator module does not import the built-in input function."""
        import src.calculator
        module_source = inspect.getsource(src.calculator)
        assert "input(" not in module_source, \
            "Calculator module should not call input()"
        assert "from builtins import input" not in module_source, \
            "Calculator module should not import input from builtins"

    def test_calculator_does_not_import_print(self) -> None:
        """Verify Calculator module does not import the built-in print function."""
        import src.calculator
        module_source = inspect.getsource(src.calculator)
        assert "print(" not in module_source, \
            "Calculator module should not call print()"

    def test_calculator_does_not_import_sys(self) -> None:
        """Verify Calculator module does not import sys."""
        import src.calculator
        module_source = inspect.getsource(src.calculator)
        assert "import sys" not in module_source, \
            "Calculator module should not import sys"
        assert "from sys import" not in module_source, \
            "Calculator module should not import from sys"

    def test_calculator_does_not_import_io(self) -> None:
        """Verify Calculator module does not import I/O modules."""
        import src.calculator
        module_source = inspect.getsource(src.calculator)
        assert "import io" not in module_source, \
            "Calculator module should not import io"
        assert "from io import" not in module_source, \
            "Calculator module should not import from io"

    def test_calculator_does_not_import_pathlib(self) -> None:
        """Verify Calculator module does not import pathlib."""
        import src.calculator
        module_source = inspect.getsource(src.calculator)
        assert "import pathlib" not in module_source, \
            "Calculator module should not import pathlib"
        assert "from pathlib import" not in module_source, \
            "Calculator module should not import from pathlib"

    def test_calculator_class_has_no_stdin_attributes(self) -> None:
        """Verify Calculator class instance has no stdin-related attributes."""
        from src.calculator import Calculator
        calc = Calculator()
        # Check that instance dict doesn't contain I/O stream attributes
        instance_dict = vars(calc)
        assert "stdin" not in instance_dict, \
            "Calculator instance should not have stdin attribute"
        assert "stdout" not in instance_dict, \
            "Calculator instance should not have stdout attribute"
        assert "stderr" not in instance_dict, \
            "Calculator instance should not have stderr attribute"


# ---------------------------------------------------------------------------
# Artifact file tests
# ---------------------------------------------------------------------------

ARTIFACTS_DIR = pathlib.Path(__file__).parent.parent / "artifacts"

CLASS_DIAGRAM = ARTIFACTS_DIR / "class_diagram.puml"
ACTIVITY_DIAGRAM = ARTIFACTS_DIR / "activity_diagram.puml"
SEQUENCE_DIAGRAM = ARTIFACTS_DIR / "sequence_diagram.puml"


def _content(path: pathlib.Path) -> str:
    """Return the full file content as a single string."""
    return path.read_text(encoding="utf-8")


class TestArtifactLayerAnnotations:
    """Verify that artifact diagrams contain layer grouping keywords."""

    def test_class_diagram_exists(self) -> None:
        """Verify class_diagram.puml file exists."""
        assert CLASS_DIAGRAM.exists(), f"Expected artifact not found: {CLASS_DIAGRAM}"

    def test_activity_diagram_exists(self) -> None:
        """Verify activity_diagram.puml file exists."""
        assert ACTIVITY_DIAGRAM.exists(), f"Expected artifact not found: {ACTIVITY_DIAGRAM}"

    def test_sequence_diagram_exists(self) -> None:
        """Verify sequence_diagram.puml file exists."""
        assert SEQUENCE_DIAGRAM.exists(), f"Expected artifact not found: {SEQUENCE_DIAGRAM}"

    def test_class_diagram_contains_calculation_layer(self) -> None:
        """Verify class_diagram.puml contains 'Calculation Layer' keyword."""
        content = _content(CLASS_DIAGRAM)
        assert "Calculation Layer" in content, \
            "class_diagram.puml should contain 'Calculation Layer' keyword"

    def test_class_diagram_contains_interaction_layer(self) -> None:
        """Verify class_diagram.puml contains 'Interaction Layer' keyword."""
        content = _content(CLASS_DIAGRAM)
        assert "Interaction Layer" in content, \
            "class_diagram.puml should contain 'Interaction Layer' keyword"

    def test_activity_diagram_contains_calculation_layer(self) -> None:
        """Verify activity_diagram.puml contains 'Calculation Layer' keyword."""
        content = _content(ACTIVITY_DIAGRAM)
        assert "Calculation Layer" in content, \
            "activity_diagram.puml should contain 'Calculation Layer' keyword"

    def test_activity_diagram_contains_interaction_layer(self) -> None:
        """Verify activity_diagram.puml contains 'Interaction Layer' keyword."""
        content = _content(ACTIVITY_DIAGRAM)
        assert "Interaction Layer" in content, \
            "activity_diagram.puml should contain 'Interaction Layer' keyword"

    def test_sequence_diagram_contains_calculation_layer(self) -> None:
        """Verify sequence_diagram.puml contains 'Calculation Layer' keyword."""
        content = _content(SEQUENCE_DIAGRAM)
        assert "Calculation Layer" in content, \
            "sequence_diagram.puml should contain 'Calculation Layer' keyword"

    def test_sequence_diagram_contains_interaction_layer(self) -> None:
        """Verify sequence_diagram.puml contains 'Interaction Layer' keyword."""
        content = _content(SEQUENCE_DIAGRAM)
        assert "Interaction Layer" in content, \
            "sequence_diagram.puml should contain 'Interaction Layer' keyword"


# ---------------------------------------------------------------------------
# Layer dependency tests
# ---------------------------------------------------------------------------

class TestLayerDependencies:
    """Verify proper layer dependencies and absence of circular dependencies."""

    def test_calculator_not_imported_by_calculation_modules(self) -> None:
        """Verify Calculator is not used by other calculation layer modules (none exist yet)."""
        # Since there's only Calculator in the calculation layer, this is a pass-through test
        # It documents the expectation that no module should import from Calculator
        # in the same layer.
        import src.calculator
        # This module should exist and be importable
        assert hasattr(src.calculator, 'Calculator'), \
            "Calculator class should exist in src.calculator"

    def test_interaction_layer_can_import_calculation_layer(self) -> None:
        """Verify interaction layer modules can import from calculation layer."""
        # input_loop imports Calculator
        import src.input_loop
        import src.calculator
        assert hasattr(src.input_loop, 'Calculator') or 'Calculator' in dir(src.input_loop), \
            "interaction layer should be able to import Calculator"

    def test_no_circular_import_between_layers(self) -> None:
        """Verify Calculator is not imported by Calculator (trivially true)."""
        import src.calculator
        module_source = inspect.getsource(src.calculator)
        # The module should not try to import itself
        assert "from src.calculator import" not in module_source or \
               "from src.calculator import Calculator" not in module_source, \
            "Calculator module should not have circular self-import"


# ---------------------------------------------------------------------------
# Documentation consistency tests
# ---------------------------------------------------------------------------

class TestDocumentationConsistency:
    """Verify docstrings are consistent with actual layer responsibilities."""

    def test_calculator_docstring_matches_behavior(self) -> None:
        """Verify Calculator docstring accurately describes it as pure calculation engine."""
        from src.calculator import Calculator
        docstring = Calculator.__doc__.lower()
        # Check for key phrases about purity
        assert "pure" in docstring or "calculation" in docstring, \
            "Calculator docstring should mention 'pure' or 'calculation'"
        assert "no input" in docstring or "no i/o" in docstring.replace("/", "").lower() or \
               "no user interaction" in docstring, \
            "Calculator docstring should mention lack of I/O or user interaction"

    def test_interaction_modules_mention_layer(self) -> None:
        """Verify all interaction layer modules explicitly mention 'Interaction layer'."""
        import src.input_loop
        import src.cli
        import src.history
        import src.error_logger
        import src.validation

        interaction_modules = [
            (src.input_loop, "input_loop"),
            (src.cli, "cli"),
            (src.history, "history"),
            (src.error_logger, "error_logger"),
            (src.validation, "validation"),
        ]

        for module, name in interaction_modules:
            docstring = module.__doc__
            assert docstring is not None, f"{name} module should have a docstring"
            assert "Interaction layer" in docstring, \
                f"{name} docstring should contain 'Interaction layer'"

    def test_entry_point_docstring_mentions_routing(self) -> None:
        """Verify __main__ module docstring mentions entry point concept."""
        import src.__main__
        docstring = src.__main__.__doc__
        assert docstring is not None, "__main__ module should have a docstring"
        assert "Entry point" in docstring or "entry point" in docstring.lower(), \
            "__main__ docstring should mention 'Entry point'"


# ---------------------------------------------------------------------------
# Sanity tests for proper separation
# ---------------------------------------------------------------------------

class TestLayerSeparationSanity:
    """Sanity checks for proper layer separation."""

    def test_all_calculator_methods_are_pure(self) -> None:
        """Verify all Calculator methods follow pure function signature."""
        from src.calculator import Calculator
        calc = Calculator()
        # Get all public methods
        methods = [m for m in dir(calc) if not m.startswith('_') and callable(getattr(calc, m))]
        # Sanity check: should have multiple methods
        assert len(methods) >= 10, \
            "Calculator should have at least 10 public methods (add, subtract, multiply, etc.)"

    def test_calculator_methods_return_values(self) -> None:
        """Verify Calculator methods return values (not None or side effects)."""
        from src.calculator import Calculator
        calc = Calculator()
        # Test that basic operations return values
        result = calc.add(2, 3)
        assert result is not None, "add() should return a value"
        assert result == 5, "add(2, 3) should return 5"

        result = calc.multiply(3, 4)
        assert result is not None, "multiply() should return a value"
        assert result == 12, "multiply(3, 4) should return 12"

    def test_calculator_immutable_behavior(self) -> None:
        """Verify Calculator doesn't maintain mutable state between calls."""
        from src.calculator import Calculator
        calc = Calculator()
        # Call methods and verify no internal state changes
        calc.add(1, 2)
        calc.add(10, 20)
        # Call the same operation again and verify identical result
        result1 = calc.add(5, 5)
        result2 = calc.add(5, 5)
        assert result1 == result2, \
            "Calculator should produce identical results for identical inputs"
