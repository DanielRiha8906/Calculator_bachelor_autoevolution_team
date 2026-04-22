"""Integration tests for CLI mode using subprocess and mocking."""

import pytest
import subprocess
import sys
from unittest.mock import patch, MagicMock
from src.__main__ import main
from src.cli_handler import CLIHandler
from src.operations import OperationRegistry
from src.calculator import Calculator


class TestCLIIntegrationViaSubprocess:
    """Integration tests using subprocess.run to invoke CLI."""

    def test_cli_add_operation(self):
        """Test CLI mode with add operation."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "add", "5", "3"],
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0
        assert "Result: 8.0" in result.stdout

    def test_cli_subtract_operation(self):
        """Test CLI mode with subtract operation."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "subtract", "10", "3"],
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0
        assert "Result: 7.0" in result.stdout

    def test_cli_multiply_operation(self):
        """Test CLI mode with multiply operation."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "multiply", "4", "5"],
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0
        assert "Result: 20.0" in result.stdout

    def test_cli_divide_operation(self):
        """Test CLI mode with divide operation."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "divide", "10", "2"],
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0
        assert "Result: 5.0" in result.stdout

    def test_cli_factorial_operation(self):
        """Test CLI mode with factorial (unary) operation."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "factorial", "5"],
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0
        assert "Result: 120" in result.stdout

    def test_cli_square_operation(self):
        """Test CLI mode with square (unary) operation."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "square", "5"],
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0
        assert "Result: 25.0" in result.stdout

    def test_cli_square_root_operation(self):
        """Test CLI mode with square_root (unary) operation."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "square_root", "16"],
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0
        assert "Result: 4.0" in result.stdout

    def test_cli_divide_by_zero_error(self):
        """Test CLI mode handles divide by zero error."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "divide", "5", "0"],
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 1
        assert "Error:" in result.stderr

    def test_cli_unknown_operation_error(self):
        """Test CLI mode handles unknown operation error."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "unknown_op", "5", "3"],
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 1
        assert "Error:" in result.stderr

    def test_cli_invalid_operand_error(self):
        """Test CLI mode handles invalid operand error."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "add", "abc", "3"],
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 1
        assert "Error:" in result.stderr

    def test_cli_missing_operand_error(self):
        """Test CLI mode handles missing operand error."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "add", "5"],
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 1
        assert "Error:" in result.stderr

    def test_cli_negative_operands(self):
        """Test CLI mode with negative operands."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "add", "-5", "-3"],
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0
        assert "Result: -8.0" in result.stdout

    def test_cli_float_operands(self):
        """Test CLI mode with float operands."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "multiply", "2.5", "4.0"],
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0
        assert "Result: 10.0" in result.stdout


class TestCLIIntegrationViaMocking:
    """Integration tests using sys.argv mocking and sys.exit with side_effect."""

    def _run_cli_test(self, args, expected_stdout=None, expected_stderr=None, expected_exit_code=0):
        """Helper method to run CLI test with mocked sys.argv and sys.exit."""
        import sys
        from src.__main__ import main

        with patch("sys.argv", args):
            with patch("sys.exit", side_effect=SystemExit(expected_exit_code)) as mock_exit:
                try:
                    main()
                except SystemExit as e:
                    pass
                return mock_exit

    def test_cli_add_via_mock(self, capsys):
        """Test CLI mode with add operation via mocking."""
        with patch("sys.argv", ["calculator", "add", "5", "3"]):
            with patch("sys.exit", side_effect=SystemExit(0)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Result: 8.0" in captured.out

    def test_cli_subtract_via_mock(self, capsys):
        """Test CLI mode with subtract operation via mocking."""
        with patch("sys.argv", ["calculator", "subtract", "10", "3"]):
            with patch("sys.exit", side_effect=SystemExit(0)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Result: 7.0" in captured.out

    def test_cli_divide_via_mock(self, capsys):
        """Test CLI mode with divide operation via mocking."""
        with patch("sys.argv", ["calculator", "divide", "10", "2"]):
            with patch("sys.exit", side_effect=SystemExit(0)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Result: 5.0" in captured.out

    def test_cli_square_via_mock(self, capsys):
        """Test CLI mode with square operation via mocking."""
        with patch("sys.argv", ["calculator", "square", "5"]):
            with patch("sys.exit", side_effect=SystemExit(0)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Result: 25.0" in captured.out

    def test_cli_factorial_via_mock(self, capsys):
        """Test CLI mode with factorial operation via mocking."""
        with patch("sys.argv", ["calculator", "factorial", "5"]):
            with patch("sys.exit", side_effect=SystemExit(0)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Result: 120" in captured.out

    def test_cli_divide_by_zero_via_mock(self, capsys):
        """Test CLI mode handles divide by zero error via mocking."""
        with patch("sys.argv", ["calculator", "divide", "5", "0"]):
            with patch("sys.exit", side_effect=SystemExit(1)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_cli_unknown_operation_via_mock(self, capsys):
        """Test CLI mode handles unknown operation error via mocking."""
        with patch("sys.argv", ["calculator", "unknown_op", "5", "3"]):
            with patch("sys.exit", side_effect=SystemExit(1)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_cli_invalid_operand_via_mock(self, capsys):
        """Test CLI mode handles invalid operand error via mocking."""
        with patch("sys.argv", ["calculator", "add", "abc", "3"]):
            with patch("sys.exit", side_effect=SystemExit(1)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_cli_missing_operand_via_mock(self, capsys):
        """Test CLI mode handles missing operand error via mocking."""
        with patch("sys.argv", ["calculator", "add", "5"]):
            with patch("sys.exit", side_effect=SystemExit(1)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_cli_negative_operands_via_mock(self, capsys):
        """Test CLI mode with negative operands via mocking."""
        with patch("sys.argv", ["calculator", "add", "-5", "-3"]):
            with patch("sys.exit", side_effect=SystemExit(0)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Result: -8.0" in captured.out

    def test_cli_float_operands_via_mock(self, capsys):
        """Test CLI mode with float operands via mocking."""
        with patch("sys.argv", ["calculator", "multiply", "2.5", "4.0"]):
            with patch("sys.exit", side_effect=SystemExit(0)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Result: 10.0" in captured.out

    def test_cli_power_operation_via_mock(self, capsys):
        """Test CLI mode with power operation via mocking."""
        with patch("sys.argv", ["calculator", "power", "2", "10"]):
            with patch("sys.exit", side_effect=SystemExit(0)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Result: 1024.0" in captured.out

    def test_cli_square_root_via_mock(self, capsys):
        """Test CLI mode with square_root operation via mocking."""
        with patch("sys.argv", ["calculator", "square_root", "16"]):
            with patch("sys.exit", side_effect=SystemExit(0)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Result: 4.0" in captured.out

    def test_cli_cube_via_mock(self, capsys):
        """Test CLI mode with cube operation via mocking."""
        with patch("sys.argv", ["calculator", "cube", "3"]):
            with patch("sys.exit", side_effect=SystemExit(0)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Result: 27.0" in captured.out

    def test_cli_log_via_mock(self, capsys):
        """Test CLI mode with log operation via mocking."""
        with patch("sys.argv", ["calculator", "log", "100"]):
            with patch("sys.exit", side_effect=SystemExit(0)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Result: 2.0" in captured.out


class TestCLIEdgeCases:
    """Edge case tests for CLI integration."""

    def test_cli_square_root_negative_error(self, capsys):
        """Test CLI mode handles square root of negative error."""
        with patch("sys.argv", ["calculator", "square_root", "-1"]):
            with patch("sys.exit", side_effect=SystemExit(1)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_cli_factorial_negative_error(self, capsys):
        """Test CLI mode handles factorial of negative error."""
        with patch("sys.argv", ["calculator", "factorial", "-1"]):
            with patch("sys.exit", side_effect=SystemExit(1)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_cli_ln_zero_error(self, capsys):
        """Test CLI mode handles ln of zero error."""
        with patch("sys.argv", ["calculator", "ln", "0"]):
            with patch("sys.exit", side_effect=SystemExit(1)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_cli_log_negative_error(self, capsys):
        """Test CLI mode handles log of negative error."""
        with patch("sys.argv", ["calculator", "log", "-5"]):
            with patch("sys.exit", side_effect=SystemExit(1)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_cli_too_many_operands(self, capsys):
        """Test CLI mode handles too many operands error."""
        with patch("sys.argv", ["calculator", "add", "5", "3", "extra"]):
            with patch("sys.exit", side_effect=SystemExit(1)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_cli_unary_with_two_operands(self, capsys):
        """Test CLI mode handles unary operation with two operands."""
        with patch("sys.argv", ["calculator", "square", "5", "3"]):
            with patch("sys.exit", side_effect=SystemExit(1)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_cli_power_zero_negative_exponent(self, capsys):
        """Test CLI mode handles 0^(-n) error."""
        with patch("sys.argv", ["calculator", "power", "0", "-1"]):
            with patch("sys.exit", side_effect=SystemExit(1)):
                try:
                    main()
                except SystemExit:
                    pass
        captured = capsys.readouterr()
        assert "Error:" in captured.err
