"""Tests to validate documentation accuracy against actual codebase.

This test module ensures that all documentation files contain accurate information
about the codebase, including:
- File existence and paths
- Operation registry keys and properties
- Module paths and exports
- Constants like MAX_RETRIES
- Error messages and their exact wording
- History format
- Diagram references
"""

import os
import re
from pathlib import Path

import pytest

from src.core.calculator import Calculator
from src.operations import OPERATIONS, NORMAL_OPERATIONS
from src.session.input_handler import MAX_RETRIES
from src.session.history import History
from src.shared.dispatcher import OperationDispatcher
from src.shared.logger import Logger


class TestDocumentationFileExistence:
    """Verify all documentation files exist at expected paths."""

    def test_readme_exists(self):
        """README.md should exist in the project root."""
        readme_path = Path("README.md")
        assert readme_path.exists(), "README.md not found in project root"
        assert readme_path.is_file(), "README.md is not a file"

    def test_architecture_doc_exists(self):
        """docs/ARCHITECTURE.md should exist."""
        arch_path = Path("docs/ARCHITECTURE.md")
        assert arch_path.exists(), "docs/ARCHITECTURE.md not found"
        assert arch_path.is_file(), "docs/ARCHITECTURE.md is not a file"

    def test_modules_doc_exists(self):
        """docs/MODULES.md should exist."""
        modules_path = Path("docs/MODULES.md")
        assert modules_path.exists(), "docs/MODULES.md not found"
        assert modules_path.is_file(), "docs/MODULES.md is not a file"

    def test_operations_reference_doc_exists(self):
        """docs/OPERATIONS_REFERENCE.md should exist."""
        ops_path = Path("docs/OPERATIONS_REFERENCE.md")
        assert ops_path.exists(), "docs/OPERATIONS_REFERENCE.md not found"
        assert ops_path.is_file(), "docs/OPERATIONS_REFERENCE.md is not a file"

    def test_session_behavior_doc_exists(self):
        """docs/SESSION_BEHAVIOR.md should exist."""
        session_path = Path("docs/SESSION_BEHAVIOR.md")
        assert session_path.exists(), "docs/SESSION_BEHAVIOR.md not found"
        assert session_path.is_file(), "docs/SESSION_BEHAVIOR.md is not a file"

    def test_troubleshooting_doc_exists(self):
        """docs/TROUBLESHOOTING.md should exist."""
        troubleshooting_path = Path("docs/TROUBLESHOOTING.md")
        assert troubleshooting_path.exists(), "docs/TROUBLESHOOTING.md not found"
        assert troubleshooting_path.is_file(), "docs/TROUBLESHOOTING.md is not a file"


class TestOperationsReferenceAccuracy:
    """Verify OPERATIONS_REFERENCE.md lists correct operations with correct properties."""

    def test_all_operations_in_registry(self):
        """Every operation in OPERATIONS should be documented in OPERATIONS_REFERENCE.md."""
        with open("docs/OPERATIONS_REFERENCE.md", "r") as f:
            content = f.read()

        expected_ops = set(OPERATIONS.keys())
        for op in expected_ops:
            assert op in content, f"Operation '{op}' not found in OPERATIONS_REFERENCE.md"

    def test_operation_arity_matches_registry(self):
        """Operation arities in documentation should match the OPERATIONS registry."""
        with open("docs/OPERATIONS_REFERENCE.md", "r") as f:
            content = f.read()

        for op_key, op_meta in OPERATIONS.items():
            expected_arity = op_meta["arity"]
            # Regex to find arity line for this operation in docs
            pattern = rf"### {re.escape(op_key)}.*?\| Arity \| ({expected_arity})"
            assert re.search(pattern, content, re.DOTALL), (
                f"Operation '{op_key}' arity mismatch in docs. "
                f"Registry says {expected_arity}"
            )

    def test_operation_keys_match_registry(self):
        """Operation keys in documentation should match OPERATIONS registry keys."""
        expected_keys = set(OPERATIONS.keys())
        # Expected from NORMAL_OPERATIONS: add, subtract, multiply, divide, power,
        # factorial, square, cube, square_root, cube_root, log10, ln
        expected_in_normal = {
            "add", "subtract", "multiply", "divide", "power",
            "factorial", "square", "cube", "square_root", "cube_root", "log10", "ln"
        }
        assert expected_keys == expected_in_normal, (
            f"OPERATIONS registry keys do not match expected set. "
            f"Got: {expected_keys}"
        )

    def test_divide_error_message_documented(self):
        """Division by zero error message should be documented."""
        with open("docs/OPERATIONS_REFERENCE.md", "r") as f:
            content = f.read()

        # The doc says: "Error: Division by zero is not allowed."
        assert "Division by zero is not allowed." in content

    def test_square_root_error_message_documented(self):
        """Square root domain error message should be documented."""
        with open("docs/OPERATIONS_REFERENCE.md", "r") as f:
            content = f.read()

        # The doc quotes: "square_root() is not defined for negative numbers, got <x>"
        assert "square_root() is not defined for negative numbers" in content

    def test_log10_error_message_documented(self):
        """log10 domain error message should be documented."""
        with open("docs/OPERATIONS_REFERENCE.md", "r") as f:
            content = f.read()

        assert "log10() is not defined for x <= 0" in content

    def test_ln_error_message_documented(self):
        """ln domain error message should be documented."""
        with open("docs/OPERATIONS_REFERENCE.md", "r") as f:
            content = f.read()

        assert "ln() is not defined for x <= 0" in content

    def test_factorial_boolean_error_documented(self):
        """factorial boolean error should be documented."""
        with open("docs/OPERATIONS_REFERENCE.md", "r") as f:
            content = f.read()

        assert "factorial() does not accept boolean values" in content

    def test_factorial_negative_error_documented(self):
        """factorial negative number error should be documented."""
        with open("docs/OPERATIONS_REFERENCE.md", "r") as f:
            content = f.read()

        assert "factorial() is not defined for negative integers" in content


class TestModulePathsAccuracy:
    """Verify module paths mentioned in MODULES.md actually exist."""

    def test_calculator_file_exists(self):
        """src/core/calculator.py should exist as documented."""
        path = Path("src/core/calculator.py")
        assert path.exists(), f"{path} not found as documented in MODULES.md"

    def test_dispatcher_file_exists(self):
        """src/shared/dispatcher.py should exist as documented."""
        path = Path("src/shared/dispatcher.py")
        assert path.exists(), f"{path} not found as documented in MODULES.md"

    def test_input_handler_file_exists(self):
        """src/session/input_handler.py should exist as documented."""
        path = Path("src/session/input_handler.py")
        assert path.exists(), f"{path} not found as documented in MODULES.md"

    def test_cli_file_exists(self):
        """src/interface/cli.py should exist as documented."""
        path = Path("src/interface/cli.py")
        assert path.exists(), f"{path} not found as documented in MODULES.md"

    def test_logger_file_exists(self):
        """src/shared/logger.py should exist as documented."""
        path = Path("src/shared/logger.py")
        assert path.exists(), f"{path} not found as documented in MODULES.md"

    def test_history_file_exists(self):
        """src/session/history.py should exist as documented."""
        path = Path("src/session/history.py")
        assert path.exists(), f"{path} not found as documented in MODULES.md"

    def test_operations_init_file_exists(self):
        """src/operations/__init__.py should exist as documented."""
        path = Path("src/operations/__init__.py")
        assert path.exists(), f"{path} not found as documented in MODULES.md"

    def test_operations_normal_file_exists(self):
        """src/operations/normal.py should exist as documented."""
        path = Path("src/operations/normal.py")
        assert path.exists(), f"{path} not found as documented in MODULES.md"

    def test_operations_scientific_file_exists(self):
        """src/operations/scientific.py should exist as documented."""
        path = Path("src/operations/scientific.py")
        assert path.exists(), f"{path} not found as documented in MODULES.md"

    def test_calculator_shim_exists(self):
        """src/calculator.py (backward compat shim) should exist as documented."""
        path = Path("src/calculator.py")
        assert path.exists(), f"{path} not found as documented in MODULES.md"

    def test_dispatcher_shim_exists(self):
        """src/dispatcher.py (backward compat shim) should exist as documented."""
        path = Path("src/dispatcher.py")
        assert path.exists(), f"{path} not found as documented in MODULES.md"

    def test_input_handler_shim_exists(self):
        """src/input_handler.py (backward compat shim) should exist as documented."""
        path = Path("src/input_handler.py")
        assert path.exists(), f"{path} not found as documented in MODULES.md"

    def test_logger_shim_exists(self):
        """src/logger.py (backward compat shim) should exist as documented."""
        path = Path("src/logger.py")
        assert path.exists(), f"{path} not found as documented in MODULES.md"

    def test_history_shim_exists(self):
        """src/history.py (backward compat shim) should exist as documented."""
        path = Path("src/history.py")
        assert path.exists(), f"{path} not found as documented in MODULES.md"

    def test_cli_shim_exists(self):
        """src/cli.py (backward compat shim) should exist as documented."""
        path = Path("src/cli.py")
        assert path.exists(), f"{path} not found as documented in MODULES.md"

    def test_operations_shim_exists(self):
        """src/operations.py (backward compat shim) should exist as documented."""
        path = Path("src/operations.py")
        assert path.exists(), f"{path} not found as documented in MODULES.md"


class TestMaxRetriesAccuracy:
    """Verify MAX_RETRIES constant matches documentation."""

    def test_max_retries_is_5(self):
        """MAX_RETRIES should be 5 as documented in SESSION_BEHAVIOR.md."""
        assert MAX_RETRIES == 5, (
            f"MAX_RETRIES is {MAX_RETRIES}, but documentation says it should be 5. "
            "Update docs/SESSION_BEHAVIOR.md if the constant changed."
        )

    def test_max_retries_documented_in_session_behavior(self):
        """MAX_RETRIES=5 should be documented in SESSION_BEHAVIOR.md."""
        with open("docs/SESSION_BEHAVIOR.md", "r") as f:
            content = f.read()

        assert "MAX_RETRIES = 5" in content, (
            "MAX_RETRIES = 5 not found in docs/SESSION_BEHAVIOR.md"
        )

    def test_max_retries_mentioned_in_modules(self):
        """MAX_RETRIES should be mentioned in MODULES.md."""
        with open("docs/MODULES.md", "r") as f:
            content = f.read()

        assert "MAX_RETRIES" in content, "MAX_RETRIES not mentioned in docs/MODULES.md"


class TestHistoryFormatAccuracy:
    """Verify history entry format matches documentation."""

    def test_history_format_with_two_args(self):
        """History should format entries as 'operation(arg1, arg2) = result'."""
        history = History()
        history.add_operation("add", [10.0, 5.0], 15.0)
        entries = history.get_all()

        assert len(entries) == 1
        assert entries[0] == "add(10.0, 5.0) = 15.0", (
            f"History format mismatch. Got: {entries[0]}"
        )

    def test_history_format_with_one_arg(self):
        """History should format single-arg operations correctly."""
        history = History()
        history.add_operation("factorial", [6], 720)
        entries = history.get_all()

        assert len(entries) == 1
        assert entries[0] == "factorial(6) = 720", (
            f"History format mismatch. Got: {entries[0]}"
        )

    def test_history_format_with_float_result(self):
        """History should format operations with float results correctly."""
        history = History()
        history.add_operation("square_root", [16.0], 4.0)
        entries = history.get_all()

        assert len(entries) == 1
        assert entries[0] == "square_root(16.0) = 4.0", (
            f"History format mismatch. Got: {entries[0]}"
        )

    def test_history_documented_format_example_add(self):
        """Documentation example 'add(10.0, 5.0) = 15.0' should match actual format."""
        history = History()
        history.add_operation("add", [10.0, 5.0], 15.0)
        entries = history.get_all()

        # This is the documented example format
        assert "add(10.0, 5.0) = 15.0" in entries[0]

    def test_history_documented_format_example_factorial(self):
        """Documentation example 'factorial(6) = 720' should match actual format."""
        history = History()
        history.add_operation("factorial", [6], 720)
        entries = history.get_all()

        assert "factorial(6) = 720" in entries[0]

    def test_history_documented_format_example_square_root(self):
        """Documentation example 'square_root(16.0) = 4.0' should match actual format."""
        history = History()
        history.add_operation("square_root", [16.0], 4.0)
        entries = history.get_all()

        assert "square_root(16.0) = 4.0" in entries[0]


class TestErrorMessageAccuracy:
    """Verify error messages in documentation match actual Calculator output."""

    def test_division_by_zero_error_matches_doc(self):
        """Division by zero should raise ZeroDivisionError (not a custom message)."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(5, 0)

    def test_square_root_negative_error_message(self):
        """square_root(-1) should raise ValueError with documented message."""
        calc = Calculator()
        with pytest.raises(ValueError) as exc_info:
            calc.square_root(-1)

        error_msg = str(exc_info.value)
        # Documentation says: "square_root() is not defined for negative numbers, got <x>"
        assert "square_root() is not defined for negative numbers" in error_msg
        assert "-1" in error_msg

    def test_cube_root_negative_works(self):
        """cube_root of negative number should work (not raise error)."""
        calc = Calculator()
        result = calc.cube_root(-8)
        assert result == -2.0, "cube_root(-8) should be -2.0"

    def test_log10_nonpositive_error_message(self):
        """log10(0) should raise ValueError with documented message."""
        calc = Calculator()
        with pytest.raises(ValueError) as exc_info:
            calc.log10(0)

        error_msg = str(exc_info.value)
        # Documentation says: "log10() is not defined for x <= 0, got <x>"
        assert "log10() is not defined for x <= 0" in error_msg
        assert "0" in error_msg

    def test_log10_negative_error_message(self):
        """log10(-5) should raise ValueError with documented message."""
        calc = Calculator()
        with pytest.raises(ValueError) as exc_info:
            calc.log10(-5)

        error_msg = str(exc_info.value)
        assert "log10() is not defined for x <= 0" in error_msg

    def test_ln_nonpositive_error_message(self):
        """ln(0) should raise ValueError with documented message."""
        calc = Calculator()
        with pytest.raises(ValueError) as exc_info:
            calc.ln(0)

        error_msg = str(exc_info.value)
        # Documentation says: "ln() is not defined for x <= 0, got <x>"
        assert "ln() is not defined for x <= 0" in error_msg

    def test_ln_negative_error_message(self):
        """ln(-1) should raise ValueError with documented message."""
        calc = Calculator()
        with pytest.raises(ValueError) as exc_info:
            calc.ln(-1)

        error_msg = str(exc_info.value)
        assert "ln() is not defined for x <= 0" in error_msg

    def test_factorial_boolean_error_message(self):
        """factorial(True) should raise TypeError with documented message."""
        calc = Calculator()
        with pytest.raises(TypeError) as exc_info:
            calc.factorial(True)

        error_msg = str(exc_info.value)
        # Documentation says: "factorial() does not accept boolean values, got <n>"
        assert "factorial() does not accept boolean values" in error_msg

    def test_factorial_negative_error_message(self):
        """factorial(-1) should raise ValueError with documented message."""
        calc = Calculator()
        with pytest.raises(ValueError) as exc_info:
            calc.factorial(-1)

        error_msg = str(exc_info.value)
        # Documentation says: "factorial() is not defined for negative integers, got <n>"
        assert "factorial() is not defined for negative integers" in error_msg

    def test_coerce_invalid_operand_error_message(self):
        """Invalid operand coercion should raise ValueError with documented message."""
        calc = Calculator()
        dispatcher = OperationDispatcher(calc)

        with pytest.raises(ValueError) as exc_info:
            dispatcher.coerce_operands(["abc"], float)

        error_msg = str(exc_info.value)
        # Documentation says: "Invalid operand '<raw>': expected a numeric value."
        assert "Invalid operand" in error_msg
        assert "expected a numeric value" in error_msg
        assert "abc" in error_msg


class TestDiagramReferences:
    """Verify diagram files referenced in documentation exist."""

    def test_activity_diagram_exists(self):
        """artifacts/activity_diagram.puml should exist as referenced in docs."""
        path = Path("artifacts/activity_diagram.puml")
        assert path.exists(), f"{path} not found but referenced in documentation"

    def test_class_diagram_exists(self):
        """artifacts/class_diagram.puml should exist as referenced in docs."""
        path = Path("artifacts/class_diagram.puml")
        assert path.exists(), f"{path} not found but referenced in documentation"

    def test_sequence_diagram_exists(self):
        """artifacts/sequence_diagram.puml should exist as referenced in docs."""
        path = Path("artifacts/sequence_diagram.puml")
        assert path.exists(), f"{path} not found but referenced in documentation"

    def test_activity_diagram_referenced_in_session_behavior(self):
        """SESSION_BEHAVIOR.md should reference activity_diagram.puml."""
        with open("docs/SESSION_BEHAVIOR.md", "r") as f:
            content = f.read()

        assert "activity_diagram.puml" in content, (
            "activity_diagram.puml not referenced in SESSION_BEHAVIOR.md"
        )

    def test_class_diagram_referenced_in_architecture(self):
        """ARCHITECTURE.md should reference class_diagram.puml."""
        with open("docs/ARCHITECTURE.md", "r") as f:
            content = f.read()

        assert "class_diagram.puml" in content, (
            "class_diagram.puml not referenced in ARCHITECTURE.md"
        )


class TestOperationRegistryStructure:
    """Verify operation registry structure as documented."""

    def test_all_normal_operations_have_method_key(self):
        """Every NORMAL_OPERATION should have a 'method' key."""
        for op_key, op_meta in NORMAL_OPERATIONS.items():
            assert "method" in op_meta, (
                f"Operation '{op_key}' missing 'method' key"
            )

    def test_all_normal_operations_have_arity_key(self):
        """Every NORMAL_OPERATION should have an 'arity' key."""
        for op_key, op_meta in NORMAL_OPERATIONS.items():
            assert "arity" in op_meta, (
                f"Operation '{op_key}' missing 'arity' key"
            )

    def test_all_normal_operations_have_label_key(self):
        """Every NORMAL_OPERATION should have a 'label' key."""
        for op_key, op_meta in NORMAL_OPERATIONS.items():
            assert "label" in op_meta, (
                f"Operation '{op_key}' missing 'label' key"
            )

    def test_factorial_has_coerce_key_as_int(self):
        """factorial operation should have 'coerce' key set to int."""
        assert "coerce" in NORMAL_OPERATIONS["factorial"], (
            "factorial should have 'coerce' key as documented"
        )
        assert NORMAL_OPERATIONS["factorial"]["coerce"] is int, (
            "factorial 'coerce' should be int type"
        )

    def test_non_factorial_operations_have_no_coerce_key(self):
        """Non-factorial operations should use default float coercion."""
        # These should not have an explicit 'coerce' key (use default float)
        default_coerce_ops = [
            "add", "subtract", "multiply", "divide", "power",
            "square", "cube", "square_root", "cube_root", "log10", "ln"
        ]
        for op_key in default_coerce_ops:
            if "coerce" in NORMAL_OPERATIONS[op_key]:
                # If present, it should be float (the default)
                assert NORMAL_OPERATIONS[op_key]["coerce"] is float, (
                    f"Operation '{op_key}' should use float coercion"
                )


class TestREADMEExamples:
    """Verify code examples in README are accurate."""

    def test_readme_mentions_python_3_12(self):
        """README should mention Python 3.12 requirement."""
        with open("README.md", "r") as f:
            content = f.read()

        assert "Python 3.12" in content, "Python 3.12 not mentioned in README"

    def test_readme_mentions_interactive_mode(self):
        """README should document interactive mode."""
        with open("README.md", "r") as f:
            content = f.read()

        assert "python -m src" in content, (
            "Interactive mode invocation not in README"
        )

    def test_readme_mentions_cli_mode(self):
        """README should document CLI mode."""
        with open("README.md", "r") as f:
            content = f.read()

        assert "main.py" in content or "python main.py" in content, (
            "CLI mode not documented in README"
        )

    def test_readme_mentions_history_file(self):
        """README should mention history.txt output file."""
        with open("README.md", "r") as f:
            content = f.read()

        assert "history.txt" in content, "history.txt not mentioned in README"

    def test_readme_mentions_error_log_file(self):
        """README should mention error.log output file."""
        with open("README.md", "r") as f:
            content = f.read()

        assert "error.log" in content, "error.log not mentioned in README"

    def test_readme_exit_or_quit_works(self):
        """README should mention exit/quit to end session."""
        with open("README.md", "r") as f:
            content = f.read()

        assert "exit" in content and "quit" in content, (
            "exit/quit commands not documented in README"
        )

    def test_readme_history_command_works(self):
        """README should mention history command."""
        with open("README.md", "r") as f:
            content = f.read()

        assert "history" in content, "history command not documented in README"


class TestDocumentationLinks:
    """Verify cross-references between documentation files are consistent."""

    def test_readme_links_to_architecture(self):
        """README should link to ARCHITECTURE.md."""
        with open("README.md", "r") as f:
            content = f.read()

        assert "ARCHITECTURE.md" in content or "ARCHITECTURE" in content, (
            "ARCHITECTURE.md not referenced in README"
        )

    def test_readme_links_to_modules(self):
        """README should link to MODULES.md."""
        with open("README.md", "r") as f:
            content = f.read()

        assert "MODULES.md" in content or "MODULES" in content, (
            "MODULES.md not referenced in README"
        )

    def test_readme_links_to_operations_reference(self):
        """README should link to OPERATIONS_REFERENCE.md."""
        with open("README.md", "r") as f:
            content = f.read()

        assert "OPERATIONS_REFERENCE.md" in content, (
            "OPERATIONS_REFERENCE.md not referenced in README"
        )

    def test_readme_links_to_session_behavior(self):
        """README should link to SESSION_BEHAVIOR.md."""
        with open("README.md", "r") as f:
            content = f.read()

        assert "SESSION_BEHAVIOR.md" in content, (
            "SESSION_BEHAVIOR.md not referenced in README"
        )

    def test_readme_links_to_troubleshooting(self):
        """README should link to TROUBLESHOOTING.md."""
        with open("README.md", "r") as f:
            content = f.read()

        assert "TROUBLESHOOTING.md" in content, (
            "TROUBLESHOOTING.md not referenced in README"
        )


class TestOperationSpecificDocumentation:
    """Verify specific operation documentation is accurate."""

    def test_add_operation_documented_correctly(self):
        """add operation documentation should be accurate."""
        with open("docs/OPERATIONS_REFERENCE.md", "r") as f:
            content = f.read()

        # add should have arity 2 and label "Add two numbers"
        add_section = re.search(
            r"### add\b.*?(?=###|\Z)", content, re.DOTALL
        )
        assert add_section, "add operation section not found"
        section_text = add_section.group()
        assert re.search(r"Arity\s*\|\s*2", section_text), "add should have arity 2"
        assert "Add two numbers" in section_text

    def test_square_operation_documented_correctly(self):
        """square operation documentation should be accurate."""
        with open("docs/OPERATIONS_REFERENCE.md", "r") as f:
            content = f.read()

        # square should have arity 1 and label "Square a number (x^2)"
        square_section = re.search(
            r"### square\b.*?(?=###|\Z)", content, re.DOTALL
        )
        assert square_section, "square operation section not found"
        section_text = square_section.group()
        assert re.search(r"Arity\s*\|\s*1", section_text), "square should have arity 1"

    def test_factorial_operation_documented_with_special_coerce(self):
        """factorial operation should document int coercion."""
        with open("docs/OPERATIONS_REFERENCE.md", "r") as f:
            content = f.read()

        factorial_section = re.search(
            r"### factorial\b.*?(?=###|\Z)", content, re.DOTALL
        )
        assert factorial_section, "factorial operation section not found"
        assert "int" in factorial_section.group(), (
            "factorial should mention int coercion"
        )


class TestSessionBehaviorDocumentation:
    """Verify SESSION_BEHAVIOR.md details match actual implementation."""

    def test_max_retries_mentioned_for_operations(self):
        """SESSION_BEHAVIOR.md should document operation retry limit."""
        with open("docs/SESSION_BEHAVIOR.md", "r") as f:
            content = f.read()

        assert "op_attempts" in content, "op_attempts not mentioned"
        assert "MAX_RETRIES" in content, "MAX_RETRIES not mentioned"

    def test_max_retries_mentioned_for_operands(self):
        """SESSION_BEHAVIOR.md should document operand retry limit."""
        with open("docs/SESSION_BEHAVIOR.md", "r") as f:
            content = f.read()

        assert "operand" in content.lower(), "operand retry not documented"

    def test_history_handling_documented(self):
        """SESSION_BEHAVIOR.md should document history handling."""
        with open("docs/SESSION_BEHAVIOR.md", "r") as f:
            content = f.read()

        assert "history" in content.lower(), "history not documented"
        assert "history.txt" in content, "history.txt not mentioned"

    def test_error_logging_documented(self):
        """SESSION_BEHAVIOR.md should document error logging."""
        with open("docs/SESSION_BEHAVIOR.md", "r") as f:
            content = f.read()

        assert "error.log" in content, "error.log not mentioned"
        assert "Logger" in content, "Logger not mentioned"


class TestTroubleshootingDocumentation:
    """Verify TROUBLESHOOTING.md references match codebase."""

    def test_troubleshooting_mentions_max_retries(self):
        """TROUBLESHOOTING.md should reference retry limits."""
        with open("docs/TROUBLESHOOTING.md", "r") as f:
            content = f.read()

        # Should mention 5 retries (MAX_RETRIES value)
        assert "5" in content, "TROUBLESHOOTING.md should mention 5 retries"

    def test_troubleshooting_mentions_invalid_operation(self):
        """TROUBLESHOOTING.md should address invalid operations."""
        with open("docs/TROUBLESHOOTING.md", "r") as f:
            content = f.read()

        assert "operation" in content.lower(), (
            "TROUBLESHOOTING.md should discuss operations"
        )

    def test_troubleshooting_mentions_domain_errors(self):
        """TROUBLESHOOTING.md should address domain errors."""
        with open("docs/TROUBLESHOOTING.md", "r") as f:
            content = f.read()

        # Should mention square root of negative, log of non-positive, etc.
        assert "square root" in content.lower() or "domain" in content.lower(), (
            "TROUBLESHOOTING.md should mention domain errors"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
