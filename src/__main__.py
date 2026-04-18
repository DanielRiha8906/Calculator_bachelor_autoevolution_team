from .core import Calculator
from .session import run_session


def main():
    calc = Calculator()
    run_session(calc)


if __name__ == "__main__":
    main()
