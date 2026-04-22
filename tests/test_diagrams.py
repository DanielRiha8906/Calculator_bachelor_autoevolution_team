"""test_diagrams.py — tests for PlantUML diagram syntax and content validation.

Tests verify that:
- All diagram files exist in artifacts/
- Each diagram has valid PlantUML syntax (proper @startuml/@enduml delimiters)
- Diagram content matches expected structure (class names, participants, keywords)
- No diagram files are empty
"""

import pytest
import re
from pathlib import Path


class TestDiagramFilesExist:
    """Tests for existence of required diagram files."""

    @pytest.fixture
    def artifact_dir(self):
        """Return the path to the artifacts directory."""
        return Path(__file__).parent.parent / "artifacts"

    def test_all_diagram_files_exist(self, artifact_dir):
        """Test that all three new diagram files exist in artifacts/."""
        required_files = [
            "calculator_class_diagram.puml",
            "calculator_repl_activity.puml",
            "calculator_evaluation_sequence.puml",
        ]

        for filename in required_files:
            file_path = artifact_dir / filename
            assert file_path.exists(), f"Required diagram file '{filename}' not found in {artifact_dir}"


class TestDiagramFilesNotEmpty:
    """Edge case tests for empty diagram files."""

    @pytest.fixture
    def artifact_dir(self):
        """Return the path to the artifacts directory."""
        return Path(__file__).parent.parent / "artifacts"

    def test_diagram_files_not_empty(self, artifact_dir):
        """Test that no diagram file is empty."""
        diagram_files = [
            "calculator_class_diagram.puml",
            "calculator_repl_activity.puml",
            "calculator_evaluation_sequence.puml",
        ]

        for filename in diagram_files:
            file_path = artifact_dir / filename
            content = file_path.read_text(encoding="utf-8")
            assert len(content.strip()) > 0, f"Diagram file '{filename}' is empty"


class TestClassDiagramSyntax:
    """Tests for class diagram syntax and content."""

    @pytest.fixture
    def artifact_dir(self):
        """Return the path to the artifacts directory."""
        return Path(__file__).parent.parent / "artifacts"

    @pytest.fixture
    def class_diagram_content(self, artifact_dir):
        """Return the content of the class diagram file."""
        file_path = artifact_dir / "calculator_class_diagram.puml"
        return file_path.read_text(encoding="utf-8")

    def test_class_diagram_starts_with_startuml(self, class_diagram_content):
        """Test that class diagram starts with @startuml."""
        assert class_diagram_content.strip().startswith("@startuml"), \
            "Class diagram must start with @startuml"

    def test_class_diagram_ends_with_enduml(self, class_diagram_content):
        """Test that class diagram ends with @enduml."""
        assert class_diagram_content.strip().endswith("@enduml"), \
            "Class diagram must end with @enduml"

    def test_class_diagram_contains_calculator_class(self, class_diagram_content):
        """Test that class diagram contains Calculator class definition."""
        assert "class Calculator" in class_diagram_content, \
            "Class diagram must contain 'class Calculator'"

    def test_class_diagram_contains_input_validator_class(self, class_diagram_content):
        """Test that class diagram contains InputValidator class."""
        assert "class InputValidator" in class_diagram_content, \
            "Class diagram must contain 'class InputValidator'"

    def test_class_diagram_contains_expression_parser_class(self, class_diagram_content):
        """Test that class diagram contains ExpressionParser class."""
        assert "class ExpressionParser" in class_diagram_content, \
            "Class diagram must contain 'class ExpressionParser'"

    def test_class_diagram_contains_calculator_repl_class(self, class_diagram_content):
        """Test that class diagram contains CalculatorREPL class."""
        assert "class CalculatorREPL" in class_diagram_content, \
            "Class diagram must contain 'class CalculatorREPL'"

    def test_class_diagram_contains_main_class(self, class_diagram_content):
        """Test that class diagram contains Main class."""
        assert "class Main" in class_diagram_content, \
            "Class diagram must contain 'class Main'"

    @pytest.mark.parametrize("method_name", [
        "add", "subtract", "multiply", "divide", "factorial",
        "square", "cube", "square_root", "cube_root",
        "power", "natural_log", "log_base_10"
    ])
    def test_class_diagram_contains_calculator_methods(self, class_diagram_content, method_name):
        """Test that class diagram includes all Calculator methods."""
        assert f"+ {method_name}(" in class_diagram_content, \
            f"Class diagram must contain Calculator method '{method_name}'"

    def test_class_diagram_contains_composition_relationships(self, class_diagram_content):
        """Test that class diagram contains composition relationships from CalculatorREPL."""
        # CalculatorREPL should use Calculator, ExpressionParser, and InputValidator
        relationships = [
            "CalculatorREPL *-- Calculator",
            "CalculatorREPL *-- ExpressionParser",
            "CalculatorREPL *-- InputValidator",
        ]
        for relationship in relationships:
            assert relationship in class_diagram_content, \
                f"Class diagram must contain composition relationship: {relationship}"

    def test_class_diagram_contains_dependency_from_main(self, class_diagram_content):
        """Test that class diagram shows Main depends on CalculatorREPL."""
        assert "Main ..> CalculatorREPL" in class_diagram_content, \
            "Class diagram must show Main dependency on CalculatorREPL"


class TestActivityDiagramSyntax:
    """Tests for activity diagram syntax and content."""

    @pytest.fixture
    def artifact_dir(self):
        """Return the path to the artifacts directory."""
        return Path(__file__).parent.parent / "artifacts"

    @pytest.fixture
    def activity_diagram_content(self, artifact_dir):
        """Return the content of the activity diagram file."""
        file_path = artifact_dir / "calculator_repl_activity.puml"
        return file_path.read_text(encoding="utf-8")

    def test_activity_diagram_starts_with_startuml(self, activity_diagram_content):
        """Test that activity diagram starts with @startuml."""
        assert activity_diagram_content.strip().startswith("@startuml"), \
            "Activity diagram must start with @startuml"

    def test_activity_diagram_ends_with_enduml(self, activity_diagram_content):
        """Test that activity diagram ends with @enduml."""
        assert activity_diagram_content.strip().endswith("@enduml"), \
            "Activity diagram must end with @enduml"

    def test_activity_diagram_contains_start(self, activity_diagram_content):
        """Test that activity diagram contains start node."""
        assert re.search(r'\bstart\b', activity_diagram_content), \
            "Activity diagram must contain 'start' node"

    def test_activity_diagram_contains_stop(self, activity_diagram_content):
        """Test that activity diagram contains stop nodes."""
        assert activity_diagram_content.count("stop") >= 2, \
            "Activity diagram must contain at least two 'stop' nodes for different exit paths"

    def test_activity_diagram_contains_decision_nodes(self, activity_diagram_content):
        """Test that activity diagram contains decision nodes (if statements)."""
        # Should have multiple 'if' statements for branching
        if_count = activity_diagram_content.count("if (")
        assert if_count >= 4, \
            f"Activity diagram should have at least 4 decision nodes, found {if_count}"

    @pytest.mark.parametrize("keyword", [
        "empty input",
        "exit / quit command",
        "parse error",
        "validation error",
        "math / type error"
    ])
    def test_activity_diagram_contains_decision_branches(self, activity_diagram_content, keyword):
        """Test that activity diagram includes all major decision branches."""
        assert keyword in activity_diagram_content.lower(), \
            f"Activity diagram must include decision for '{keyword}'"

    def test_activity_diagram_contains_repeat_loop(self, activity_diagram_content):
        """Test that activity diagram contains repeat loop structure."""
        assert "repeat" in activity_diagram_content, \
            "Activity diagram must contain 'repeat' loop for REPL"

    def test_activity_diagram_contains_expression_parser_call(self, activity_diagram_content):
        """Test that activity diagram references ExpressionParser."""
        assert "ExpressionParser.parse" in activity_diagram_content, \
            "Activity diagram must reference ExpressionParser.parse()"

    def test_activity_diagram_contains_input_validator_call(self, activity_diagram_content):
        """Test that activity diagram references InputValidator."""
        assert "InputValidator.validate" in activity_diagram_content, \
            "Activity diagram must reference InputValidator.validate()"

    def test_activity_diagram_contains_calculator_dispatch(self, activity_diagram_content):
        """Test that activity diagram shows dispatch to Calculator."""
        assert "Calculator method" in activity_diagram_content or "Dispatch to Calculator" in activity_diagram_content, \
            "Activity diagram must show dispatch to Calculator methods"


class TestSequenceDiagramSyntax:
    """Tests for sequence diagram syntax and content."""

    @pytest.fixture
    def artifact_dir(self):
        """Return the path to the artifacts directory."""
        return Path(__file__).parent.parent / "artifacts"

    @pytest.fixture
    def sequence_diagram_content(self, artifact_dir):
        """Return the content of the sequence diagram file."""
        file_path = artifact_dir / "calculator_evaluation_sequence.puml"
        return file_path.read_text(encoding="utf-8")

    def test_sequence_diagram_starts_with_startuml(self, sequence_diagram_content):
        """Test that sequence diagram starts with @startuml."""
        assert sequence_diagram_content.strip().startswith("@startuml"), \
            "Sequence diagram must start with @startuml"

    def test_sequence_diagram_ends_with_enduml(self, sequence_diagram_content):
        """Test that sequence diagram ends with @enduml."""
        assert sequence_diagram_content.strip().endswith("@enduml"), \
            "Sequence diagram must end with @enduml"

    @pytest.mark.parametrize("participant", [
        "User",
        "CalculatorREPL",
        "ExpressionParser",
        "InputValidator",
        "Calculator"
    ])
    def test_sequence_diagram_contains_participants(self, sequence_diagram_content, participant):
        """Test that sequence diagram includes all five main participants."""
        assert participant in sequence_diagram_content, \
            f"Sequence diagram must include participant '{participant}'"

    def test_sequence_diagram_contains_parse_call(self, sequence_diagram_content):
        """Test that sequence diagram shows ExpressionParser.parse() call."""
        assert "parse(" in sequence_diagram_content, \
            "Sequence diagram must show parse() call"

    def test_sequence_diagram_contains_validate_call(self, sequence_diagram_content):
        """Test that sequence diagram shows InputValidator.validate() call."""
        assert "validate(" in sequence_diagram_content, \
            "Sequence diagram must show validate() call"

    def test_sequence_diagram_contains_calculator_operation_call(self, sequence_diagram_content):
        """Test that sequence diagram shows Calculator operation calls."""
        # Should show operation calls like add(*operands)
        assert re.search(r'\(e\.g\.\s+\w+\(', sequence_diagram_content), \
            "Sequence diagram must show Calculator operation calls (e.g. add(5, 3))"

    def test_sequence_diagram_contains_coerce_numeric_selfcall(self, sequence_diagram_content):
        """Test that sequence diagram shows _coerce_numeric self-call on ExpressionParser."""
        assert "_coerce_numeric" in sequence_diagram_content, \
            "Sequence diagram must show ExpressionParser._coerce_numeric self-call"

    def test_sequence_diagram_contains_alt_blocks(self, sequence_diagram_content):
        """Test that sequence diagram contains alt blocks for error handling."""
        alt_count = sequence_diagram_content.count("alt ")
        assert alt_count >= 2, \
            f"Sequence diagram should have at least 2 'alt' blocks for error paths, found {alt_count}"

    def test_sequence_diagram_contains_validation_error_path(self, sequence_diagram_content):
        """Test that sequence diagram includes validation error alt path."""
        assert "validation fails" in sequence_diagram_content, \
            "Sequence diagram must include 'validation fails' alt path"

    def test_sequence_diagram_contains_math_error_path(self, sequence_diagram_content):
        """Test that sequence diagram includes math/type error alt path."""
        assert "math / type error" in sequence_diagram_content or "error" in sequence_diagram_content.lower(), \
            "Sequence diagram must include math/type error alt path"

    def test_sequence_diagram_error_raises_exceptions(self, sequence_diagram_content):
        """Test that sequence diagram shows exceptions being raised."""
        exceptions = ["ValueError", "ZeroDivisionError", "TypeError"]
        found_exceptions = sum(1 for exc in exceptions if exc in sequence_diagram_content)
        assert found_exceptions >= 1, \
            "Sequence diagram must show at least one exception type being raised"

    def test_sequence_diagram_contains_result_message(self, sequence_diagram_content):
        """Test that sequence diagram shows result being returned to user."""
        assert "Result:" in sequence_diagram_content, \
            "Sequence diagram must show result being returned to user"


class TestPlantUMLDiagramStructure:
    """Integration tests for overall diagram structure and consistency."""

    @pytest.fixture
    def artifact_dir(self):
        """Return the path to the artifacts directory."""
        return Path(__file__).parent.parent / "artifacts"

    def test_all_diagrams_have_valid_startuml_enduml_pair(self, artifact_dir):
        """Test that all three diagrams have matching @startuml/@enduml pairs."""
        diagram_files = [
            "calculator_class_diagram.puml",
            "calculator_repl_activity.puml",
            "calculator_evaluation_sequence.puml",
        ]

        for filename in diagram_files:
            file_path = artifact_dir / filename
            content = file_path.read_text(encoding="utf-8")

            startuml_count = content.count("@startuml")
            enduml_count = content.count("@enduml")

            assert startuml_count == 1, \
                f"{filename}: expected 1 @startuml, found {startuml_count}"
            assert enduml_count == 1, \
                f"{filename}: expected 1 @enduml, found {enduml_count}"

            # Verify @startuml comes before @enduml
            startuml_pos = content.find("@startuml")
            enduml_pos = content.find("@enduml")
            assert startuml_pos < enduml_pos, \
                f"{filename}: @startuml must come before @enduml"

    def test_no_diagram_file_has_syntax_errors_indicators(self, artifact_dir):
        """Test that diagram files do not contain common PlantUML error patterns."""
        diagram_files = [
            "calculator_class_diagram.puml",
            "calculator_repl_activity.puml",
            "calculator_evaluation_sequence.puml",
        ]

        # Common error patterns that indicate malformed PlantUML
        error_patterns = [
            r'@startuml.*@startuml',  # Duplicate @startuml
            r'@enduml.*@enduml',      # Duplicate @enduml
        ]

        for filename in diagram_files:
            file_path = artifact_dir / filename
            content = file_path.read_text(encoding="utf-8")

            for pattern in error_patterns:
                assert not re.search(pattern, content, re.DOTALL), \
                    f"{filename}: contains malformed pattern matching '{pattern}'"

    def test_class_diagram_references_match_other_diagrams(self, artifact_dir):
        """Test that class names used in diagrams are consistent across all files."""
        class_diagram_path = artifact_dir / "calculator_class_diagram.puml"
        activity_diagram_path = artifact_dir / "calculator_repl_activity.puml"
        sequence_diagram_path = artifact_dir / "calculator_evaluation_sequence.puml"

        class_content = class_diagram_path.read_text(encoding="utf-8")
        activity_content = activity_diagram_path.read_text(encoding="utf-8")
        sequence_content = sequence_diagram_path.read_text(encoding="utf-8")

        # Key classes that should be referenced across diagrams
        key_classes = ["CalculatorREPL", "Calculator", "ExpressionParser", "InputValidator"]

        for cls in key_classes:
            assert cls in class_content, f"Class '{cls}' not found in class diagram"
            # These should be mentioned (may not be explicit class names in activity/sequence)
            # but we can check that they're at least referenced
            full_diagram_content = activity_content + sequence_content
            assert cls in full_diagram_content, \
                f"Class '{cls}' not referenced in activity or sequence diagrams"
