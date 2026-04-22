from .core.calculator import Calculator
from .cli import interactive_session

def main():
    calc = Calculator()
    interactive_session(calc)

if __name__ == "__main__":
    main()
