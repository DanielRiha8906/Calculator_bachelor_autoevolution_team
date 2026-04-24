"""
Tests for the src.__main__ module entry point.

Verifies that running `python -m src` correctly dispatches to interactive session
or CLI based on the presence of command-line arguments.
"""

import runpy
import sys
from unittest.mock import patch, MagicMock

import pytest


class TestMainEntryPoint:
    """Test suite for src.__main__ module entry point."""

    def test_main_entry_point_calls_interactive_session(self):
        """
        Scenario: Running `python -m src` should invoke run_interactive_session().

        Method: Mock run_interactive_session at the import location before executing
        the module via runpy.run_module to prevent actual interactive code execution.
        Patch sys.argv to have length 1 (no CLI arguments).

        Expected: run_interactive_session is called exactly once with no arguments.
        """
        # Patch the source modules before running __main__
        with patch('src.ui.interactive.run_interactive_session') as mock_run:
            with patch('src.ui.cli.run_cli') as mock_cli:
                # Clear the module cache to force re-execution with the mock in place
                if 'src.__main__' in sys.modules:
                    del sys.modules['src.__main__']

                # Patch sys.argv to have length 1 (no CLI arguments)
                with patch.object(sys, 'argv', ['src']):
                    # Simulate `python -m src` with mocked run_interactive_session
                    runpy.run_module('src', run_name='__main__')

                    # Verify run_interactive_session was called exactly once with no args
                    assert mock_run.call_count == 1
                    mock_run.assert_called_once_with()

                    # Verify run_cli was NOT called
                    assert mock_cli.call_count == 0

    def test_main_function_preserved_for_backward_compatibility(self):
        """
        Scenario: The main() function should still exist and be callable
        for backward compatibility, even though it's not called by the entry point.

        Expected: main() function exists and can be called without error.
        """
        from src.__main__ import main

        # Verify main is callable
        assert callable(main)

        # Mock print to capture output without actually printing
        with patch('builtins.print'):
            # Should not raise any exception
            main()

    def test_main_function_demo_output(self):
        """
        Scenario: The main() function should print demo output for all basic operations.

        Expected: Print is called with output for add, subtract, multiply, divide, factorial.
        """
        from src.__main__ import main

        with patch('builtins.print') as mock_print:
            main()

            # Verify print was called (at least once per operation)
            assert mock_print.call_count >= 5  # add, subtract, multiply, divide, factorial

            # Verify the calls include expected operation names
            print_calls_text = str(mock_print.call_args_list)
            assert 'Addition' in print_calls_text or any(
                'Addition' in str(call) for call in mock_print.call_args_list
            )


class TestMainDispatch:
    """Test suite for CLI vs interactive mode dispatch logic."""

    def test_main_entry_no_args_calls_interactive(self):
        """
        Scenario: When sys.argv contains only the script name (length 1),
        run_interactive_session() should be called.

        Expected: run_interactive_session() is called; run_cli() is NOT called.
        """
        with patch('src.ui.interactive.run_interactive_session') as mock_interactive:
            with patch('src.ui.cli.run_cli') as mock_cli:
                if 'src.__main__' in sys.modules:
                    del sys.modules['src.__main__']

                with patch.object(sys, 'argv', ['src']):
                    runpy.run_module('src', run_name='__main__')

                    assert mock_interactive.call_count == 1
                    assert mock_cli.call_count == 0

    def test_main_entry_with_cli_args_calls_cli(self):
        """
        Scenario: When sys.argv contains command-line arguments (length > 1),
        run_cli() should be called with those arguments; run_interactive_session()
        should NOT be called.

        Expected: run_cli() is called; run_interactive_session() is NOT called.
        """
        with patch('src.ui.interactive.run_interactive_session') as mock_interactive:
            with patch('src.ui.cli.run_cli', return_value=0) as mock_cli:
                if 'src.__main__' in sys.modules:
                    del sys.modules['src.__main__']

                with patch.object(sys, 'argv', ['src', 'add', '5', '7']):
                    # Mock sys.exit to prevent test exit
                    with patch('sys.exit'):
                        runpy.run_module('src', run_name='__main__')

                        assert mock_cli.call_count == 1
                        assert mock_interactive.call_count == 0

    def test_main_entry_cli_success_exit_zero(self):
        """
        Scenario: When run_cli() returns 0 (success), sys.exit(0) should be called.

        Expected: sys.exit(0) is called.
        """
        with patch('src.ui.cli.run_cli', return_value=0) as mock_cli:
            if 'src.__main__' in sys.modules:
                del sys.modules['src.__main__']

            with patch.object(sys, 'argv', ['src', 'add', '5', '7']):
                with patch('sys.exit') as mock_exit:
                    runpy.run_module('src', run_name='__main__')
                    mock_exit.assert_called_once_with(0)

    def test_main_entry_cli_error_exit_nonzero(self):
        """
        Scenario: When run_cli() returns 1 (error), sys.exit(1) should be called.

        Expected: sys.exit(1) is called.
        """
        with patch('src.ui.cli.run_cli', return_value=1) as mock_cli:
            if 'src.__main__' in sys.modules:
                del sys.modules['src.__main__']

            with patch.object(sys, 'argv', ['src', 'unknown_op', '5']):
                with patch('sys.exit') as mock_exit:
                    runpy.run_module('src', run_name='__main__')
                    mock_exit.assert_called_once_with(1)

    def test_main_entry_single_arg_dispatches_to_cli(self):
        """
        Scenario: When sys.argv has length > 1 (e.g., ['src', 'add']),
        even with a single argument after the script name, run_cli()
        should be invoked (not run_interactive_session()).

        Expected: run_cli() is called; run_interactive_session() is NOT called.
        """
        with patch('src.ui.interactive.run_interactive_session') as mock_interactive:
            with patch('src.ui.cli.run_cli', return_value=1) as mock_cli:
                if 'src.__main__' in sys.modules:
                    del sys.modules['src.__main__']

                with patch.object(sys, 'argv', ['src', 'add']):
                    with patch('sys.exit'):
                        runpy.run_module('src', run_name='__main__')

                        assert mock_cli.call_count == 1
                        assert mock_interactive.call_count == 0
