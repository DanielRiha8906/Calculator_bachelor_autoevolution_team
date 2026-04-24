"""
Tests for README.md documentation.

Verifies that README.md exists, is readable, and contains comprehensive documentation
of calculator features, modes, error handling, and usage instructions.
"""

import os
import pytest
from pathlib import Path


# Get the repository root by going up from the tests directory
REPO_ROOT = Path(__file__).parent.parent
README_PATH = REPO_ROOT / "README.md"


class TestReadmeDocumentation:
    """Test suite for README.md existence and content."""

    @pytest.fixture
    def readme_content(self):
        """Read README.md content once for all tests that need it."""
        with open(README_PATH, "r", encoding="utf-8") as f:
            return f.read()

    def test_readme_exists(self):
        """Verify README.md file exists at repository root."""
        assert README_PATH.exists(), f"README.md not found at {README_PATH}"
        assert README_PATH.is_file(), f"README.md is not a regular file: {README_PATH}"

    def test_readme_contains_title_section(self, readme_content):
        """Verify README.md has a title/header (Markdown h1)."""
        assert "#" in readme_content, "README.md missing Markdown h1 header (# symbol)"
        # Check for h1 at start of a line
        lines = readme_content.split("\n")
        has_h1 = any(line.strip().startswith("#") for line in lines)
        assert has_h1, "README.md missing Markdown h1 header at line start"

    def test_readme_contains_features_section(self, readme_content):
        """Verify README.md documents all calculator features/operations."""
        readme_lower = readme_content.lower()
        required_features = [
            "add", "subtract", "multiply", "divide", "factorial", "modulo",
            "square", "cube", "power", "log", "ln"
        ]
        missing = [f for f in required_features if f not in readme_lower]
        assert not missing, f"README.md missing documentation for: {missing}"

    def test_readme_contains_arithmetic_section(self, readme_content):
        """Verify README.md distinguishes arithmetic operations."""
        assert "arithmetic" in readme_content.lower(), \
            "README.md missing 'arithmetic' section"

    def test_readme_contains_scientific_section(self, readme_content):
        """Verify README.md distinguishes scientific operations."""
        assert "scientific" in readme_content.lower(), \
            "README.md missing 'scientific' section"

    def test_readme_contains_cli_mode_documentation(self, readme_content):
        """Verify README.md documents CLI mode usage."""
        assert "python -m src" in readme_content, \
            "README.md missing CLI invocation pattern (python -m src)"

    def test_readme_contains_interactive_mode_documentation(self, readme_content):
        """Verify README.md documents interactive mode."""
        assert "interactive" in readme_content.lower(), \
            "README.md missing 'interactive' mode documentation"

    def test_readme_contains_cli_usage_examples(self, readme_content):
        """Verify README.md includes concrete CLI command examples."""
        count = readme_content.count("python -m src")
        assert count >= 3, \
            f"README.md has {count} CLI examples (need at least 3)"

    def test_readme_contains_interactive_usage_examples(self, readme_content):
        """Verify README.md includes interactive mode interaction examples."""
        readme_lower = readme_content.lower()
        has_exit_cmd = "quit" in readme_lower or "exit" in readme_lower
        assert has_exit_cmd, \
            "README.md missing exit command (quit/exit) for interactive mode"

        # Check for at least one operation name in example context
        operations = ["add", "subtract", "multiply", "divide", "factorial"]
        has_operation_example = any(op in readme_lower for op in operations)
        assert has_operation_example, \
            "README.md missing operation example in interactive section"

    def test_readme_contains_error_handling_section(self, readme_content):
        """Verify README.md documents error handling behavior."""
        lines = readme_content.split("\n")
        header_lines = [line for line in lines if line.strip().startswith("#")]
        header_text = " ".join(h.lower() for h in header_lines)
        assert "error" in header_text, \
            "README.md missing 'error' in section headers"

    def test_readme_contains_project_structure_section(self, readme_content):
        """Verify README.md describes project structure."""
        assert "src/" in readme_content, "README.md missing 'src/' directory reference"
        assert "tests/" in readme_content, "README.md missing 'tests/' directory reference"

    def test_readme_contains_history_feature_documentation(self, readme_content):
        """Verify README.md mentions operation history feature."""
        assert "history" in readme_content.lower(), \
            "README.md missing 'history' feature documentation"

    def test_readme_contains_error_logging_feature_documentation(self, readme_content):
        """Verify README.md mentions error logging feature."""
        readme_lower = readme_content.lower()
        has_log = "log" in readme_lower
        has_error = "error" in readme_lower
        assert has_log and has_error, \
            "README.md missing error logging feature documentation (log + error)"

    def test_readme_contains_failure_limit_documentation(self, readme_content):
        """Verify README.md documents the 3-strike consecutive failure limit."""
        has_three = "3" in readme_content
        has_failure_context = any(
            word in readme_content.lower()
            for word in ["consecutive", "failure", "attempts"]
        )
        assert has_three and has_failure_context, \
            "README.md missing documentation of 3-strike consecutive failure limit"

    def test_readme_is_valid_markdown(self, readme_content):
        """Verify README.md is non-empty and has basic markdown structure."""
        # Check file size (should be > 500 bytes for meaningful content)
        assert len(readme_content) > 500, \
            f"README.md is too short ({len(readme_content)} bytes, need > 500)"

        # Check for at least 3 Markdown headers
        header_count = readme_content.count("\n#")
        assert header_count >= 3, \
            f"README.md has {header_count} headers (need at least 3)"

        # Check for placeholder text that indicates incomplete documentation
        placeholder_keywords = ["TODO", "PLACEHOLDER", "FIXME", "XXX"]
        for keyword in placeholder_keywords:
            assert keyword not in readme_content.upper(), \
                f"README.md contains placeholder text: {keyword}"

    def test_readme_mentions_modulo_operation(self, readme_content):
        """Verify README.md documents the modulo operation."""
        readme_lower = readme_content.lower()
        has_modulo = "modulo" in readme_lower or "mod" in readme_lower
        assert has_modulo, "README.md missing modulo/mod operation documentation"

    def test_readme_mode_switching_documented(self, readme_content):
        """Verify README.md explains CLI vs interactive mode distinction."""
        readme_lower = readme_content.lower()
        has_cli = "cli" in readme_lower or "command" in readme_lower
        has_interactive = "interactive" in readme_lower
        assert has_cli and has_interactive, \
            "README.md missing documentation of CLI vs interactive mode distinction"
