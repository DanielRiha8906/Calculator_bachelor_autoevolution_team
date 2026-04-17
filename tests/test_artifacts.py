"""
Tests for PlantUML documentation artifacts.

Validates that the three diagram files (class_diagram.puml,
activity_diagram.puml, sequence_diagram.puml) exist, are well-formed
PlantUML documents, and reference identifiers that actually exist in src/.
"""

import pathlib
import pytest

ARTIFACTS_DIR = pathlib.Path(__file__).parent.parent / "artifacts"

CLASS_DIAGRAM = ARTIFACTS_DIR / "class_diagram.puml"
ACTIVITY_DIAGRAM = ARTIFACTS_DIR / "activity_diagram.puml"
SEQUENCE_DIAGRAM = ARTIFACTS_DIR / "sequence_diagram.puml"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# class_diagram.puml
# ---------------------------------------------------------------------------

class TestClassDiagram:

    def test_file_exists(self):
        assert CLASS_DIAGRAM.exists(), f"Expected {CLASS_DIAGRAM} to exist"

    def test_file_is_not_empty(self):
        assert CLASS_DIAGRAM.stat().st_size > 0, "class_diagram.puml must not be empty"

    def test_starts_with_startuml(self):
        content = _read(CLASS_DIAGRAM)
        assert content.lstrip().startswith("@startuml"), (
            "class_diagram.puml must start with @startuml"
        )

    def test_ends_with_enduml(self):
        content = _read(CLASS_DIAGRAM)
        assert content.rstrip().endswith("@enduml"), (
            "class_diagram.puml must end with @enduml"
        )

    def test_contains_calculator_class(self):
        content = _read(CLASS_DIAGRAM)
        assert "class Calculator" in content, (
            "class_diagram.puml must declare the Calculator class"
        )

    def test_contains_input_handler_class(self):
        content = _read(CLASS_DIAGRAM)
        assert "class InputHandler" in content, (
            "class_diagram.puml must declare the InputHandler class"
        )

    # --- Calculator methods that exist in src/calculator.py ---

    @pytest.mark.parametrize("method", [
        "add", "subtract", "multiply", "divide",
        "factorial", "square", "cube", "square_root",
        "cube_root", "log10", "ln", "power",
    ])
    def test_calculator_method_documented(self, method):
        content = _read(CLASS_DIAGRAM)
        assert method in content, (
            f"class_diagram.puml must document Calculator.{method}"
        )

    # --- InputHandler members that exist in src/input_handler.py ---

    @pytest.mark.parametrize("member", [
        "run", "_show_menu", "_prompt_operands", "_dispatch",
        "_calculator", "_input_fn",
    ])
    def test_input_handler_member_documented(self, member):
        content = _read(CLASS_DIAGRAM)
        assert member in content, (
            f"class_diagram.puml must document InputHandler member '{member}'"
        )

    def test_run_session_free_function_referenced(self):
        content = _read(CLASS_DIAGRAM)
        assert "run_session" in content, (
            "class_diagram.puml must reference the run_session free function"
        )

    def test_operations_constant_referenced(self):
        content = _read(CLASS_DIAGRAM)
        assert "OPERATIONS" in content, (
            "class_diagram.puml must reference the OPERATIONS module-level constant"
        )

    def test_relationship_between_handler_and_calculator(self):
        content = _read(CLASS_DIAGRAM)
        # Either an association or dependency arrow must link the two classes
        assert "InputHandler" in content and "Calculator" in content, (
            "class_diagram.puml must include both InputHandler and Calculator"
        )
        assert "-->" in content or ".." in content, (
            "class_diagram.puml must include at least one relationship arrow"
        )

    def test_source_module_paths_mentioned(self):
        content = _read(CLASS_DIAGRAM)
        assert "src/input_handler.py" in content, (
            "class_diagram.puml should reference the source module path for InputHandler"
        )


# ---------------------------------------------------------------------------
# activity_diagram.puml
# ---------------------------------------------------------------------------

class TestActivityDiagram:

    def test_file_exists(self):
        assert ACTIVITY_DIAGRAM.exists(), f"Expected {ACTIVITY_DIAGRAM} to exist"

    def test_file_is_not_empty(self):
        assert ACTIVITY_DIAGRAM.stat().st_size > 0, "activity_diagram.puml must not be empty"

    def test_starts_with_startuml(self):
        content = _read(ACTIVITY_DIAGRAM)
        assert content.lstrip().startswith("@startuml"), (
            "activity_diagram.puml must start with @startuml"
        )

    def test_ends_with_enduml(self):
        content = _read(ACTIVITY_DIAGRAM)
        assert content.rstrip().endswith("@enduml"), (
            "activity_diagram.puml must end with @enduml"
        )

    def test_has_start_node(self):
        content = _read(ACTIVITY_DIAGRAM)
        assert "start" in content, (
            "activity_diagram.puml must contain a 'start' node"
        )

    def test_has_stop_node(self):
        content = _read(ACTIVITY_DIAGRAM)
        assert "stop" in content, (
            "activity_diagram.puml must contain a 'stop' node"
        )

    def test_exit_branch_present(self):
        content = _read(ACTIVITY_DIAGRAM)
        # The exit branch is triggered by 'exit' or 'quit' input
        assert "exit" in content or "quit" in content, (
            "activity_diagram.puml must document the exit/quit branch"
        )

    def test_show_menu_step_present(self):
        content = _read(ACTIVITY_DIAGRAM)
        assert "_show_menu" in content or "show_menu" in content, (
            "activity_diagram.puml must reference the _show_menu step"
        )

    def test_prompt_operands_step_present(self):
        content = _read(ACTIVITY_DIAGRAM)
        assert "_prompt_operands" in content or "prompt_operands" in content, (
            "activity_diagram.puml must reference the _prompt_operands step"
        )

    def test_dispatch_step_present(self):
        content = _read(ACTIVITY_DIAGRAM)
        assert "_dispatch" in content or "dispatch" in content, (
            "activity_diagram.puml must reference the _dispatch step"
        )

    def test_error_handling_zero_division(self):
        content = _read(ACTIVITY_DIAGRAM)
        assert "ZeroDivisionError" in content or "zero" in content.lower(), (
            "activity_diagram.puml must document division-by-zero error handling"
        )

    def test_error_handling_value_error(self):
        content = _read(ACTIVITY_DIAGRAM)
        assert "ValueError" in content, (
            "activity_diagram.puml must document ValueError handling"
        )

    def test_operations_registry_referenced(self):
        content = _read(ACTIVITY_DIAGRAM)
        assert "OPERATIONS" in content, (
            "activity_diagram.puml must reference the OPERATIONS registry"
        )

    def test_loop_structure_present(self):
        content = _read(ACTIVITY_DIAGRAM)
        # PlantUML activity loops use 'repeat'/'repeat while' or 'while'
        assert "repeat" in content or "while" in content, (
            "activity_diagram.puml must contain a loop construct (repeat/while)"
        )

    def test_has_conditional_branch(self):
        content = _read(ACTIVITY_DIAGRAM)
        assert "if" in content, (
            "activity_diagram.puml must contain at least one conditional (if) branch"
        )


# ---------------------------------------------------------------------------
# sequence_diagram.puml
# ---------------------------------------------------------------------------

class TestSequenceDiagram:

    def test_file_exists(self):
        assert SEQUENCE_DIAGRAM.exists(), f"Expected {SEQUENCE_DIAGRAM} to exist"

    def test_file_is_not_empty(self):
        assert SEQUENCE_DIAGRAM.stat().st_size > 0, "sequence_diagram.puml must not be empty"

    def test_starts_with_startuml(self):
        content = _read(SEQUENCE_DIAGRAM)
        assert content.lstrip().startswith("@startuml"), (
            "sequence_diagram.puml must start with @startuml"
        )

    def test_ends_with_enduml(self):
        content = _read(SEQUENCE_DIAGRAM)
        assert content.rstrip().endswith("@enduml"), (
            "sequence_diagram.puml must end with @enduml"
        )

    def test_user_participant_present(self):
        content = _read(SEQUENCE_DIAGRAM)
        assert "User" in content, (
            "sequence_diagram.puml must include a User participant"
        )

    def test_calculator_participant_present(self):
        content = _read(SEQUENCE_DIAGRAM)
        assert "Calculator" in content, (
            "sequence_diagram.puml must include a Calculator participant"
        )

    def test_input_handler_participant_present(self):
        content = _read(SEQUENCE_DIAGRAM)
        assert "InputHandler" in content, (
            "sequence_diagram.puml must include an InputHandler participant"
        )

    def test_has_participant_declarations(self):
        content = _read(SEQUENCE_DIAGRAM)
        # 'actor', 'participant', or 'boundary' introduce participants
        has_declarations = any(
            kw in content for kw in ("actor", "participant", "boundary")
        )
        assert has_declarations, (
            "sequence_diagram.puml must declare participants with actor/participant/boundary"
        )

    def test_has_message_arrows(self):
        content = _read(SEQUENCE_DIAGRAM)
        assert "->" in content, (
            "sequence_diagram.puml must contain at least one message arrow (->)"
        )

    def test_exit_quit_condition_shown(self):
        content = _read(SEQUENCE_DIAGRAM)
        assert "quit" in content or "exit" in content, (
            "sequence_diagram.puml must show the quit/exit condition"
        )

    def test_loop_block_present(self):
        content = _read(SEQUENCE_DIAGRAM)
        assert "loop" in content, (
            "sequence_diagram.puml must contain a loop block"
        )

    def test_goodbye_message_present(self):
        content = _read(SEQUENCE_DIAGRAM)
        assert "Goodbye" in content, (
            "sequence_diagram.puml must include the 'Goodbye!' farewell message"
        )

    def test_run_session_or_main_entrypoint_referenced(self):
        content = _read(SEQUENCE_DIAGRAM)
        assert "run_session" in content or "__main__" in content or "main" in content, (
            "sequence_diagram.puml must reference the entry point (run_session or __main__)"
        )

    def test_dispatch_flow_documented(self):
        content = _read(SEQUENCE_DIAGRAM)
        # The dispatch step must call through to Calculator
        assert "dispatch" in content or "getattr" in content, (
            "sequence_diagram.puml must document the dispatch flow to Calculator"
        )

    def test_result_returned_to_user(self):
        content = _read(SEQUENCE_DIAGRAM)
        assert "Result" in content, (
            "sequence_diagram.puml must show the Result being printed to the User"
        )

    @pytest.mark.parametrize("operation", ["add"])
    def test_example_operation_shown(self, operation):
        content = _read(SEQUENCE_DIAGRAM)
        assert operation in content, (
            f"sequence_diagram.puml must include an example using the '{operation}' operation"
        )
