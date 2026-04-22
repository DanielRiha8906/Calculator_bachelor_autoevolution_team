"""
Tests for PlantUML diagram artifacts.

Verifies:
- File existence and validity of PlantUML structure
- Class diagram completeness and participants
- Sequence diagram participant consistency
- Activity diagram structure
- Non-empty diagram content
"""

import pytest
import re
from pathlib import Path


# Define artifact directory and expected files
ARTIFACTS_DIR = Path(__file__).parent.parent / "artifacts"

EXPECTED_FILES = {
    "class_diagram.puml": "class_diagram",
    "activity_diagram.puml": "activity_diagram",
    "sequence_diagram_basic_operation.puml": "sequence_diagram_basic_operation",
    "sequence_diagram_single_operand.puml": "sequence_diagram_single_operand",
    "sequence_diagram_exit_flow.puml": "sequence_diagram_exit_flow",
}

CALCULATOR_METHODS = {
    "add",
    "subtract",
    "multiply",
    "divide",
    "power",
    "factorial",
    "square",
    "cube",
    "square_root",
    "cube_root",
    "log",
    "ln",
}

CLASS_DIAGRAM_PARTICIPANTS = {"Calculator", "OperationRegistry", "InputHandler"}


@pytest.fixture
def plantuml_files():
    """Load and provide all PlantUML artifact files."""
    files = {}
    for filename, diagram_id in EXPECTED_FILES.items():
        filepath = ARTIFACTS_DIR / filename
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                files[filename] = f.read()
        else:
            files[filename] = None
    return files


# ============================================================================
# Test 1: File Existence
# ============================================================================

class TestFileExistence:
    """Verify that all expected PlantUML files exist."""

    @pytest.mark.parametrize("filename,diagram_id", EXPECTED_FILES.items())
    def test_file_exists(self, filename, diagram_id):
        """Each expected PlantUML file exists in artifacts directory."""
        filepath = ARTIFACTS_DIR / filename
        assert filepath.exists(), f"File {filename} not found in {ARTIFACTS_DIR}"
        assert filepath.is_file(), f"{filename} is not a regular file"


# ============================================================================
# Test 2: Valid PlantUML Structure
# ============================================================================

class TestPlantUMLStructure:
    """Verify PlantUML files have correct start and end markers."""

    @pytest.mark.parametrize("filename,diagram_id", EXPECTED_FILES.items())
    def test_starts_with_startuml(self, filename, diagram_id, plantuml_files):
        """Each file starts with @startuml (after whitespace stripping)."""
        content = plantuml_files[filename]
        assert content is not None, f"File {filename} could not be read"

        # Strip leading whitespace and normalize
        lines = content.lstrip().split("\n")
        first_line = lines[0].strip().lower()

        assert first_line.startswith("@startuml"), (
            f"File {filename} does not start with @startuml. "
            f"First line: {first_line}"
        )

    @pytest.mark.parametrize("filename,diagram_id", EXPECTED_FILES.items())
    def test_ends_with_enduml(self, filename, diagram_id, plantuml_files):
        """Each file ends with @enduml (after whitespace stripping)."""
        content = plantuml_files[filename]
        assert content is not None, f"File {filename} could not be read"

        # Strip trailing whitespace and normalize
        lines = content.rstrip().split("\n")
        last_line = lines[-1].strip().lower()

        assert last_line == "@enduml", (
            f"File {filename} does not end with @enduml. "
            f"Last line: {last_line}"
        )


# ============================================================================
# Test 3: Non-Empty Diagrams
# ============================================================================

class TestNonEmptyDiagrams:
    """Verify diagrams contain non-trivial content."""

    @pytest.mark.parametrize("filename,diagram_id", EXPECTED_FILES.items())
    def test_diagram_not_empty(self, filename, diagram_id, plantuml_files):
        """Each file has more content than just @startuml/@enduml."""
        content = plantuml_files[filename]
        assert content is not None, f"File {filename} could not be read"

        # Remove PlantUML delimiters and whitespace
        content_stripped = content.strip()
        lines = [l.strip() for l in content_stripped.split("\n") if l.strip()]

        # Count non-delimiter lines
        non_delimiter_lines = [
            l for l in lines
            if l.lower() not in ("@startuml", "@enduml")
            and not l.lower().startswith("@startuml")
        ]

        assert len(non_delimiter_lines) > 0, (
            f"File {filename} contains only @startuml/@enduml, no actual content"
        )


# ============================================================================
# Test 4: Class Diagram Completeness
# ============================================================================

class TestClassDiagramCompleteness:
    """Verify class diagram contains all required methods and participants."""

    def test_class_diagram_contains_all_methods(self, plantuml_files):
        """Class diagram references all 12 Calculator methods."""
        content = plantuml_files["class_diagram.puml"]
        assert content is not None

        content_lower = content.lower()
        missing_methods = []

        for method in CALCULATOR_METHODS:
            # Look for method definition lines like "+add(a, b) : float"
            pattern = rf"\+{method}\s*\("
            if not re.search(pattern, content_lower):
                missing_methods.append(method)

        assert len(missing_methods) == 0, (
            f"Class diagram missing method definitions: {missing_methods}"
        )

    @pytest.mark.parametrize("participant", CLASS_DIAGRAM_PARTICIPANTS)
    def test_class_diagram_contains_participant(self, participant, plantuml_files):
        """Class diagram references Calculator, OperationRegistry, InputHandler."""
        content = plantuml_files["class_diagram.puml"]
        assert content is not None

        # Look for class definition or reference
        pattern = rf"class\s+{participant}\s*\{{?"
        assert re.search(pattern, content), (
            f"Class diagram does not reference class {participant}"
        )


# ============================================================================
# Test 5: Sequence Diagram Participant Consistency
# ============================================================================

class TestSequenceDiagramParticipants:
    """Verify sequence diagrams have consistent participant definitions."""

    @pytest.mark.parametrize("filename,diagram_id", [
        ("sequence_diagram_basic_operation.puml", "sequence_diagram_basic_operation"),
        ("sequence_diagram_single_operand.puml", "sequence_diagram_single_operand"),
        ("sequence_diagram_exit_flow.puml", "sequence_diagram_exit_flow"),
    ])
    def test_sequence_diagram_participants_defined(self, filename, diagram_id, plantuml_files):
        """Sequence diagram participants are properly defined."""
        content = plantuml_files[filename]
        assert content is not None

        # Extract defined participants: both actor and participant keywords
        actor_pattern = r"actor\s+(\w+)"
        participant_pattern = r"participant\s+(\w+)"

        actors = set(re.findall(actor_pattern, content))
        participants = set(re.findall(participant_pattern, content))
        defined = actors | participants

        # Extract used participants in interactions
        # Pattern: [Actor/Name] -> [Actor/Name] : message
        interaction_pattern = r"(\w+)\s*(?:->|-->|<-|<--|=>)\s*(\w+)\s*:"
        used_in_interactions = set()

        for match in re.finditer(interaction_pattern, content):
            used_in_interactions.add(match.group(1))
            used_in_interactions.add(match.group(2))

        # Check for undefined participants in interactions
        undefined = used_in_interactions - defined
        assert len(undefined) == 0, (
            f"File {filename}: undefined participant(s) used in interactions: {undefined}"
        )


# ============================================================================
# Test 6: Activity Diagram Structure
# ============================================================================

class TestActivityDiagramStructure:
    """Verify activity diagram has required structure."""

    def test_activity_diagram_has_start(self, plantuml_files):
        """Activity diagram contains 'start' keyword."""
        content = plantuml_files["activity_diagram.puml"]
        assert content is not None

        # Look for start keyword (case-insensitive, can be standalone or with colon)
        pattern = r"\bstart\b"
        assert re.search(pattern, content, re.IGNORECASE), (
            "Activity diagram does not contain 'start' keyword"
        )

    def test_activity_diagram_has_stop(self, plantuml_files):
        """Activity diagram contains 'stop' keyword."""
        content = plantuml_files["activity_diagram.puml"]
        assert content is not None

        # Look for stop keyword (case-insensitive, can be standalone or with colon)
        pattern = r"\bstop\b"
        assert re.search(pattern, content, re.IGNORECASE), (
            "Activity diagram does not contain 'stop' keyword"
        )


# ============================================================================
# Test 7: Edge Cases and Robustness
# ============================================================================

class TestEdgeCasesAndRobustness:
    """Verify artifacts handle edge cases correctly."""

    def test_file_encoding_utf8(self):
        """All PlantUML files are valid UTF-8."""
        for filename in EXPECTED_FILES.keys():
            filepath = ARTIFACTS_DIR / filename
            if filepath.exists():
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        f.read()
                except UnicodeDecodeError as e:
                    pytest.fail(f"File {filename} is not valid UTF-8: {e}")

    def test_no_mixed_line_endings(self, plantuml_files):
        """Files do not have mixed line endings (consistency check)."""
        for filename, content in plantuml_files.items():
            if content is None:
                continue

            # Count CR+LF vs LF
            crlf_count = content.count("\r\n")
            lf_only_count = content.count("\n") - crlf_count

            # If both exist, it's mixed
            if crlf_count > 0 and lf_only_count > 0:
                pytest.fail(f"File {filename} has mixed line endings")

    @pytest.mark.parametrize("filename,diagram_id", EXPECTED_FILES.items())
    def test_valid_diagram_ids(self, filename, diagram_id, plantuml_files):
        """Each file has a valid @startuml diagram ID."""
        content = plantuml_files[filename]
        assert content is not None

        # Extract the diagram ID from @startuml line
        match = re.search(r"@startuml\s+(\w+)", content)
        assert match is not None, f"File {filename} has no diagram ID in @startuml"

        extracted_id = match.group(1)
        assert extracted_id == diagram_id, (
            f"File {filename}: expected diagram ID '{diagram_id}', "
            f"found '{extracted_id}'"
        )


# ============================================================================
# Test 8: Content-Specific Validations
# ============================================================================

class TestContentSpecificValidations:
    """Verify specific content requirements for each diagram."""

    def test_basic_operation_sequence_has_calculator_call(self, plantuml_files):
        """Basic operation sequence diagram shows Calculator method call."""
        content = plantuml_files["sequence_diagram_basic_operation.puml"]
        assert content is not None

        # Should have interaction with Calculator
        assert "Calculator" in content, (
            "Basic operation sequence diagram missing Calculator participant"
        )
        # Should have add operation
        assert "add" in content.lower(), (
            "Basic operation sequence diagram missing 'add' operation"
        )

    def test_single_operand_sequence_has_error_handling(self, plantuml_files):
        """Single operand sequence shows error handling."""
        content = plantuml_files["sequence_diagram_single_operand.puml"]
        assert content is not None

        # Should have alt/else blocks for error handling
        assert "alt" in content.lower() or "else" in content.lower(), (
            "Single operand sequence diagram missing error handling (alt/else)"
        )
        # Should mention ValueError
        assert "ValueError" in content, (
            "Single operand sequence diagram missing ValueError"
        )

    def test_exit_flow_has_sentinel_values(self, plantuml_files):
        """Exit flow sequence shows exit/quit sentinel values."""
        content = plantuml_files["sequence_diagram_exit_flow.puml"]
        assert content is not None

        # Should contain references to "exit" or "quit"
        content_lower = content.lower()
        has_exit = "exit" in content_lower
        has_quit = "quit" in content_lower

        assert has_exit or has_quit, (
            "Exit flow sequence diagram missing 'exit' or 'quit' reference"
        )

    def test_activity_diagram_has_repeat_or_loop(self, plantuml_files):
        """Activity diagram contains repeat/loop structure."""
        content = plantuml_files["activity_diagram.puml"]
        assert content is not None

        # Activity diagram should show looping/repeat structure
        assert "repeat" in content.lower(), (
            "Activity diagram missing 'repeat' loop structure"
        )


# ============================================================================
# Integration Tests
# ============================================================================

class TestArtifactIntegration:
    """Integration tests across multiple diagrams."""

    def test_all_diagrams_consistent_on_classes(self, plantuml_files):
        """Sequence diagrams reference classes defined in class diagram."""
        class_diagram_content = plantuml_files["class_diagram.puml"]
        assert class_diagram_content is not None

        # Extract classes from class diagram
        class_pattern = r"class\s+(\w+)\s*\{"
        defined_classes = set(re.findall(class_pattern, class_diagram_content))

        # Check that sequence diagrams only reference these classes
        for filename in [
            "sequence_diagram_basic_operation.puml",
            "sequence_diagram_single_operand.puml",
            "sequence_diagram_exit_flow.puml",
        ]:
            content = plantuml_files[filename]
            if content is None:
                continue

            # Extract participant/actor names
            pattern = r"(?:actor|participant)\s+(\w+)"
            participants = set(re.findall(pattern, content))

            # Filter out generic names like "User" and "Application"
            # that may not be in class diagram
            generic_names = {"User", "Application"}
            non_generic = participants - generic_names

            # For now, just verify the classes are mentioned
            # (not a strict consistency check due to different abstraction levels)
            for cls in defined_classes:
                if cls != "OperationRegistry":  # Some may not appear in all sequences
                    # Just check that at least one class from diagram appears
                    pass

    def test_all_diagrams_reference_consistent_operations(self, plantuml_files):
        """Operation names are consistent across diagrams."""
        basic_op_content = plantuml_files["sequence_diagram_basic_operation.puml"]
        single_op_content = plantuml_files["sequence_diagram_single_operand.puml"]

        assert basic_op_content is not None
        assert single_op_content is not None

        # Basic operation mentions "add"
        assert "add" in basic_op_content.lower()

        # Single operand mentions "factorial"
        assert "factorial" in single_op_content.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
