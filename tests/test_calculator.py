import pytest
import math
from src.calculator import Calculator


class TestDivisionInvalidInputs:
    """Test suite for division with invalid/incorrect inputs."""

    @pytest.fixture
    def calc(self):
        """Fixture providing a Calculator instance."""
        return Calculator()

    def test_divide_by_string_numerator(self, calc):
        """Verify TypeError when numerator is a string."""
        with pytest.raises(TypeError):
            calc.divide("10", 2)

    def test_divide_by_string_denominator(self, calc):
        """Verify TypeError when denominator is a string."""
        with pytest.raises(TypeError):
            calc.divide(10, "2")

    def test_divide_string_by_string(self, calc):
        """Verify TypeError with both operands as strings."""
        with pytest.raises(TypeError):
            calc.divide("10", "2")

    def test_divide_by_none_numerator(self, calc):
        """Verify TypeError when numerator is None."""
        with pytest.raises(TypeError):
            calc.divide(None, 2)

    def test_divide_by_none_denominator(self, calc):
        """Verify TypeError when denominator is None."""
        with pytest.raises(TypeError):
            calc.divide(10, None)

    def test_divide_by_zero(self, calc):
        """Verify ZeroDivisionError is raised."""
        with pytest.raises(ZeroDivisionError):
            calc.divide(10, 0)

    def test_divide_by_list(self, calc):
        """Verify TypeError when denominator is a list."""
        with pytest.raises(TypeError):
            calc.divide(10, [2])

    def test_divide_by_dict(self, calc):
        """Verify TypeError when denominator is a dict."""
        with pytest.raises(TypeError):
            calc.divide(10, {"value": 2})

    def test_divide_by_custom_object(self, calc):
        """Verify TypeError when denominator is a custom object without numeric behavior."""
        class CustomObject:
            pass

        with pytest.raises(TypeError):
            calc.divide(10, CustomObject())