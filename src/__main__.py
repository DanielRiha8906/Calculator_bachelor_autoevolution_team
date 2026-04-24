from .cli import run_calculator, display_error


def main() -> None:
    """Entry point for the interactive calculator CLI."""
    try:
        run_calculator()
    except ZeroDivisionError:
        display_error("Division by zero is not allowed.")
    except Exception as e:
        display_error(str(e))


if __name__ == "__main__":
    main()
