"""Input validation utilities for the modular calculator (Issue #405).

Provides InputValidator with static methods for parsing and validating
user-supplied number strings.
"""


class InputValidator:
    """Static helpers for validating and parsing calculator input."""

    @staticmethod
    def parse_number(raw: str) -> int | float:
        """Parse a string as an integer or float.

        Tries integer parsing first; falls back to float.  Strips surrounding
        whitespace before parsing.

        Args:
            raw: The raw input string to parse.

        Returns:
            An int if the string represents a whole number without a decimal
            point, otherwise a float.

        Raises:
            ValueError: If the string cannot be interpreted as any numeric
                type.
        """
        raw = raw.strip()
        try:
            return int(raw)
        except ValueError:
            try:
                return float(raw)
            except ValueError:
                raise ValueError(f"Invalid number: {raw!r}")
