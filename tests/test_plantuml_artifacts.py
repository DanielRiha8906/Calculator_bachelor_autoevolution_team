import pytest
import os
from pathlib import Path


class TestPlantUMLArtifactExistence:
    """Test suite for PlantUML artifact file existence."""

    @pytest.fixture
    def artifacts_dir(self):
        """Fixture providing the artifacts directory path."""
        return Path(__file__).parent.parent / "artifacts"

    @pytest.mark.parametrize("filename", [
        "class_diagram_cli.puml",
        "activity_diagram_interactive_session.puml",
        "sequence_diagram_operation_execution.puml",
    ])
    def test_plantuml_files_exist(self, artifacts_dir, filename):
        """Test that all required PlantUML artifact files exist."""
        filepath = artifacts_dir / filename
        assert filepath.exists(), f"File {filename} does not exist at {filepath}"
        assert filepath.is_file(), f"{filename} exists but is not a regular file"


class TestPlantUMLStructureValidity:
    """Test suite for PlantUML structure validation."""

    @pytest.fixture
    def artifacts_dir(self):
        """Fixture providing the artifacts directory path."""
        return Path(__file__).parent.parent / "artifacts"

    @pytest.fixture
    def load_puml_content(self, artifacts_dir):
        """Fixture that loads PlantUML file content."""
        def _load(filename):
            filepath = artifacts_dir / filename
            with open(filepath, 'r') as f:
                return f.read()
        return _load

    @pytest.mark.parametrize("filename", [
        "class_diagram_cli.puml",
        "activity_diagram_interactive_session.puml",
        "sequence_diagram_operation_execution.puml",
    ])
    def test_plantuml_starts_with_startuml(self, load_puml_content, filename):
        """Test that each PlantUML file starts with @startuml."""
        content = load_puml_content(filename)
        assert "@startuml" in content, f"{filename} does not contain @startuml"
        # Check it appears near the beginning (first 100 chars)
        assert content.strip().startswith("@startuml"), \
            f"{filename} does not start with @startuml (after stripping whitespace)"

    @pytest.mark.parametrize("filename", [
        "class_diagram_cli.puml",
        "activity_diagram_interactive_session.puml",
        "sequence_diagram_operation_execution.puml",
    ])
    def test_plantuml_ends_with_enduml(self, load_puml_content, filename):
        """Test that each PlantUML file ends with @enduml."""
        content = load_puml_content(filename)
        assert "@enduml" in content, f"{filename} does not contain @enduml"
        # Check it appears near the end
        assert content.strip().endswith("@enduml"), \
            f"{filename} does not end with @enduml (after stripping whitespace)"

    @pytest.mark.parametrize("filename", [
        "class_diagram_cli.puml",
        "activity_diagram_interactive_session.puml",
        "sequence_diagram_operation_execution.puml",
    ])
    def test_plantuml_has_nontrivial_content(self, load_puml_content, filename):
        """Test that each PlantUML file has more than 2 lines of content."""
        content = load_puml_content(filename)
        lines = content.strip().split('\n')
        assert len(lines) > 2, \
            f"{filename} has {len(lines)} lines; expected more than 2"


class TestClassDiagramContent:
    """Test suite for class diagram content accuracy."""

    @pytest.fixture
    def class_diagram_content(self):
        """Fixture providing the class diagram file content."""
        filepath = Path(__file__).parent.parent / "artifacts" / "class_diagram_cli.puml"
        with open(filepath, 'r') as f:
            return f.read()

    def test_class_diagram_contains_all_calculator_methods(self, class_diagram_content):
        """Test that class diagram contains all 12 Calculator method names."""
        calculator_methods = [
            "add", "subtract", "multiply", "divide", "power", "factorial",
            "square", "cube", "square_root", "cube_root", "logarithm",
            "natural_logarithm"
        ]
        for method in calculator_methods:
            assert method in class_diagram_content, \
                f"Method '{method}' not found in class diagram"

    def test_class_diagram_contains_all_cli_functions(self, class_diagram_content):
        """Test that class diagram contains all 5 CLI function names."""
        cli_functions = [
            "get_operation_menu", "get_arity", "parse_float",
            "get_operands", "interactive_session"
        ]
        for func in cli_functions:
            assert func in class_diagram_content, \
                f"CLI function '{func}' not found in class diagram"


class TestActivityDiagramContent:
    """Test suite for activity diagram content accuracy."""

    @pytest.fixture
    def activity_diagram_content(self):
        """Fixture providing the activity diagram file content."""
        filepath = Path(__file__).parent.parent / "artifacts" / "activity_diagram_interactive_session.puml"
        with open(filepath, 'r') as f:
            return f.read()

    @pytest.mark.parametrize("keyword", [
        "start", "stop", "repeat", "if", "getattr"
    ])
    def test_activity_diagram_contains_flow_markers(self, activity_diagram_content, keyword):
        """Test that activity diagram contains key flow markers."""
        assert keyword in activity_diagram_content, \
            f"Flow marker '{keyword}' not found in activity diagram"

    @pytest.mark.parametrize("quit_keyword", ["quit", "exit"])
    def test_activity_diagram_contains_quit_path(self, activity_diagram_content, quit_keyword):
        """Test that activity diagram contains quit/exit keywords in quit path."""
        assert quit_keyword in activity_diagram_content, \
            f"Quit keyword '{quit_keyword}' not found in activity diagram"


class TestSequenceDiagramContent:
    """Test suite for sequence diagram content accuracy."""

    @pytest.fixture
    def sequence_diagram_content(self):
        """Fixture providing the sequence diagram file content."""
        filepath = Path(__file__).parent.parent / "artifacts" / "sequence_diagram_operation_execution.puml"
        with open(filepath, 'r') as f:
            return f.read()

    @pytest.mark.parametrize("participant", [
        "Calculator", "interactive_session", "get_operation_menu",
        "get_arity", "get_operands", "parse_float"
    ])
    def test_sequence_diagram_contains_key_participants(self, sequence_diagram_content, participant):
        """Test that sequence diagram contains key participants."""
        assert participant in sequence_diagram_content, \
            f"Participant '{participant}' not found in sequence diagram"

    @pytest.mark.parametrize("action", ["getattr", "Goodbye"])
    def test_sequence_diagram_contains_key_actions(self, sequence_diagram_content, action):
        """Test that sequence diagram contains key actions."""
        assert action in sequence_diagram_content, \
            f"Action '{action}' not found in sequence diagram"
