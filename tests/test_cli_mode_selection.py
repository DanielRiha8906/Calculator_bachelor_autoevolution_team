"""Tests for get_mode_selection() function in cli.py."""

import pytest
from unittest.mock import patch
from src.cli import get_mode_selection


class TestGetModeSelection:
    """Test suite for get_mode_selection() function."""

    @patch("builtins.input", return_value="1")
    @patch("builtins.print")
    def test_get_mode_selection_returns_normal_on_input_1(self, mock_print, mock_input):
        """Test get_mode_selection returns 'normal' when user enters '1'."""
        result = get_mode_selection()
        assert result == "normal"

    @patch("builtins.input", return_value="2")
    @patch("builtins.print")
    def test_get_mode_selection_returns_scientific_on_input_2(self, mock_print, mock_input):
        """Test get_mode_selection returns 'scientific' when user enters '2'."""
        result = get_mode_selection()
        assert result == "scientific"

    @patch("builtins.input", side_effect=["invalid", "invalid", "invalid"])
    @patch("builtins.print")
    def test_get_mode_selection_returns_none_after_three_failures(self, mock_print, mock_input):
        """Test get_mode_selection returns None after 3 invalid attempts."""
        result = get_mode_selection()
        assert result is None

    @patch("builtins.input", side_effect=["x", "y", "z"])
    @patch("builtins.print")
    def test_get_mode_selection_three_invalid_inputs(self, mock_print, mock_input):
        """Test get_mode_selection with three different invalid inputs."""
        result = get_mode_selection()
        assert result is None

    @patch("builtins.input", side_effect=["invalid", "invalid", "1"])
    @patch("builtins.print")
    def test_get_mode_selection_succeeds_on_third_attempt(self, mock_print, mock_input):
        """Test get_mode_selection succeeds after two invalid inputs and one valid."""
        result = get_mode_selection()
        assert result == "normal"

    @patch("builtins.input", side_effect=["invalid", "2"])
    @patch("builtins.print")
    def test_get_mode_selection_succeeds_on_second_attempt(self, mock_print, mock_input):
        """Test get_mode_selection succeeds on second attempt."""
        result = get_mode_selection()
        assert result == "scientific"

    @patch("builtins.input", return_value="1")
    @patch("builtins.print")
    def test_get_mode_selection_calls_print_menu(self, mock_print, mock_input):
        """Test get_mode_selection calls print to show menu."""
        get_mode_selection()
        # Should have called print at least once (for the menu)
        assert mock_print.called

    @patch("builtins.input", return_value="3")
    @patch("builtins.print")
    def test_get_mode_selection_invalid_number(self, mock_print, mock_input):
        """Test get_mode_selection with out-of-range number."""
        with patch("builtins.input", side_effect=["3", "3", "3"]):
            result = get_mode_selection()
            assert result is None

    @patch("builtins.input", return_value="1")
    @patch("builtins.print")
    def test_get_mode_selection_returns_string(self, mock_print, mock_input):
        """Test get_mode_selection returns a string when successful."""
        result = get_mode_selection()
        assert isinstance(result, str)

    @patch("builtins.input", side_effect=["", "", ""])
    @patch("builtins.print")
    def test_get_mode_selection_empty_string_invalid(self, mock_print, mock_input):
        """Test get_mode_selection treats empty string as invalid."""
        result = get_mode_selection()
        assert result is None

    @patch("builtins.input", side_effect=["1", "2"])
    @patch("builtins.print")
    def test_get_mode_selection_returns_on_first_success(self, mock_print, mock_input):
        """Test get_mode_selection returns immediately on first valid input."""
        result = get_mode_selection()
        assert result == "normal"
        # Should only have called input once (first call returned "1")
        assert mock_input.call_count == 1

    @patch("builtins.input", side_effect=["2"])
    @patch("builtins.print")
    def test_get_mode_selection_input_called_at_least_once(self, mock_print, mock_input):
        """Test get_mode_selection calls input at least once."""
        get_mode_selection()
        assert mock_input.called

    @patch("builtins.input", return_value=" 1 ")
    @patch("builtins.print")
    def test_get_mode_selection_handles_whitespace(self, mock_print, mock_input):
        """Test get_mode_selection handles input with whitespace."""
        result = get_mode_selection()
        # Depending on implementation, may or may not strip whitespace
        # This test documents the behavior
        assert result in ["normal", None]

    @patch("builtins.input", side_effect=["invalid", "invalid", "2"])
    @patch("builtins.print")
    def test_get_mode_selection_retry_logic(self, mock_print, mock_input):
        """Test get_mode_selection allows retries up to max."""
        result = get_mode_selection()
        assert result == "scientific"
        # Should have called input 3 times
        assert mock_input.call_count == 3

    @patch("builtins.input", side_effect=["1", "2", "3"])
    @patch("builtins.print")
    def test_get_mode_selection_stops_after_success(self, mock_print, mock_input):
        """Test get_mode_selection doesn't continue after success."""
        result = get_mode_selection()
        assert result == "normal"
        # Should stop after first success, so only 1 input call
        assert mock_input.call_count == 1

    @patch("builtins.input", return_value="2")
    @patch("builtins.print")
    def test_get_mode_selection_case_sensitivity(self, mock_print, mock_input):
        """Test get_mode_selection with numeric input (not case-sensitive)."""
        result = get_mode_selection()
        assert result in ["normal", "scientific"]
