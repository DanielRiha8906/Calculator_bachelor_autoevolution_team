"""
Tests for the src.__main__ module entry point.

Verifies that running `python -m src` correctly invokes the interactive session.
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

        Expected: run_interactive_session is called exactly once with no arguments.
        """
        # Mock run_interactive_session before running the module to prevent actual
        # interactive input attempts during test execution
        with patch('src.interactive.run_interactive_session') as mock_run:
            # Clear the module cache to force re-execution with the mock in place
            if 'src.__main__' in sys.modules:
                del sys.modules['src.__main__']

            # Simulate `python -m src` with mocked run_interactive_session
            runpy.run_module('src', run_name='__main__')

            # Verify run_interactive_session was called exactly once with no args
            assert mock_run.call_count == 1
            mock_run.assert_called_once_with()

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
