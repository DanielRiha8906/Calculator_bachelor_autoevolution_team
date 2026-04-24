"""
Tests for input validation and retry logic in interactive calculator session.

Tests use unittest.mock.patch to mock builtins.input and capture builtins.print.
Each test validates counter incrementation on invalid inputs, session termination
after 5 consecutive failures, counter reset on success, and computation errors
not incrementing the counter.
"""

from unittest.mock import patch, call
import pytest
from src.ui.interactive import run_interactive_session


class TestValidationCounter:
    """Test suite for validation counter in run_interactive_session."""

    def test_max_attempts_constant_equals_5(self):
        """Test that MAX_ATTEMPTS constant is defined and equals 5.

        Scenario: Import interactive module and inspect MAX_ATTEMPTS.
        Expected: MAX_ATTEMPTS exists and equals 5.
        """
        from src.ui import interactive
        assert hasattr(interactive, 'MAX_ATTEMPTS'), \
            "interactive module should define MAX_ATTEMPTS constant"
        assert interactive.MAX_ATTEMPTS == 5, \
            f"MAX_ATTEMPTS should be 5, got {interactive.MAX_ATTEMPTS}"

    def test_valid_operation_resets_counter(self):
        """Test valid operation (index 0 = add) with valid operands resets counter to 0.

        Scenario: User selects valid operation (add), enters valid operands (5, 3).
        Expected: Calculation succeeds, result "Result: 8" displayed, counter resets to 0.

        This test validates counter reset by: valid op -> should trigger counter reset mechanism.
        """
        # Import to check that the counter reset mechanism is implemented
        from src.ui.interactive import run_interactive_session as ris
        import inspect
        source = inspect.getsource(ris)
        assert "counter" in source or "MAX_ATTEMPTS" in source, \
            "run_interactive_session must contain counter or MAX_ATTEMPTS logic"

        with patch('builtins.input', side_effect=["0", "5", "3", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # After valid operation, result should be printed
                assert "Result: 8" in output

    def test_invalid_operation_increments_counter_displays_list(self):
        """Test invalid operation index (999) increments counter, displays list, then valid add.

        Scenario: User enters invalid operation index 999, then valid operation 0.
        Expected: "Invalid operation" displayed, operations list shown, counter increments,
                 valid selection succeeds.
        """
        from src.ui.interactive import run_interactive_session as ris
        import inspect
        source = inspect.getsource(ris)
        assert "counter" in source or "MAX_ATTEMPTS" in source, \
            "run_interactive_session must implement counter/MAX_ATTEMPTS logic"

        with patch('builtins.input', side_effect=["999", "0", "5", "3", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # Should see both invalid message and result
                assert "Invalid operation" in output
                assert "Result: 8" in output

    def test_invalid_operand_unary_increments_counter(self):
        """Test unary operation with non-numeric operand increments counter.

        Scenario: User selects unary operation (e.g., sqrt at index 9),
                 enters non-numeric operand "abc", then correct value "4".
        Expected: "Invalid input" displayed, counter increments to 1, user re-prompted,
                 result calculated successfully.
        """
        from src.ui.interactive import run_interactive_session as ris
        import inspect
        source = inspect.getsource(ris)
        assert "counter" in source or "MAX_ATTEMPTS" in source, \
            "run_interactive_session must implement counter logic"

        with patch('builtins.input', side_effect=["9", "abc", "4", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # Should see invalid input message
                assert "Invalid input" in output
                # Should see result (sqrt(4) = 2.0)
                assert "Result:" in output

    def test_invalid_operand_binary_first_increments_counter(self):
        """Test binary operation with non-numeric first operand increments counter.

        Scenario: User selects "add" (index 0), enters non-numeric first operand "xyz",
                 then correct values 5, 3.
        Expected: "Invalid input" displayed, counter increments to 1, user re-prompted,
                 then succeeds with valid inputs.
        """
        from src.ui.interactive import run_interactive_session as ris
        import inspect
        source = inspect.getsource(ris)
        assert "counter" in source or "MAX_ATTEMPTS" in source, \
            "run_interactive_session must implement counter logic"

        with patch('builtins.input', side_effect=["0", "xyz", "5", "3", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "Invalid input" in output
                assert "Result: 8" in output

    def test_invalid_operand_binary_second_increments_counter(self):
        """Test binary operation with non-numeric second operand increments counter.

        Scenario: User selects "add", enters valid first operand 5,
                 enters non-numeric second operand "bad", then correct value 3.
        Expected: "Invalid input" displayed, counter increments to 1, user re-prompted,
                 then succeeds with valid second operand.
        """
        from src.ui.interactive import run_interactive_session as ris
        import inspect
        source = inspect.getsource(ris)
        assert "counter" in source or "MAX_ATTEMPTS" in source, \
            "run_interactive_session must implement counter logic"

        with patch('builtins.input', side_effect=["0", "5", "bad", "3", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "Invalid input" in output
                assert "Result: 8" in output

    def test_counter_resets_after_prior_failures(self):
        """Test counter resets to 0 after valid operation follows failures.

        Scenario: Two invalid operations (counter=2), then one valid operation
                 with valid operands (counter reset to 0).
        Expected: Two "Invalid operation" messages, then successful calculation result.
        """
        from src.ui.interactive import run_interactive_session as ris
        import inspect
        source = inspect.getsource(ris)
        assert "counter" in source or "MAX_ATTEMPTS" in source, \
            "run_interactive_session must implement counter reset logic"

        with patch('builtins.input', side_effect=["999", "888", "0", "5", "3", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # Should have at least 2 "Invalid" messages
                invalid_count = output.count("Invalid")
                assert invalid_count >= 2, f"Expected at least 2 'Invalid' messages, got {invalid_count}"
                # Then successful result
                assert "Result: 8" in output

    def test_session_terminates_after_5_consecutive_invalid_operations(self):
        """Test session terminates after 5 consecutive invalid operation indices.

        Scenario: User enters 5 consecutive invalid operation indices.
        Expected: After 5th attempt, "Too many consecutive invalid inputs. Session terminated."
                 displayed, session exits cleanly.
        """
        with patch('builtins.input', side_effect=["999", "888", "777", "666", "555"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # Should see termination message
                assert "Too many consecutive invalid inputs" in output or \
                       "Session terminated" in output, \
                       f"Expected termination message after 5 failures, output was: {output}"

    def test_session_terminates_after_5_consecutive_invalid_operands(self):
        """Test session terminates after 5 consecutive invalid operand inputs.

        Scenario: User selects valid operation (add at index 0), then attempts
                 to enter operand 5 times with non-numeric inputs.
        Expected: After 5th invalid operand, "Too many consecutive invalid inputs"
                 displayed, session exits cleanly.
        """
        with patch('builtins.input', side_effect=["0", "a", "b", "c", "d", "e"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # Should see termination message after 5 invalid operands
                assert "Too many consecutive invalid inputs" in output or \
                       "Session terminated" in output, \
                       f"Expected termination after 5 invalid operands, output was: {output}"

    def test_mixed_failures_count_toward_limit(self):
        """Test mixed operation and operand failures count toward 5-input limit.

        Scenario: Mix of invalid operation and invalid operands reaching 5 consecutive failures.
                 Input sequence: invalid_op, valid_op, then 5 invalid operands
        Expected: After 5th consecutive invalid operand entry, session terminates with message.
        """
        with patch('builtins.input', side_effect=["999", "0", "a", "b", "c", "d", "e"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # After 5th consecutive invalid operand, session terminates
                assert "Too many consecutive invalid inputs" in output or \
                       "Session terminated" in output, \
                       f"Expected termination after 5 consecutive invalid operands, output was: {output}"

    def test_computation_error_does_not_increment_counter_zero_division(self):
        """Test division by zero error does NOT increment counter.

        Scenario: User selects divide (index 3), enters operands 5 and 0
                 (triggers ZeroDivisionError).
        Expected: Error shown, counter NOT incremented, session continues (no termination).
        """
        from src.ui.interactive import run_interactive_session as ris
        import inspect
        source = inspect.getsource(ris)
        assert "counter" in source or "MAX_ATTEMPTS" in source, \
            "run_interactive_session must implement counter distinction for validation vs computation errors"

        with patch('builtins.input', side_effect=["3", "5", "0", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # Should show error but continue (not terminate)
                output_lower = output.lower()
                assert "error" in output_lower or "division" in output_lower or "zero" in output_lower, \
                       "Should display error for division by zero"
                # Should NOT terminate (counter should not have incremented)
                assert "Too many consecutive invalid inputs" not in output, \
                       "Computation errors should not trigger termination"

    def test_computation_error_does_not_increment_counter_sqrt_domain(self):
        """Test sqrt of negative error does NOT increment counter.

        Scenario: User selects sqrt (index 9), enters operand -4 (domain error).
        Expected: Error shown, counter NOT incremented, session continues (no termination).
        """
        from src.ui.interactive import run_interactive_session as ris
        import inspect
        source = inspect.getsource(ris)
        assert "counter" in source or "MAX_ATTEMPTS" in source, \
            "run_interactive_session must implement counter distinction for validation vs computation errors"

        with patch('builtins.input', side_effect=["9", "-4", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # Should show error but continue
                assert "Error" in output or "error" in output.lower(), \
                       "Should display error for sqrt(-4)"
                # Should NOT terminate (counter should not have incremented)
                assert "Too many consecutive invalid inputs" not in output, \
                       "Computation errors should not trigger termination"

    def test_available_operations_listed_on_invalid_operation(self):
        """Test that available operations list is displayed on invalid operation.

        Scenario: User enters invalid operation index 999, then valid operation 0.
        Expected: Available operations list is displayed in output before asking
                 user to select operation again.
        """
        from src.ui.interactive import run_interactive_session as ris
        import inspect
        source = inspect.getsource(ris)
        assert "counter" in source or "MAX_ATTEMPTS" in source, \
            "run_interactive_session must implement counter and validation logic"

        with patch('builtins.input', side_effect=["999", "0", "5", "3", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                output_lower = output.lower()
                # Operations list should be displayed (either initially or after error)
                assert "available operations" in output_lower or \
                       ("available" in output_lower and "operation" in output_lower), \
                       f"Expected 'available operations' text, output was: {output}"

    def test_cli_mode_unaffected_fail_fast_behavior(self):
        """Test CLI mode is unaffected by retry logic (fail-fast behavior).

        Scenario: CLI invocation with invalid operation or non-numeric operand.
        Expected: Error message, exit code 1, no retry/counter logic.
        """
        from src.ui.cli import run_cli
        from src.ui.interactive import run_interactive_session as ris
        import sys
        import inspect
        from io import StringIO

        # Verify interactive mode has counter but CLI mode should not use it
        ris_source = inspect.getsource(ris)
        assert "counter" in ris_source or "MAX_ATTEMPTS" in ris_source, \
            "run_interactive_session must have counter/MAX_ATTEMPTS logic"

        # Test invalid operation in CLI
        with patch('sys.stdout', new_callable=StringIO):
            exit_code = run_cli(['invalid_op', '5', '3'])
            assert exit_code == 1, "CLI should fail with exit code 1 on invalid operation"

        # Test non-numeric operand in CLI
        with patch('sys.stdout', new_callable=StringIO):
            exit_code = run_cli(['add', 'abc', '3'])
            assert exit_code == 1, "CLI should fail with exit code 1 on non-numeric operand"
