from .calculator import Calculator
from .input_handler import run_session


def main():
    calc = Calculator()
    run_session(calc)


if __name__ == "__main__":
    main()
