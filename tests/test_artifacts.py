"""
Tests for PlantUML documentation artifact files under artifacts/.

Validates structural correctness of each .puml file using only the Python
standard library — no external PlantUML runtime or third-party packages.
"""

import pathlib
import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ARTIFACTS_DIR = pathlib.Path(__file__).parent.parent / "artifacts"

CLASS_DIAGRAM = ARTIFACTS_DIR / "class_diagram.puml"
ACTIVITY_DIAGRAM = ARTIFACTS_DIR / "activity_diagram.puml"
SEQUENCE_DIAGRAM = ARTIFACTS_DIR / "sequence_diagram.puml"

ALL_DIAGRAMS = [CLASS_DIAGRAM, ACTIVITY_DIAGRAM, SEQUENCE_DIAGRAM]


def _non_empty_lines(path: pathlib.Path) -> list[str]:
    """Return the list of non-empty (stripped) lines from *path*."""
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _content(path: pathlib.Path) -> str:
    """Return the full file content as a single string."""
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Parametrised: structural invariants shared by every diagram
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("diagram_path", ALL_DIAGRAMS, ids=["class", "activity", "sequence"])
class TestAllDiagramsStructure:
    """Every .puml file must satisfy these baseline structural requirements."""

    def test_file_exists(self, diagram_path: pathlib.Path) -> None:
        assert diagram_path.exists(), f"Expected artifact not found: {diagram_path}"

    def test_file_is_regular_file(self, diagram_path: pathlib.Path) -> None:
        assert diagram_path.is_file(), f"Path exists but is not a regular file: {diagram_path}"

    def test_file_is_not_empty(self, diagram_path: pathlib.Path) -> None:
        assert diagram_path.stat().st_size > 0, f"File is empty: {diagram_path}"

    def test_first_non_empty_line_is_startuml(self, diagram_path: pathlib.Path) -> None:
        lines = _non_empty_lines(diagram_path)
        assert lines, "File has no non-empty lines"
        assert lines[0] == "@startuml", (
            f"First non-empty line must be '@startuml', got: {lines[0]!r}"
        )

    def test_last_non_empty_line_is_enduml(self, diagram_path: pathlib.Path) -> None:
        lines = _non_empty_lines(diagram_path)
        assert lines, "File has no non-empty lines"
        assert lines[-1] == "@enduml", (
            f"Last non-empty line must be '@enduml', got: {lines[-1]!r}"
        )

    def test_startuml_appears_exactly_once(self, diagram_path: pathlib.Path) -> None:
        content = _content(diagram_path)
        assert content.count("@startuml") == 1, (
            "@startuml must appear exactly once in the file"
        )

    def test_enduml_appears_exactly_once(self, diagram_path: pathlib.Path) -> None:
        content = _content(diagram_path)
        assert content.count("@enduml") == 1, (
            "@enduml must appear exactly once in the file"
        )

    def test_startuml_precedes_enduml(self, diagram_path: pathlib.Path) -> None:
        content = _content(diagram_path)
        start_pos = content.index("@startuml")
        end_pos = content.index("@enduml")
        assert start_pos < end_pos, "@startuml must come before @enduml"

    def test_file_uses_utf8_encoding(self, diagram_path: pathlib.Path) -> None:
        # If this raises UnicodeDecodeError the file is not valid UTF-8.
        try:
            diagram_path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            pytest.fail(f"File is not valid UTF-8: {exc}")


# ---------------------------------------------------------------------------
# class_diagram.puml — detailed content checks
# ---------------------------------------------------------------------------

class TestClassDiagram:
    """Content checks specific to artifacts/class_diagram.puml."""

    @pytest.fixture(scope="class")
    def content(self) -> str:
        return _content(CLASS_DIAGRAM)

    # --- Class declarations --------------------------------------------------

    def test_contains_class_calculator(self, content: str) -> None:
        assert "class Calculator" in content

    def test_contains_class_inputloop(self, content: str) -> None:
        assert "class InputLoop" in content

    def test_contains_class_main(self, content: str) -> None:
        assert "class Main" in content

    # --- All 12 method names -------------------------------------------------

    @pytest.mark.parametrize("method", [
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
    ])
    def test_calculator_method_present(self, content: str, method: str) -> None:
        assert method in content, f"Expected Calculator method '{method}' not found"

    # --- Relationship arrows --------------------------------------------------

    def test_inputloop_uses_calculator_arrow(self, content: str) -> None:
        # Arrow from InputLoop to Calculator with any label
        assert "InputLoop --> Calculator" in content, (
            "Expected 'InputLoop --> Calculator' relationship arrow"
        )

    def test_main_calls_inputloop_arrow(self, content: str) -> None:
        assert "Main --> InputLoop" in content, (
            "Expected 'Main --> InputLoop' relationship arrow"
        )

    # --- Sanity: no extra spurious @startuml/@enduml -------------------------

    def test_title_line_present(self, content: str) -> None:
        assert "title" in content, "Expected a 'title' directive in the class diagram"


# ---------------------------------------------------------------------------
# activity_diagram.puml — detailed content checks
# ---------------------------------------------------------------------------

class TestActivityDiagram:
    """Content checks specific to artifacts/activity_diagram.puml."""

    @pytest.fixture(scope="class")
    def content(self) -> str:
        return _content(ACTIVITY_DIAGRAM)

    def test_contains_start(self, content: str) -> None:
        assert "start" in content

    def test_contains_stop(self, content: str) -> None:
        assert "stop" in content

    def test_contains_if(self, content: str) -> None:
        assert "if" in content

    def test_contains_endif(self, content: str) -> None:
        assert "endif" in content

    def test_if_count_matches_endif_count(self, content: str) -> None:
        # Every opened 'if' block must be closed with 'endif'.
        # Count occurrences on their own as keywords (case-sensitive, PlantUML spec).
        lines = content.splitlines()
        if_count = sum(1 for line in lines if line.strip().startswith("if"))
        endif_count = sum(1 for line in lines if line.strip() == "endif")
        assert if_count == endif_count, (
            f"Mismatched if/endif: {if_count} 'if' blocks but {endif_count} 'endif' keywords"
        )

    def test_contains_else(self, content: str) -> None:
        assert "else" in content

    @pytest.mark.parametrize("label", [
        "print_menu",
        "get_operation",
        "Calculator",
        "dispatch",
    ])
    def test_activity_label_present(self, content: str, label: str) -> None:
        assert label in content, f"Expected activity label keyword '{label}' not found"

    def test_contains_exit_condition(self, content: str) -> None:
        assert "exit" in content.lower(), "Expected 'exit' condition referenced in activity diagram"

    def test_title_line_present(self, content: str) -> None:
        assert "title" in content


# ---------------------------------------------------------------------------
# sequence_diagram.puml — detailed content checks
# ---------------------------------------------------------------------------

class TestSequenceDiagram:
    """Content checks specific to artifacts/sequence_diagram.puml."""

    @pytest.fixture(scope="class")
    def content(self) -> str:
        return _content(SEQUENCE_DIAGRAM)

    @pytest.mark.parametrize("participant", [
        "participant User",
        "participant InputLoop",
        "participant Calculator",
    ])
    def test_participant_declared(self, content: str, participant: str) -> None:
        assert participant in content, f"Expected declaration '{participant}' not found"

    def test_contains_loop(self, content: str) -> None:
        assert "loop" in content

    def test_contains_alt(self, content: str) -> None:
        assert "alt" in content

    def test_loop_has_matching_end(self, content: str) -> None:
        lines = [line.strip() for line in content.splitlines()]
        loop_count = sum(1 for line in lines if line.startswith("loop"))
        end_count = sum(1 for line in lines if line == "end")
        assert loop_count <= end_count, (
            f"loop/end mismatch: {loop_count} 'loop' blocks but only {end_count} 'end' keywords"
        )

    def test_alt_has_matching_end(self, content: str) -> None:
        lines = [line.strip() for line in content.splitlines()]
        alt_count = sum(1 for line in lines if line.startswith("alt"))
        end_count = sum(1 for line in lines if line == "end")
        assert alt_count <= end_count, (
            f"alt/end mismatch: {alt_count} 'alt' blocks but only {end_count} 'end' keywords"
        )

    def test_user_to_inputloop_message_present(self, content: str) -> None:
        assert "User -> InputLoop" in content or "User --> InputLoop" in content, (
            "Expected a message arrow from User to InputLoop"
        )

    def test_inputloop_to_calculator_message_present(self, content: str) -> None:
        assert "InputLoop -> Calculator" in content or "InputLoop --> Calculator" in content, (
            "Expected a message arrow from InputLoop to Calculator"
        )

    def test_title_line_present(self, content: str) -> None:
        assert "title" in content

    def test_contains_run_loop_call(self, content: str) -> None:
        assert "run_loop" in content, "Expected 'run_loop' call in sequence diagram"

    def test_contains_exit_condition(self, content: str) -> None:
        assert "exit" in content.lower(), "Expected 'exit' referenced in sequence diagram"
