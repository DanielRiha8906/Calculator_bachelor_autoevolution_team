"""Entry point for ``python -m src``.

Delegates to the modular calculator implementation in src.calculator.main.
"""

from src.calculator.main import cli_mode

if __name__ == "__main__":
    cli_mode()
