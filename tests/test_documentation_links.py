"""Test documentation links and file existence.

Verifies that all documentation files referenced in README.md exist
and are accessible.
"""

import pytest
from pathlib import Path


class TestDocumentationLinks:
    """Test that all documentation links in README.md resolve to existing files."""

    @pytest.fixture
    def docs_dir(self):
        """Path to the docs directory."""
        return Path(__file__).parent.parent / "docs"

    @pytest.fixture
    def readme_path(self):
        """Path to the README.md file."""
        return Path(__file__).parent.parent / "README.md"

    def test_readme_exists(self, readme_path):
        """Test that README.md exists."""
        assert readme_path.exists(), "README.md does not exist"
        assert readme_path.is_file(), "README.md is not a file"

    def test_readme_links_to_architecture(self, docs_dir):
        """Test that docs/ARCHITECTURE.md exists."""
        arch_path = docs_dir / "ARCHITECTURE.md"
        assert arch_path.exists(), f"{arch_path} does not exist"
        assert arch_path.is_file(), f"{arch_path} is not a file"

    def test_readme_links_to_operation_reference(self, docs_dir):
        """Test that docs/OPERATION_REFERENCE.md exists."""
        op_ref_path = docs_dir / "OPERATION_REFERENCE.md"
        assert op_ref_path.exists(), f"{op_ref_path} does not exist"
        assert op_ref_path.is_file(), f"{op_ref_path} is not a file"

    def test_readme_links_to_session_behavior(self, docs_dir):
        """Test that docs/SESSION_BEHAVIOR.md exists."""
        session_path = docs_dir / "SESSION_BEHAVIOR.md"
        assert session_path.exists(), f"{session_path} does not exist"
        assert session_path.is_file(), f"{session_path} is not a file"

    def test_readme_links_to_user_guide(self, docs_dir):
        """Test that docs/USER_GUIDE.md exists."""
        user_guide_path = docs_dir / "USER_GUIDE.md"
        assert user_guide_path.exists(), f"{user_guide_path} does not exist"
        assert user_guide_path.is_file(), f"{user_guide_path} is not a file"

    def test_readme_links_to_cli_reference(self, docs_dir):
        """Test that docs/CLI_REFERENCE.md exists."""
        cli_ref_path = docs_dir / "CLI_REFERENCE.md"
        assert cli_ref_path.exists(), f"{cli_ref_path} does not exist"
        assert cli_ref_path.is_file(), f"{cli_ref_path} is not a file"

    def test_all_doc_files_readable(self, docs_dir):
        """Test that all documentation files are readable."""
        doc_files = [
            "ARCHITECTURE.md",
            "OPERATION_REFERENCE.md",
            "SESSION_BEHAVIOR.md",
            "USER_GUIDE.md",
            "CLI_REFERENCE.md",
        ]
        for doc_file in doc_files:
            path = docs_dir / doc_file
            assert path.exists(), f"{doc_file} does not exist"
            content = path.read_text()
            assert len(content) > 0, f"{doc_file} is empty"

    def test_readme_contains_documentation_section(self, readme_path):
        """Test that README.md contains a Documentation section."""
        content = readme_path.read_text()
        assert "Documentation" in content, "README.md does not contain Documentation section"

    def test_readme_contains_all_doc_links(self, readme_path):
        """Test that README.md references all documentation files."""
        content = readme_path.read_text()
        doc_files = [
            "ARCHITECTURE.md",
            "OPERATION_REFERENCE.md",
            "SESSION_BEHAVIOR.md",
            "USER_GUIDE.md",
            "CLI_REFERENCE.md",
        ]
        for doc_file in doc_files:
            assert doc_file in content, f"README.md does not reference {doc_file}"
