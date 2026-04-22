"""Integration tests for the operation history feature in the calculator session."""

import pytest
import os
from unittest.mock import patch
from src.__main__ import main
from src.history import OperationHistory


class TestSessionRecordsOperationsToHistory:
    """Integration tests for recording operations to history file during session."""

    def test_single_operation_recorded_to_history(self, tmp_path, monkeypatch):
        """Test that a single operation is recorded to the history file during session."""
        history_file = tmp_path / "history.txt"
        monkeypatch.setattr("src.history.OperationHistory.__init__",
                           lambda self, filename="history.txt": setattr(self, "filename", str(history_file)))

        with patch("builtins.input", side_effect=["add", "5", "3", "exit"]):
            main()

        # Verify operation was recorded
        assert history_file.exists()
        with open(history_file, "r") as f:
            content = f.read()
        assert "add(5.0, 3.0) = 8.0" in content

    def test_multiple_operations_recorded_in_order(self, tmp_path, monkeypatch):
        """Test that multiple operations are recorded to file in order."""
        history_file = tmp_path / "history.txt"
        monkeypatch.setattr("src.history.OperationHistory.__init__",
                           lambda self, filename="history.txt": setattr(self, "filename", str(history_file)))

        with patch("builtins.input", side_effect=[
            "add", "1", "2",
            "multiply", "3", "4",
            "divide", "10", "2",
            "exit"
        ]):
            main()

        assert history_file.exists()
        with open(history_file, "r") as f:
            lines = f.read().strip().split("\n")

        assert len(lines) == 3
        assert "add(1.0, 2.0) = 3.0" in lines[0]
        assert "multiply(3.0, 4.0) = 12.0" in lines[1]
        assert "divide(10.0, 2.0) = 5.0" in lines[2]

    def test_unary_operation_recorded_to_history(self, tmp_path, monkeypatch):
        """Test that unary operations are recorded correctly."""
        history_file = tmp_path / "history.txt"
        monkeypatch.setattr("src.history.OperationHistory.__init__",
                           lambda self, filename="history.txt": setattr(self, "filename", str(history_file)))

        with patch("builtins.input", side_effect=["square", "5", "exit"]):
            main()

        assert history_file.exists()
        with open(history_file, "r") as f:
            content = f.read()
        assert "square(5.0) = 25.0" in content

    def test_factorial_recorded_with_int_operand(self, tmp_path, monkeypatch):
        """Test that factorial operation is recorded with integer operand."""
        history_file = tmp_path / "history.txt"
        monkeypatch.setattr("src.history.OperationHistory.__init__",
                           lambda self, filename="history.txt": setattr(self, "filename", str(history_file)))

        with patch("builtins.input", side_effect=["factorial", "5", "exit"]):
            main()

        assert history_file.exists()
        with open(history_file, "r") as f:
            content = f.read()
        # Factorial should record the int-converted operand
        assert "factorial(5) = 120" in content


class TestHistoryClearedAtSessionStart:
    """Integration tests for history being cleared at session startup."""

    def test_history_cleared_on_new_session_start(self, tmp_path, monkeypatch):
        """Test that history is cleared when a new session starts."""
        history_file = tmp_path / "history.txt"

        # Override OperationHistory to use our temp file
        original_init = OperationHistory.__init__

        def mock_init(self, filename="history.txt"):
            original_init(self, str(history_file))

        monkeypatch.setattr("src.history.OperationHistory.__init__", mock_init)

        # First session: record an operation
        with patch("builtins.input", side_effect=["add", "1", "1", "exit"]):
            main()

        assert history_file.exists()
        with open(history_file, "r") as f:
            content = f.read()
        assert "add(1.0, 1.0) = 2.0" in content
        first_session_size = len(content)

        # Second session: history should be cleared before any new operations
        with patch("builtins.input", side_effect=["subtract", "5", "2", "exit"]):
            main()

        # History file should only contain the new operation, not the old one
        with open(history_file, "r") as f:
            content = f.read()

        assert "add" not in content, "Old operation should be removed after history.clear()"
        assert "subtract(5.0, 2.0) = 3.0" in content

    def test_history_file_does_not_accumulate_across_sessions(self, tmp_path, monkeypatch):
        """Test that history doesn't accumulate across multiple session starts."""
        history_file = tmp_path / "history.txt"

        original_init = OperationHistory.__init__

        def mock_init(self, filename="history.txt"):
            original_init(self, str(history_file))

        monkeypatch.setattr("src.history.OperationHistory.__init__", mock_init)

        # Run 3 sessions, each with different operations
        operations_per_session = [
            (["add", "1", "1", "exit"], "add(1.0, 1.0) = 2.0"),
            (["multiply", "2", "3", "exit"], "multiply(2.0, 3.0) = 6.0"),
            (["divide", "8", "2", "exit"], "divide(8.0, 2.0) = 4.0"),
        ]

        for inputs, expected_content in operations_per_session:
            with patch("builtins.input", side_effect=inputs):
                main()

        # Final history should only contain the last session's operation
        with open(history_file, "r") as f:
            content = f.read()

        lines = [line.strip() for line in content.strip().split("\n") if line.strip()]
        # Should have exactly 1 line (the last operation)
        assert len(lines) == 1
        assert "divide(8.0, 2.0) = 4.0" in lines[0]


class TestHistorySentinelInInteractiveFlow:
    """Integration tests for 'history' sentinel in interactive flow."""

    def test_history_command_displays_recorded_operations(self, tmp_path, monkeypatch):
        """Test that 'history' command displays operations recorded in session."""
        history_file = tmp_path / "history.txt"

        original_init = OperationHistory.__init__

        def mock_init(self, filename="history.txt"):
            original_init(self, str(history_file))

        monkeypatch.setattr("src.history.OperationHistory.__init__", mock_init)

        with patch("builtins.input", side_effect=[
            "add", "1", "2",
            "history",
            "exit"
        ]):
            with patch("builtins.print") as mock_print:
                main()

            # Verify that history was printed
            print_calls = [str(call) for call in mock_print.call_args_list]
            all_output = " ".join(print_calls)
            # Should contain the operation in numbered format
            assert any("add(1.0, 2.0) = 3.0" in str(call) for call in mock_print.call_args_list)

    def test_history_command_does_not_exit_session(self, tmp_path, monkeypatch):
        """Test that 'history' command doesn't exit the session."""
        history_file = tmp_path / "history.txt"

        original_init = OperationHistory.__init__

        def mock_init(self, filename="history.txt"):
            original_init(self, str(history_file))

        monkeypatch.setattr("src.history.OperationHistory.__init__", mock_init)

        with patch("builtins.input", side_effect=[
            "add", "5", "3",
            "history",
            "subtract", "10", "5",
            "exit"
        ]):
            main()

        # Verify both operations were recorded
        with open(history_file, "r") as f:
            content = f.read()

        assert "add(5.0, 3.0) = 8.0" in content
        assert "subtract(10.0, 5.0) = 5.0" in content

    def test_history_command_multiple_times_in_session(self, tmp_path, monkeypatch):
        """Test that 'history' can be called multiple times during a session."""
        history_file = tmp_path / "history.txt"

        original_init = OperationHistory.__init__

        def mock_init(self, filename="history.txt"):
            original_init(self, str(history_file))

        monkeypatch.setattr("src.history.OperationHistory.__init__", mock_init)

        with patch("builtins.input", side_effect=[
            "add", "1", "1",
            "history",
            "multiply", "2", "3",
            "history",
            "exit"
        ]):
            main()

        # Verify both operations were recorded
        with open(history_file, "r") as f:
            content = f.read()

        assert "add(1.0, 1.0) = 2.0" in content
        assert "multiply(2.0, 3.0) = 6.0" in content

    def test_history_with_empty_session(self, tmp_path, monkeypatch):
        """Test that 'history' displays 'No history yet.' when no operations recorded."""
        history_file = tmp_path / "history.txt"

        original_init = OperationHistory.__init__

        def mock_init(self, filename="history.txt"):
            original_init(self, str(history_file))

        monkeypatch.setattr("src.history.OperationHistory.__init__", mock_init)

        with patch("builtins.input", side_effect=[
            "history",
            "exit"
        ]):
            with patch("builtins.print") as mock_print:
                main()

            # Verify that "No history yet." was printed
            assert any("No history yet" in str(call) for call in mock_print.call_args_list)


class TestHistoryErrorHandling:
    """Integration tests for error handling with history."""

    def test_error_operation_not_recorded_in_history(self, tmp_path, monkeypatch):
        """Test that operations resulting in errors are not recorded in history."""
        history_file = tmp_path / "history.txt"

        original_init = OperationHistory.__init__

        def mock_init(self, filename="history.txt"):
            original_init(self, str(history_file))

        monkeypatch.setattr("src.history.OperationHistory.__init__", mock_init)

        with patch("builtins.input", side_effect=[
            "divide", "5", "0",  # This will error
            "exit"
        ]):
            main()

        # History file should not exist or should be empty (no successful operation recorded)
        if history_file.exists():
            with open(history_file, "r") as f:
                content = f.read()
            # File should be empty because the divide by zero failed
            assert "divide" not in content or content.strip() == ""

    def test_successful_operation_after_error_recorded(self, tmp_path, monkeypatch):
        """Test that successful operations after an error are still recorded."""
        history_file = tmp_path / "history.txt"

        original_init = OperationHistory.__init__

        def mock_init(self, filename="history.txt"):
            original_init(self, str(history_file))

        monkeypatch.setattr("src.history.OperationHistory.__init__", mock_init)

        with patch("builtins.input", side_effect=[
            "divide", "5", "0",  # This will error
            "add", "2", "3",     # This should succeed
            "exit"
        ]):
            main()

        # Only the successful add operation should be recorded
        assert history_file.exists()
        with open(history_file, "r") as f:
            content = f.read()

        assert "add(2.0, 3.0) = 5.0" in content
        assert "divide" not in content


class TestHistoryFileLocation:
    """Integration tests for history file location and naming."""

    def test_history_file_created_in_working_directory(self, tmp_path):
        """Test that history.txt is created in the current working directory by default."""
        import os
        original_cwd = os.getcwd()

        try:
            os.chdir(str(tmp_path))

            with patch("builtins.input", side_effect=["add", "1", "1", "exit"]):
                main()

            # Check that history.txt exists in the temp directory
            history_path = tmp_path / "history.txt"
            assert history_path.exists()

        finally:
            os.chdir(original_cwd)
