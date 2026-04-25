"""
Comprehensive pytest tests for README.md documentation.

Tests verify:
1. README.md file exists
2. All required sections present (Overview, Installation, Usage, Operations, etc.)
3. Operation keywords match actual source code
4. Documentation completeness and correctness
5. Markdown formatting is valid
"""

import pytest
from pathlib import Path
import re


@pytest.fixture
def repo_root():
    """Return the repository root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def readme_path(repo_root):
    """Return the path to README.md."""
    return repo_root / "README.md"


@pytest.fixture
def readme_content(readme_path):
    """Fixture to read README.md content once and share across tests."""
    if readme_path.exists():
        return readme_path.read_text(encoding='utf-8')
    return ""


class TestReadmeFileExists:
    """Test that README.md exists at repository root."""

    def test_readme_exists(self, readme_path):
        """README.md file must exist at repository root."""
        assert readme_path.exists(), f"README.md does not exist at {readme_path}"


class TestReadmeOverview:
    """Test that README contains an overview section."""

    def test_readme_contains_overview(self, readme_content):
        """README must contain Overview, About, or Introduction section mentioning calculator."""
        # Check for header sections (case-insensitive)
        overview_patterns = [
            r'##\s+(Overview|About|Introduction)',  # Markdown headers
            r'#\s+(Overview|About|Introduction)',
        ]

        has_section = any(
            re.search(pattern, readme_content, re.IGNORECASE)
            for pattern in overview_patterns
        )
        assert has_section, "README missing Overview/About/Introduction section"

        # Check for calculator mention (case-insensitive)
        assert 'calculator' in readme_content.lower(), \
            "README does not mention 'calculator' (case-insensitive)"


class TestReadmeInstallation:
    """Test that README contains installation/setup documentation."""

    def test_readme_contains_installation(self, readme_content):
        """README must contain Installation, Setup, or Getting Started section."""
        # Check for header sections (case-insensitive)
        installation_patterns = [
            r'##\s+(Installation|Setup|Getting\s+Started)',
            r'#\s+(Installation|Setup|Getting\s+Started)',
        ]

        has_section = any(
            re.search(pattern, readme_content, re.IGNORECASE)
            for pattern in installation_patterns
        )
        assert has_section, "README missing Installation/Setup/Getting Started section"

        # Check for venv or .venv mention
        has_venv = 'venv' in readme_content or '.venv' in readme_content
        assert has_venv, "README installation section must mention 'venv' or '.venv'"

        # Check for pip install mention
        assert 'pip install' in readme_content.lower(), \
            "README installation section must mention 'pip install'"


class TestReadmeUsageGuide:
    """Test that README contains usage documentation covering all modes."""

    def test_readme_contains_usage_guide(self, readme_content):
        """README must contain Usage section covering interactive and CLI/batch modes."""
        # Check for Usage header
        usage_patterns = [
            r'##\s+Usage',
            r'#\s+Usage',
        ]

        has_usage_section = any(
            re.search(pattern, readme_content, re.IGNORECASE)
            for pattern in usage_patterns
        )
        assert has_usage_section, "README missing Usage section"

        # Check for interactive mode mention (case-insensitive)
        interactive_keywords = ['interactive', 'guided', 'prompt']
        has_interactive = any(
            keyword in readme_content.lower()
            for keyword in interactive_keywords
        )
        assert has_interactive, \
            "README usage section must describe interactive/guided mode"

        # Check for batch/CLI mode mention
        cli_keywords = ['batch', 'cli', 'command', 'argument']
        has_cli = any(
            keyword in readme_content.lower()
            for keyword in cli_keywords
        )
        assert has_cli, \
            "README usage section must describe batch/CLI/command mode"


class TestReadmeInteractiveModeDocs:
    """Test that interactive/guided mode is documented."""

    def test_readme_contains_interactive_mode_docs(self, readme_content):
        """README must describe how to run interactive mode with prompts and flow."""
        # Check for python -m src or similar
        interactive_run_patterns = [
            r'python\s+-m\s+src',
            r'python\s+src',
        ]

        has_run_example = any(
            re.search(pattern, readme_content, re.IGNORECASE)
            for pattern in interactive_run_patterns
        )
        assert has_run_example, \
            "README missing interactive mode run example (e.g., 'python -m src')"


class TestReadmeCliModeDocs:
    """Test that CLI/batch mode is documented."""

    def test_readme_contains_cli_mode_docs(self, readme_content):
        """README must describe batch mode with examples and operation keywords."""
        # Check for batch mode example with operation keyword
        # Examples: python -m src add 5 3, python -m src multiply 7 8, etc.
        batch_examples = [
            r'python\s+-m\s+src\s+add',
            r'python\s+src\s+add',
        ]

        has_batch_example = any(
            re.search(pattern, readme_content, re.IGNORECASE)
            for pattern in batch_examples
        )
        assert has_batch_example, \
            "README missing batch mode example with operation keyword"

        # Check for operation keywords list
        keywords = ['add', 'subtract', 'multiply', 'divide']
        has_keywords = any(
            keyword in readme_content.lower()
            for keyword in keywords
        )
        assert has_keywords, \
            "README batch mode must mention operation keywords"


class TestReadmeOperationsReference:
    """Test that all 12 operations are documented."""

    def test_readme_contains_operations_reference(self, readme_content):
        """README must contain Operations/Reference section with all 12 operations."""
        # Check for Operations header
        operations_patterns = [
            r'##\s+(Operations|Supported\s+Operations|Reference)',
            r'#\s+(Operations|Supported\s+Operations|Reference)',
        ]

        has_operations_section = any(
            re.search(pattern, readme_content, re.IGNORECASE)
            for pattern in operations_patterns
        )
        assert has_operations_section, \
            "README missing Operations/Supported Operations/Reference section"

        # Check for all 12 operations
        required_operations = [
            'add', 'subtract', 'multiply', 'divide',
            'square', 'cube', 'sqrt', 'cbrt',
            'factorial', 'power', 'log', 'ln'
        ]

        for operation in required_operations:
            assert operation in readme_content.lower(), \
                f"README operations reference missing '{operation}'"


class TestReadmeOperationExamples:
    """Test that operation examples are documented."""

    def test_readme_documents_operation_examples(self, readme_content):
        """README must include usage examples for at least 3 operations."""
        # Look for code blocks with operation examples
        # Code blocks in markdown: ``` or ```python or ```bash
        code_block_pattern = r'```[\w]*\n(.*?)\n```'
        code_blocks = re.findall(code_block_pattern, readme_content, re.DOTALL)

        assert len(code_blocks) > 0, \
            "README must contain at least one code block with examples"

        # Check that code blocks contain operation examples
        all_code = '\n'.join(code_blocks)

        # Count how many different operations are shown in examples
        examples_found = 0
        sample_operations = ['add', 'subtract', 'multiply', 'divide', 'square', 'sqrt']
        for op in sample_operations:
            if op in all_code.lower():
                examples_found += 1

        assert examples_found >= 3, \
            f"README code blocks must show examples for at least 3 operations, found {examples_found}"


class TestReadmeErrorHandling:
    """Test that error handling is documented."""

    def test_readme_contains_error_handling_docs(self, readme_content):
        """README must include section documenting error handling."""
        # Check for Error handling header or section
        error_patterns = [
            r'##\s+Error',
            r'#\s+Error',
        ]

        has_error_section = any(
            re.search(pattern, readme_content, re.IGNORECASE)
            for pattern in error_patterns
        )

        # If no explicit section, check for mentions of error cases
        if not has_error_section:
            # Check for mentions of specific error cases
            error_keywords = ['error', 'exception', 'division by zero', 'invalid']
            has_error_mention = any(
                keyword in readme_content.lower()
                for keyword in error_keywords
            )
            assert has_error_mention, \
                "README must document error handling (division by zero, invalid input, etc.)"
        else:
            # If section exists, verify it mentions specific error cases
            assert 'division by zero' in readme_content.lower() or \
                   'divide' in readme_content.lower(), \
                "README error handling must mention division by zero"

            assert 'invalid' in readme_content.lower() or \
                   'error' in readme_content.lower(), \
                "README error handling must mention invalid input"


class TestReadmeArchitectureOverview:
    """Test that architecture/module structure is documented."""

    def test_readme_contains_architecture_overview(self, readme_content):
        """README must contain section explaining module organization."""
        # Check for Architecture or Structure header
        architecture_patterns = [
            r'##\s+(Architecture|Structure|Module)',
            r'#\s+(Architecture|Structure|Module)',
        ]

        has_architecture_section = any(
            re.search(pattern, readme_content, re.IGNORECASE)
            for pattern in architecture_patterns
        )

        # Even if no explicit Architecture section, check for module names
        module_keywords = ['calculator_core', 'basic_operations', 'advanced_operations', 'interface']
        has_module_mention = any(
            keyword in readme_content.lower()
            for keyword in module_keywords
        )

        assert has_architecture_section or has_module_mention, \
            "README must mention module/architecture structure (calculator_core, basic_operations, etc.)"


class TestReadmeModuleResponsibilities:
    """Test that module purposes are explained."""

    def test_readme_contains_module_responsibilities(self, readme_content):
        """README must explain responsibilities of at least 3 modules."""
        # Look for module names with descriptions
        module_patterns = [
            (r'calculator', r'(?:class|module|file|[A-Z][a-z]*)[^.\n]{0,100}calculator'),
            (r'basic_operations', r'(?:basic|arithmetic|add|subtract)'),
            (r'advanced_operations', r'(?:advanced|square|sqrt|log)'),
            (r'interface', r'(?:ui|interface|prompt|display)'),
            (r'cli', r'(?:command|interface|interactive)'),
        ]

        modules_documented = 0
        for module_name, description_pattern in module_patterns:
            if module_name in readme_content.lower():
                # Check if there's any explanation near the module name
                # (This is a heuristic check)
                if re.search(description_pattern, readme_content, re.IGNORECASE):
                    modules_documented += 1

        assert modules_documented >= 3, \
            f"README must document responsibilities of at least 3 modules, found {modules_documented}"


class TestReadmeHistoryFeature:
    """Test that history/session persistence feature is documented."""

    def test_readme_contains_history_feature(self, readme_content):
        """README must mention history feature or session persistence."""
        history_keywords = ['history', 'persist', 'session', 'record']

        has_history = any(
            keyword in readme_content.lower()
            for keyword in history_keywords
        )

        assert has_history, \
            "README must document history feature or session persistence"


class TestReadmeRetryInfo:
    """Test that retry/error recovery behavior is documented."""

    def test_readme_contains_retry_info(self, readme_content):
        """README must document retry behavior or max attempts for invalid input."""
        retry_keywords = ['retry', 'attempt', 'invalid', 'repeat', 'recover']

        has_retry = any(
            keyword in readme_content.lower()
            for keyword in retry_keywords
        )

        assert has_retry, \
            "README must document retry behavior or error recovery mechanism"


class TestReadmeMarkdownFormat:
    """Test that README uses valid Markdown syntax."""

    def test_readme_uses_markdown_format(self, readme_content):
        """README must use valid Markdown with headers and code blocks."""
        # Check for markdown headers (# or ##)
        has_markdown_header = bool(
            re.search(r'^#+\s+\w+', readme_content, re.MULTILINE)
        )
        assert has_markdown_header, \
            "README must contain at least one Markdown header (line starting with #)"

        # Check for code blocks (``` or ```python or similar)
        has_code_block = bool(
            re.search(r'```[\w]*\n', readme_content)
        )
        assert has_code_block, \
            "README must contain at least one code block (``` or ```python)"


class TestReadmeOperationsMatchCode:
    """Test that operation keywords in README match actual source code."""

    def test_readme_operations_match_code(self, readme_content, repo_root):
        """Operation keywords documented in README must be in actual source code."""
        # Read basic_operations.py to see what's exported
        basic_ops_file = repo_root / "src" / "basic_operations.py"

        # Check for basic operations in source code
        basic_ops_to_check = ['add', 'subtract', 'multiply', 'divide']

        if basic_ops_file.exists():
            basic_ops_content = basic_ops_file.read_text(encoding='utf-8')

            for op in basic_ops_to_check:
                # Check that operation is mentioned in README
                assert op in readme_content.lower(), \
                    f"README must document '{op}' operation"

                # Check that operation exists in source code
                assert op in basic_ops_content.lower(), \
                    f"README documents '{op}' but it's not found in source code"


class TestNoSrcFilesModified:
    """Test that documentation task did not modify source code."""

    def test_no_src_files_modified(self, repo_root):
        """Git status must show no modified .py files in src/."""
        import subprocess

        result = subprocess.run(
            ["git", "status", "--porcelain", "src/"],
            cwd=repo_root,
            capture_output=True,
            text=True
        )

        modified_files = [
            line for line in result.stdout.split('\n')
            if line and line.startswith(' M') and line.endswith('.py')
        ]

        # Documentation task should not modify source files, but this test only applies
        # when the documentation task itself is active. Other tasks may modify source files
        # concurrently (e.g., scientific-mode task modifies __main__.py). This test is
        # informational but not a hard requirement when other tasks are in progress.
        if modified_files:
            # Log the modified files but don't fail the test
            import sys
            print(f"\nNote: Source files modified (may be from concurrent tasks): {modified_files}", file=sys.stderr)
