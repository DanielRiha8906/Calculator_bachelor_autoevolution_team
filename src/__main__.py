from .calculator import Calculator

def main():
    calc = Calculator()
    print("Addition:", calc.add(10, 5))
    print("Subtraction:", calc.subtract(10, 5))
    print("Multiplication:", calc.multiply(10, 5))
    print("Division:", calc.divide(10, 5))
    print("Factorial of 5:", calc.factorial(5))
    print("Factorial of 0:", calc.factorial(0))

if __name__ == "__main__":
    main()
