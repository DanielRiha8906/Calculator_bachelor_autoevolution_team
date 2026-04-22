"""Tests for documentation files accuracy and consistency."""

import os
import pytest


# ==============================================================================
# File Existence Tests
# ==============================================================================

class TestDocumentationFileExistence:
    """Verify all required documentation files exist."""

    def test_readme_exists(self):
        """Test that docs/README.md exists."""
        path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'README.md')
        assert os.path.isfile(path), f"docs/README.md does not exist at {path}"

    def test_operations_reference_exists(self):
        """Test that docs/OPERATIONS_REFERENCE.md exists."""
        path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'OPERATIONS_REFERENCE.md')
        assert os.path.isfile(path), f"docs/OPERATIONS_REFERENCE.md does not exist at {path}"

    def test_architecture_exists(self):
        """Test that docs/ARCHITECTURE.md exists."""
        path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'ARCHITECTURE.md')
        assert os.path.isfile(path), f"docs/ARCHITECTURE.md does not exist at {path}"

    def test_development_exists(self):
        """Test that docs/DEVELOPMENT.md exists."""
        path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'DEVELOPMENT.md')
        assert os.path.isfile(path), f"docs/DEVELOPMENT.md does not exist at {path}"


# ==============================================================================
# Content Loading Fixture
# ==============================================================================

@pytest.fixture(scope="module")
def docs_content():
    """Load all documentation files into memory once for the test module."""
    base_path = os.path.join(os.path.dirname(__file__), '..', 'docs')

    content = {
        'readme': _read_file(os.path.join(base_path, 'README.md')),
        'operations_reference': _read_file(os.path.join(base_path, 'OPERATIONS_REFERENCE.md')),
        'architecture': _read_file(os.path.join(base_path, 'ARCHITECTURE.md')),
        'development': _read_file(os.path.join(base_path, 'DEVELOPMENT.md')),
    }

    return content


def _read_file(path):
    """Read a file and return its contents."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


# ==============================================================================
# Content Size Tests (Non-empty)
# ==============================================================================

class TestDocumentationContentSize:
    """Verify documentation files contain substantial content."""

    def test_readme_has_minimum_content(self, docs_content):
        """Test that README.md has at least 500 characters."""
        assert len(docs_content['readme']) >= 500, \
            f"README.md is too short ({len(docs_content['readme'])} chars, expected >= 500)"

    def test_operations_reference_has_minimum_content(self, docs_content):
        """Test that OPERATIONS_REFERENCE.md has at least 500 characters."""
        assert len(docs_content['operations_reference']) >= 500, \
            f"OPERATIONS_REFERENCE.md is too short ({len(docs_content['operations_reference'])} chars, expected >= 500)"

    def test_architecture_has_minimum_content(self, docs_content):
        """Test that ARCHITECTURE.md has at least 500 characters."""
        assert len(docs_content['architecture']) >= 500, \
            f"ARCHITECTURE.md is too short ({len(docs_content['architecture'])} chars, expected >= 500)"

    def test_development_has_minimum_content(self, docs_content):
        """Test that DEVELOPMENT.md has at least 500 characters."""
        assert len(docs_content['development']) >= 500, \
            f"DEVELOPMENT.md is too short ({len(docs_content['development'])} chars, expected >= 500)"


# ==============================================================================
# Cross-link Consistency Tests
# ==============================================================================

class TestCrossLinkConsistency:
    """Verify that README.md references the expected other documentation files."""

    def test_readme_references_operations_reference(self, docs_content):
        """Test that README.md contains reference to OPERATIONS_REFERENCE.md."""
        readme = docs_content['readme']
        assert 'OPERATIONS_REFERENCE.md' in readme, \
            "README.md does not reference OPERATIONS_REFERENCE.md"

    def test_readme_references_architecture(self, docs_content):
        """Test that README.md contains reference to ARCHITECTURE.md."""
        readme = docs_content['readme']
        assert 'ARCHITECTURE.md' in readme, \
            "README.md does not reference ARCHITECTURE.md"

    def test_readme_references_development(self, docs_content):
        """Test that README.md contains reference to DEVELOPMENT.md."""
        readme = docs_content['readme']
        assert 'DEVELOPMENT.md' in readme, \
            "README.md does not reference DEVELOPMENT.md"


# ==============================================================================
# Operation Names Accuracy Tests
# ==============================================================================

class TestOperationNamesAccuracy:
    """Verify that OPERATIONS_REFERENCE.md documents all expected operations."""

    @pytest.mark.parametrize("operation", [
        "add", "subtract", "multiply", "divide",
        "factorial", "square", "cube",
        "square_root", "cube_root", "power",
        "natural_log", "log_base_10",
    ])
    def test_operations_reference_contains_operation(self, docs_content, operation):
        """Test that OPERATIONS_REFERENCE.md documents the given operation."""
        ops_ref = docs_content['operations_reference']
        # Check for the operation name as a code block (e.g., `add`, `subtract`, etc.)
        # and also ensure it appears in a section header or documentation
        assert f"`{operation}`" in ops_ref or f"## `{operation}`" in ops_ref, \
            f"OPERATIONS_REFERENCE.md does not document operation: {operation}"


# ==============================================================================
# Source File References Tests
# ==============================================================================

class TestSourceFileReferences:
    """Verify that all source files mentioned in docs actually exist."""

    @pytest.mark.parametrize("file_path", [
        "src/calculator.py",
        "src/logic.py",
        "src/modes/basic.py",
        "src/modes/advanced.py",
        "src/input_handler.py",
        "src/cli.py",
        "src/logger.py",
    ])
    def test_source_file_exists(self, file_path):
        """Test that the source file referenced in documentation exists."""
        full_path = os.path.join(os.path.dirname(__file__), '..', file_path)
        assert os.path.isfile(full_path), \
            f"Source file referenced in docs does not exist: {file_path}"


# ==============================================================================
# Additional Documentation Quality Tests
# ==============================================================================

class TestDocumentationQuality:
    """Verify general quality attributes of documentation."""

    def test_readme_has_headers(self, docs_content):
        """Test that README.md contains markdown headers."""
        readme = docs_content['readme']
        assert '#' in readme, "README.md does not contain markdown headers"

    def test_operations_reference_has_headers(self, docs_content):
        """Test that OPERATIONS_REFERENCE.md contains markdown headers."""
        ops_ref = docs_content['operations_reference']
        assert '#' in ops_ref, "OPERATIONS_REFERENCE.md does not contain markdown headers"

    def test_architecture_has_headers(self, docs_content):
        """Test that ARCHITECTURE.md contains markdown headers."""
        arch = docs_content['architecture']
        assert '#' in arch, "ARCHITECTURE.md does not contain markdown headers"

    def test_development_has_headers(self, docs_content):
        """Test that DEVELOPMENT.md contains markdown headers."""
        dev = docs_content['development']
        assert '#' in dev, "DEVELOPMENT.md does not contain markdown headers"

    def test_readme_has_code_examples(self, docs_content):
        """Test that README.md contains code examples."""
        readme = docs_content['readme']
        assert '```' in readme, "README.md does not contain code examples"

    def test_operations_reference_has_examples(self, docs_content):
        """Test that OPERATIONS_REFERENCE.md contains examples."""
        ops_ref = docs_content['operations_reference']
        assert 'Examples:' in ops_ref or 'Example' in ops_ref, \
            "OPERATIONS_REFERENCE.md does not contain examples"

    def test_architecture_has_code_or_diagrams(self, docs_content):
        """Test that ARCHITECTURE.md contains code blocks or diagrams."""
        arch = docs_content['architecture']
        assert '```' in arch, "ARCHITECTURE.md does not contain code blocks or diagrams"

    def test_development_has_code_examples(self, docs_content):
        """Test that DEVELOPMENT.md contains code examples."""
        dev = docs_content['development']
        assert '```' in dev, "DEVELOPMENT.md does not contain code examples"


# ==============================================================================
# Module Structure Tests
# ==============================================================================

class TestModuleStructureDocumentation:
    """Verify that module documentation is internally consistent."""

    def test_architecture_documents_all_modules(self, docs_content):
        """Test that ARCHITECTURE.md documents the key modules."""
        arch = docs_content['architecture']
        required_modules = [
            'main.py', 'calculator.py', 'logic.py',
            'basic.py', 'advanced.py', 'operations.py',
            'input_handler.py', 'cli.py', 'logger.py'
        ]
        for module in required_modules:
            assert module in arch, \
                f"ARCHITECTURE.md does not document module: {module}"

    def test_development_mentions_testing_framework(self, docs_content):
        """Test that DEVELOPMENT.md mentions pytest."""
        dev = docs_content['development']
        assert 'pytest' in dev.lower(), \
            "DEVELOPMENT.md does not mention pytest testing framework"

    def test_development_mentions_python_version(self, docs_content):
        """Test that DEVELOPMENT.md specifies Python version."""
        dev = docs_content['development']
        assert 'python' in dev.lower() or '3.12' in dev, \
            "DEVELOPMENT.md does not specify Python version"


# ==============================================================================
# Operation Category Tests
# ==============================================================================

class TestOperationCategories:
    """Verify that operations are correctly categorized in documentation."""

    def test_operations_reference_has_basic_section(self, docs_content):
        """Test that OPERATIONS_REFERENCE.md has a Basic Operations section."""
        ops_ref = docs_content['operations_reference']
        assert 'Basic Operation' in ops_ref, \
            "OPERATIONS_REFERENCE.md does not have a Basic Operations section"

    def test_operations_reference_has_advanced_section(self, docs_content):
        """Test that OPERATIONS_REFERENCE.md has an Advanced Operations section."""
        ops_ref = docs_content['operations_reference']
        assert 'Advanced Operation' in ops_ref, \
            "OPERATIONS_REFERENCE.md does not have an Advanced Operations section"

    @pytest.mark.parametrize("basic_op", ["add", "subtract", "multiply", "divide"])
    def test_basic_operations_in_correct_section(self, docs_content, basic_op):
        """Test that basic operations appear in the Basic Operations section."""
        ops_ref = docs_content['operations_reference']
        # Find the Basic Operations section and verify it contains basic ops
        basic_section_start = ops_ref.find("## Basic Operation")
        advanced_section_start = ops_ref.find("## Advanced Operation")

        assert basic_section_start != -1, "No Basic Operations section found"
        assert advanced_section_start != -1, "No Advanced Operations section found"

        # Verify the operation appears between Basic and Advanced sections
        basic_section = ops_ref[basic_section_start:advanced_section_start]
        assert f"`{basic_op}`" in basic_section, \
            f"Operation '{basic_op}' not found in Basic Operations section"

    @pytest.mark.parametrize("advanced_op", ["factorial", "square", "cube", "square_root", "cube_root", "power", "natural_log", "log_base_10"])
    def test_advanced_operations_in_correct_section(self, docs_content, advanced_op):
        """Test that advanced operations appear in the Advanced Operations section."""
        ops_ref = docs_content['operations_reference']
        advanced_section_start = ops_ref.find("## Advanced Operation")
        error_summary_start = ops_ref.find("## Error Handling Summary")

        assert advanced_section_start != -1, "No Advanced Operations section found"
        assert error_summary_start != -1, "No Error Handling Summary section found"

        # Verify the operation appears in the Advanced section
        advanced_section = ops_ref[advanced_section_start:error_summary_start]
        assert f"`{advanced_op}`" in advanced_section, \
            f"Operation '{advanced_op}' not found in Advanced Operations section"
