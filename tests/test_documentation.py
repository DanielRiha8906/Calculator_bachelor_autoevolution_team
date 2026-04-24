"""
Tests to validate README.md documentation exists and has required content.

This test suite verifies that the README includes:
1. User Guide section with usage instructions, examples, and operation documentation
2. Developer Guide section with code structure, module purposes, and test execution
3. Content about operations, domain validation, history tracking, and error logging
"""

import os
import re


class TestREADMEBasics:
    """Tests for basic README.md existence and size requirements."""

    def test_readme_exists(self):
        """Verify README.md exists in repository root."""
        readme_path = "README.md"
        assert os.path.isfile(readme_path), f"{readme_path} not found in repository root"
        assert os.path.getsize(readme_path) > 0, f"{readme_path} is empty"

    def test_readme_is_non_empty(self):
        """Verify README has substantial content (not a stub)."""
        readme_path = "README.md"
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert len(content) > 1000, f"README.md is too small ({len(content)} chars). Expected > 1000 chars."


class TestREADMEUserGuideSection:
    """Tests for User Guide section and its content."""

    def test_readme_has_user_guide_section(self):
        """Verify README.md contains 'User Guide' heading (case-insensitive)."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        # Match "User Guide" as a heading (case-insensitive)
        assert re.search(r"#+\s+.*User\s+Guide.*", content, re.IGNORECASE), \
            "README.md does not contain a 'User Guide' section heading"

    def test_readme_user_guide_has_run_instructions(self):
        """Verify User Guide documents how to run the calculator."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        assert "python -m src" in content, \
            "README.md User Guide does not contain 'python -m src' instruction"

    def test_readme_user_guide_has_interactive_mode_walkthrough(self):
        """Verify User Guide has guided example of interactive mode."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        # Look for "interactive" keyword and some example session content
        has_interactive = re.search(r"interactive", content, re.IGNORECASE)
        has_example = re.search(r">|$|example|session", content, re.IGNORECASE)
        assert has_interactive, \
            "README.md User Guide does not mention 'interactive' mode"
        assert has_example, \
            "README.md User Guide does not contain example session content"

    def test_readme_user_guide_has_cli_syntax(self):
        """Verify User Guide documents CLI syntax and examples."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        # Look for CLI syntax pattern (add/subtract/multiply/divide with operands)
        cli_pattern = r"python\s+-m\s+src\s+(add|subtract|multiply|divide|power|sqrt|factorial)"
        assert re.search(cli_pattern, content), \
            "README.md User Guide does not document CLI syntax with operation examples"

    def test_readme_user_guide_has_operations_list(self):
        """Verify User Guide lists all available operations."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        operations = ["add", "subtract", "multiply", "divide", "power", "factorial",
                      "square", "cube", "sqrt", "cbrt", "ln", "log10"]
        for op in operations:
            assert op.lower() in content.lower(), \
                f"README.md does not document operation '{op}'"

    def test_readme_user_guide_has_history_behavior(self):
        """Verify User Guide documents history tracking."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        assert "history.txt" in content.lower() or "history" in content.lower(), \
            "README.md User Guide does not mention history tracking or history.txt"

    def test_readme_user_guide_has_error_logging(self):
        """Verify User Guide documents error logging."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        assert "error.log" in content.lower() or "error logging" in content.lower(), \
            "README.md User Guide does not mention error logging or error.log"


class TestREADMEDeveloperGuideSection:
    """Tests for Developer Guide section and its content."""

    def test_readme_has_developer_guide_section(self):
        """Verify README.md contains 'Developer Guide' heading (case-insensitive)."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        # Match "Developer Guide" as a heading
        assert re.search(r"#+\s+.*Developer\s+Guide.*", content, re.IGNORECASE), \
            "README.md does not contain a 'Developer Guide' section heading"

    def test_readme_developer_guide_has_code_structure(self):
        """Verify Developer Guide documents refactored module organization."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        required_dirs = ["src/ui", "src/infrastructure", "src/core"]
        for dir_name in required_dirs:
            assert dir_name in content, \
                f"README.md Developer Guide does not mention '{dir_name}' module organization"

    def test_readme_developer_guide_has_module_purposes(self):
        """Verify key modules are described in the developer guide."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        modules = ["calculator.py", "operation_registry.py", "interactive.py",
                   "cli.py", "history.py", "error_logger.py"]
        for module in modules:
            assert module in content, \
                f"README.md Developer Guide does not document module '{module}'"

    def test_readme_developer_guide_has_entry_point_flow(self):
        """Verify entry point flow is documented."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        assert "__main__.py" in content or "entry point" in content.lower(), \
            "README.md Developer Guide does not document __main__.py or entry point dispatch logic"

    def test_readme_developer_guide_has_test_execution(self):
        """Verify how to run tests is documented."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        assert "pytest" in content.lower(), \
            "README.md Developer Guide does not document how to run pytest tests"


class TestREADMEOperationsAndDomainDocumentation:
    """Tests for operations and domain validation documentation."""

    def test_readme_has_operations_with_arity(self):
        """Verify operation categories and arity are documented."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        # Should mention both binary and unary operations
        has_binary = re.search(r"binary|two\s+operand|argument", content, re.IGNORECASE)
        has_unary = re.search(r"unary|one\s+operand|single\s+argument", content, re.IGNORECASE)
        assert has_binary, "README.md does not document binary operations"
        assert has_unary, "README.md does not document unary operations"

    def test_readme_has_domain_validation_info(self):
        """Verify documentation mentions domain validation for operations."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        # Look for mentions of constraints (non-negative, positive, domain, etc.)
        domain_keywords = ["non-negative", "positive", "domain", "constraint", "validation", "error"]
        found_keywords = [kw for kw in domain_keywords if kw.lower() in content.lower()]
        assert len(found_keywords) > 0, \
            "README.md does not document domain validation or operational constraints"
