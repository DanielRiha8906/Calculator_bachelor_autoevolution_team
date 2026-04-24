from .calculator import Calculator
from .interactive import run_interactive_session


def main():
    """Demo mode (preserved for backward compatibility; not called by entry point)."""
    calc = Calculator()
    print("Addition:", calc.add(10, 5))
    print("Subtraction:", calc.subtract(10, 5))
    print("Multiplication:", calc.multiply(10, 5))
    print("Division:", calc.divide(10, 5))
    print("Factorial:", calc.factorial(5))


if __name__ == "__main__":
    run_interactive_session()
