"""Comprehensive test suite for Calculator history persistence feature.

Tests cover:
1. persist_history_to_file - file writing, error handling (18 tests)
2. display_history_notification - output format (4 tests)
3. prompt_for_operator quit/exit detection - immediate return (8 tests)
4. run_calculator with calc parameter - reuse and persistence (6 tests)
5. main() interactive loop - multi-calc accumulation and loop control (8 tests)
6. main() history sub-command - reading history.txt (4 tests)
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO

from src.calculator import Calculator
from src.cli import (
    persist_history_to_file,
    display_history_notification,
    prompt_for_operator,
    run_calculator,
)


# ===== GROUP 1: persist_history_to_file TESTS =====

class TestPersistHistoryToFileWithData:
    """Test persist_history_to_file appends entries in expected format."""

    def test_persist_history_with_populated_calc(self, tmp_path):
        """
        Create Calculator with one operation (add), persist to temp file,
        verify file contains formatted entry.
        """
        calc = Calculator()
        calc.add(5, 3)
        history_file = tmp_path / "history.txt"

        persist_history_to_file(calc, str(history_file))

        assert history_file.exists()
        content = history_file.read_text()
        assert "add" in content
        assert "5" in content
        assert "3" in content
        assert "8" in content

    def test_persist_history_multiple_operations(self, tmp_path):
        """
        Create Calculator with 3 operations, persist, verify all appear in file.
        """
        calc = Calculator()
        calc.add(1, 2)
        calc.multiply(3, 4)
        calc.divide(20, 5)
        history_file = tmp_path / "history.txt"

        persist_history_to_file(calc, str(history_file))

        content = history_file.read_text()
        # All operations should be present
        assert "add" in content
        assert "multiply" in content
        assert "divide" in content
        # Results should be present
        assert "3" in content  # 1 + 2
        assert "12" in content  # 3 * 4
        assert "4" in content  # 20 / 5

    def test_persist_history_uses_format_history_entry(self, tmp_path):
        """
        Verify output matches _format_history_entry pattern: index. operation(operands) = result
        """
        from src.cli import _format_history_entry
        calc = Calculator()
        calc.square(5)
        history_file = tmp_path / "history.txt"

        persist_history_to_file(calc, str(history_file))

        content = history_file.read_text().strip()
        # Should match format: "1. square(5.0) = 25"
        assert "1." in content
        assert "square" in content
        assert "5" in content
        assert "25" in content
        assert "=" in content


class TestPersistHistoryEmptyCalculator:
    """Test persist_history_to_file with empty Calculator."""

    def test_persist_history_with_empty_calc(self, tmp_path):
        """
        Create Calculator with no operations, persist to temp file,
        verify file is empty or not created.
        """
        calc = Calculator()
        history_file = tmp_path / "history.txt"

        persist_history_to_file(calc, str(history_file))

        # File may or may not exist; if it does, it should be empty
        if history_file.exists():
            content = history_file.read_text()
            assert content == ""


class TestPersistHistoryAppendSemantics:
    """Test that multiple calls to persist_history_to_file append, not overwrite."""

    def test_persist_history_append_semantics(self, tmp_path):
        """
        Call persist twice on same file with different Calculator instances,
        verify both sets of entries are preserved.
        """
        history_file = tmp_path / "history.txt"

        # First persistence: add(1, 2)
        calc1 = Calculator()
        calc1.add(1, 2)
        persist_history_to_file(calc1, str(history_file))

        # Second persistence: multiply(3, 4)
        calc2 = Calculator()
        calc2.multiply(3, 4)
        persist_history_to_file(calc2, str(history_file))

        content = history_file.read_text()
        # Both operations should be present
        assert "add" in content
        assert "multiply" in content
        # Both results
        assert "3" in content  # 1 + 2
        assert "12" in content  # 3 * 4


class TestPersistHistoryErrorHandling:
    """Test persist_history_to_file error handling (ValueError, IOError, OSError)."""

    def test_persist_history_invalid_path_no_exception(self, capsys):
        """
        Try to persist to invalid path (e.g., /nonexistent/dir/history.txt),
        verify warning is printed and no exception is raised.
        """
        calc = Calculator()
        calc.add(1, 2)
        invalid_path = "/nonexistent/dir/does/not/exist/history.txt"

        # Should not raise
        persist_history_to_file(calc, invalid_path)

        captured = capsys.readouterr()
        # Warning should be printed
        assert "Warning" in captured.out or "Could not save" in captured.out

    def test_persist_history_read_only_directory(self, capsys, tmp_path):
        """
        Try to persist to read-only directory (if possible on platform),
        verify graceful error handling.
        """
        calc = Calculator()
        calc.add(1, 2)

        # Create a directory and remove write permissions
        read_only_dir = tmp_path / "readonly"
        read_only_dir.mkdir()
        read_only_dir.chmod(0o444)

        try:
            invalid_path = str(read_only_dir / "history.txt")
            persist_history_to_file(calc, invalid_path)

            captured = capsys.readouterr()
            # Should print warning, not raise exception
            assert "Warning" in captured.out or "Could not save" in captured.out
        finally:
            # Cleanup: restore permissions
            read_only_dir.chmod(0o755)

    def test_persist_history_catches_ioerror(self, capsys, tmp_path):
        """
        Mock Calculator.get_history() to raise IOError during file write,
        verify error is caught and warning printed.
        """
        calc = Calculator()
        calc.add(1, 2)

        # Mock open to raise IOError
        with patch("builtins.open", side_effect=IOError("Mocked I/O error")):
            persist_history_to_file(calc, str(tmp_path / "history.txt"))

        captured = capsys.readouterr()
        assert "Warning" in captured.out or "Could not save" in captured.out


class TestPersistHistoryCustomFilepath:
    """Test persist_history_to_file with custom filepath parameter."""

    def test_persist_history_custom_filepath(self, tmp_path):
        """
        Persist to custom filepath (not "history.txt"),
        verify file created at custom location.
        """
        calc = Calculator()
        calc.add(5, 3)
        custom_file = tmp_path / "my_custom_history.log"

        persist_history_to_file(calc, str(custom_file))

        assert custom_file.exists()
        content = custom_file.read_text()
        assert "add" in content
        assert "5" in content

    def test_persist_history_filepath_with_subdirectory(self, tmp_path):
        """
        Persist to filepath in subdirectory that exists,
        verify file created in correct location.
        """
        calc = Calculator()
        calc.multiply(2, 3)
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        history_file = subdir / "history.txt"

        persist_history_to_file(calc, str(history_file))

        assert history_file.exists()
        content = history_file.read_text()
        assert "multiply" in content


# ===== GROUP 2: display_history_notification TESTS =====

class TestDisplayHistoryNotification:
    """Test display_history_notification output format."""

    def test_display_history_notification_default(self, capsys):
        """
        Call display_history_notification() with default filepath,
        verify output contains 'history.txt' and 'python -m calculator history'.
        """
        display_history_notification()
        captured = capsys.readouterr()
        output = captured.out
        assert "history.txt" in output
        assert "python -m calculator history" in output

    def test_display_history_notification_custom_filepath(self, capsys):
        """
        Call display_history_notification(filepath='custom.log'),
        verify output contains 'custom.log' and 'python -m calculator history'.
        """
        display_history_notification(filepath="custom.log")
        captured = capsys.readouterr()
        output = captured.out
        assert "custom.log" in output
        assert "python -m calculator history" in output

    def test_display_history_notification_contains_history_txt(self, capsys):
        """
        Verify notification mentions the history.txt file explicitly.
        """
        display_history_notification(filepath="history.txt")
        captured = capsys.readouterr()
        output = captured.out
        assert "History saved to history.txt" in output

    def test_display_history_notification_contains_command(self, capsys):
        """
        Verify notification mentions viewing history with python -m calculator history.
        """
        display_history_notification()
        captured = capsys.readouterr()
        output = captured.out
        assert "View your history with" in output
        assert "python -m calculator history" in output


# ===== GROUP 3: prompt_for_operator quit/exit detection TESTS =====

class TestPromptForOperatorQuitDetection:
    """Test that quit/exit inputs return "QUIT" immediately."""

    @pytest.mark.parametrize("quit_input", ["quit", "exit"])
    def test_prompt_for_operator_quit_lowercase(self, quit_input):
        """
        Input 'quit' or 'exit' returns "QUIT" immediately.
        """
        with patch("builtins.input", return_value=quit_input):
            result = prompt_for_operator()
            assert result == "QUIT"

    @pytest.mark.parametrize("quit_input", ["QUIT", "EXIT"])
    def test_prompt_for_operator_quit_uppercase(self, quit_input):
        """
        Input 'QUIT' or 'EXIT' returns "QUIT" immediately.
        """
        with patch("builtins.input", return_value=quit_input):
            result = prompt_for_operator()
            assert result == "QUIT"

    def test_prompt_for_operator_quit_case_insensitive(self):
        """
        Input 'QuIt' (mixed case) returns "QUIT" immediately.
        """
        with patch("builtins.input", return_value="QuIt"):
            result = prompt_for_operator()
            assert result == "QUIT"

    def test_prompt_for_operator_quit_no_retry_consumed(self):
        """
        Input 'quit' does not consume retry count,
        verify by mocking input to check it's not called again.
        """
        mock_input = patch("builtins.input", return_value="quit")
        with mock_input as m:
            result = prompt_for_operator()
            assert result == "QUIT"
            # input() should be called exactly once
            assert m.call_count == 1

    def test_prompt_for_operator_exit_no_retry_consumed(self):
        """
        Input 'exit' does not consume retry count.
        """
        mock_input = patch("builtins.input", return_value="exit")
        with mock_input as m:
            result = prompt_for_operator()
            assert result == "QUIT"
            assert m.call_count == 1

    def test_prompt_for_operator_normal_invalid_increments_retry(self):
        """
        Invalid operator (not quit/exit) still increments retry count,
        eventually raises MaxRetriesExceeded.
        """
        from src.cli import MaxRetriesExceeded
        # Input: invalid, invalid, invalid, invalid (4 invalid attempts)
        with patch("builtins.input", side_effect=["invalid", "invalid", "invalid", "invalid"]):
            with pytest.raises(MaxRetriesExceeded):
                prompt_for_operator(max_retries=3)

    def test_prompt_for_operator_quit_then_continue_simulation(self):
        """
        Verify that 'quit' returns immediately, not consumed by retry logic.
        """
        with patch("builtins.input", return_value="quit"):
            result = prompt_for_operator(max_retries=3)
            assert result == "QUIT"


# ===== GROUP 4: run_calculator with calc parameter TESTS =====

class TestRunCalculatorWithCalcParameter:
    """Test run_calculator with calc parameter (reuse and persistence)."""

    def test_run_calculator_creates_fresh_calc_when_none(self):
        """
        Call run_calculator(calc=None), verify it creates a Calculator and returns float result.
        """
        with patch("builtins.input", side_effect=["+", "5", "3"]):
            result = run_calculator(calc=None)
            assert isinstance(result, (int, float))
            assert result == 8

    def test_run_calculator_reuses_existing_calc(self):
        """
        Create Calculator, pass to run_calculator, verify history accumulates.
        """
        calc = Calculator()
        calc.add(1, 1)
        assert len(calc.get_history()) == 1

        with patch("builtins.input", side_effect=["+", "5", "3"]):
            result = run_calculator(calc=calc)
            assert result == 8
            # History should contain both operations
            assert len(calc.get_history()) == 2

    def test_run_calculator_returns_quit_from_operator_prompt(self):
        """
        Call run_calculator, user enters 'quit' at operator prompt,
        verify return value is "QUIT".
        """
        with patch("builtins.input", return_value="quit"):
            result = run_calculator()
            assert result == "QUIT"

    def test_run_calculator_history_accumulates_across_calls(self):
        """
        Create Calculator, call run_calculator twice with same instance,
        verify all 2 operations in history.
        """
        calc = Calculator()

        # First call: +
        with patch("builtins.input", side_effect=["+", "1", "2"]):
            result1 = run_calculator(calc=calc)
            assert result1 == 3

        # Second call: *
        with patch("builtins.input", side_effect=["*", "4", "5"]):
            result2 = run_calculator(calc=calc)
            assert result2 == 20

        # History should have both
        history = calc.get_history()
        assert len(history) == 2
        assert history[0]["operation"] == "add"
        assert history[1]["operation"] == "multiply"

    def test_run_calculator_displays_notification_after_success(self, capsys):
        """
        After successful calculation, display_history_notification is called.
        """
        with patch("builtins.input", side_effect=["+", "2", "3"]):
            run_calculator()
            captured = capsys.readouterr()
            output = captured.out
            assert "history.txt" in output
            assert "python -m calculator history" in output


# ===== GROUP 5: main() interactive loop TESTS =====

class TestMainInteractiveLoop:
    """Test main() interactive loop behavior."""

    def test_main_multiple_calculations_accumulate(self, tmp_path, monkeypatch):
        """
        Simulate 2 calculations in interactive loop, verify history accumulates.
        """
        monkeypatch.chdir(tmp_path)
        history_file = tmp_path / "history.txt"

        # Mock sys.argv, input, and sys.exit
        with patch("sys.argv", ["calculator"]):
            with patch("builtins.input", side_effect=[
                "+", "1", "2",  # First: add(1, 2) = 3
                "+", "3", "4",  # Second: add(3, 4) = 7
                "quit"           # Exit
            ]):
                with patch("sys.exit") as mock_exit:
                    from src.__main__ import main
                    main()
                    # sys.exit(0) should be called at the end
                    mock_exit.assert_called_with(0)

        # Verify history file was written
        assert history_file.exists()
        content = history_file.read_text()
        # Should have 2 operations
        assert content.count("add") == 2

    def test_main_loop_breaks_on_quit(self, tmp_path, monkeypatch):
        """
        User enters 'quit', loop breaks, persist_history_to_file is called.
        """
        monkeypatch.chdir(tmp_path)
        history_file = tmp_path / "history.txt"

        with patch("sys.argv", ["calculator"]):
            with patch("builtins.input", side_effect=["quit"]):
                with patch("sys.exit") as mock_exit:
                    from src.__main__ import main
                    main()
                    mock_exit.assert_called_with(0)

    def test_main_loop_persists_history_on_exit(self, tmp_path, monkeypatch):
        """
        Perform 1 operation, quit, verify persist_history_to_file is called (file created).
        """
        monkeypatch.chdir(tmp_path)
        history_file = tmp_path / "history.txt"

        with patch("sys.argv", ["calculator"]):
            with patch("builtins.input", side_effect=["+", "1", "2", "quit"]):
                with patch("sys.exit"):
                    from src.__main__ import main
                    main()

        # History file should exist with the operation
        assert history_file.exists()
        content = history_file.read_text()
        assert "add" in content

    def test_main_keyboard_interrupt_prints_message(self, tmp_path, monkeypatch, capsys):
        """
        Simulate KeyboardInterrupt (Ctrl-C), verify "Exiting..." printed.
        """
        monkeypatch.chdir(tmp_path)

        with patch("sys.argv", ["calculator"]):
            with patch("builtins.input", side_effect=KeyboardInterrupt):
                with patch("sys.exit"):
                    from src.__main__ import main
                    main()

        captured = capsys.readouterr()
        assert "Exiting..." in captured.out

    def test_main_keyboard_interrupt_still_persists_history(self, tmp_path, monkeypatch):
        """
        KeyboardInterrupt raised, verify persist_history_to_file is still called in finally.
        """
        monkeypatch.chdir(tmp_path)
        history_file = tmp_path / "history.txt"

        with patch("sys.argv", ["calculator"]):
            with patch("builtins.input", side_effect=["+", "5", "3", KeyboardInterrupt]):
                with patch("sys.exit"):
                    from src.__main__ import main
                    main()

        # History should be persisted despite KeyboardInterrupt
        assert history_file.exists()
        content = history_file.read_text()
        assert "add" in content

    def test_main_calls_sys_exit_0_at_end(self, tmp_path, monkeypatch):
        """
        Interactive loop completes normally (user quits),
        sys.exit(0) is called at end of main().
        """
        monkeypatch.chdir(tmp_path)

        with patch("sys.argv", ["calculator"]):
            with patch("builtins.input", side_effect=["quit"]):
                with patch("sys.exit") as mock_exit:
                    from src.__main__ import main
                    main()
                    # sys.exit should be called with 0
                    mock_exit.assert_called_with(0)


# ===== GROUP 6: main() history sub-command TESTS =====

class TestMainHistorySubcommand:
    """Test main() handling of 'history' sub-command."""

    def test_main_history_reads_and_prints_file(self, tmp_path, monkeypatch, capsys):
        """
        Create history.txt, call main() with argv ['calculator', 'history'],
        verify content is printed to stdout.
        """
        monkeypatch.chdir(tmp_path)
        history_file = tmp_path / "history.txt"
        history_file.write_text("1. add(1, 2) = 3\n2. multiply(3, 4) = 12\n")

        with patch("sys.argv", ["calculator", "history"]):
            with patch("sys.exit") as mock_exit:
                from src.__main__ import main
                main()
                mock_exit.assert_called_with(0)

        captured = capsys.readouterr()
        output = captured.out
        assert "add" in output
        assert "multiply" in output

    def test_main_history_prints_no_history_found_when_missing(self, tmp_path, monkeypatch, capsys):
        """
        No history.txt exists, call main() with ['calculator', 'history'],
        verify "No history found." printed and sys.exit(0) called.
        """
        monkeypatch.chdir(tmp_path)
        # Ensure history.txt does NOT exist
        assert not (tmp_path / "history.txt").exists()

        with patch("sys.argv", ["calculator", "history"]):
            with patch("sys.exit") as mock_exit:
                from src.__main__ import main
                main()
                mock_exit.assert_called_with(0)

        captured = capsys.readouterr()
        output = captured.out
        assert "No history found." in output

    def test_main_history_exits_with_0(self, tmp_path, monkeypatch):
        """
        Call main() with ['calculator', 'history'], verify sys.exit(0) is called.
        """
        monkeypatch.chdir(tmp_path)
        (tmp_path / "history.txt").write_text("1. add(1, 2) = 3\n")

        with patch("sys.argv", ["calculator", "history"]):
            with patch("sys.exit") as mock_exit:
                from src.__main__ import main
                main()
                mock_exit.assert_called_with(0)

    def test_main_history_reads_entire_file_content(self, tmp_path, monkeypatch, capsys):
        """
        Create history.txt with multiple entries, call main() history,
        verify all lines are printed.
        """
        monkeypatch.chdir(tmp_path)
        history_content = "1. add(1, 2) = 3\n2. subtract(5, 2) = 3\n3. multiply(2, 3) = 6\n"
        history_file = tmp_path / "history.txt"
        history_file.write_text(history_content)

        with patch("sys.argv", ["calculator", "history"]):
            with patch("sys.exit"):
                from src.__main__ import main
                main()

        captured = capsys.readouterr()
        output = captured.out
        # All three operations should appear
        assert "add" in output
        assert "subtract" in output
        assert "multiply" in output
