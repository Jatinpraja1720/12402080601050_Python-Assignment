'''
Problem Statement: Build an interactive calculator that accepts formulas of the form operand operator operand. Operands may be
integers, decimals or previously stored variables. Supported operators are +, -, *, / and %. Invalid format, unknown variables, division by
zero and unsupported operators must raise separate custom exceptions. The calculator must continue until the user enters quit.
'''

class InvalidFormatError(Exception):
    pass


class UnknownVariableError(Exception):
    pass


class DivisionByZeroError(Exception):
    pass


class UnsupportedOperatorError(Exception):
    pass


variables = {}


def get_value(value):
    try:
        return float(value)
    except ValueError:
        if value in variables:
            return variables[value]

        raise UnknownVariableError()


def calculate(left, operator, right):

    left = get_value(left)
    right = get_value(right)

    if operator == "+":
        return left + right

    if operator == "-":
        return left - right

    if operator == "*":
        return left * right

    if operator == "/":
        if right == 0:
            raise DivisionByZeroError()

        return left / right

    if operator == "%":
        if right == 0:
            raise DivisionByZeroError()

        return left % right

    raise UnsupportedOperatorError()


while True:

    line = input()

    if line == "quit":
        break

    try:

        if "=" in line:

            parts = line.split("=")

            if len(parts) != 2:
                raise InvalidFormatError()

            name = parts[0].strip()
            value = parts[1].strip()

            if not name.isidentifier():
                raise InvalidFormatError()

            variables[name] = get_value(value)

        else:

            parts = line.split()

            if len(parts) != 3:
                raise InvalidFormatError()

            result = calculate(parts[0], parts[1], parts[2])

            if result.is_integer():
                result = int(result)

            print(result)

    except InvalidFormatError:
        print("InvalidFormatError")

    except UnknownVariableError:
        print("UnknownVariableError")

    except DivisionByZeroError:
        print("DivisionByZeroError")

    except UnsupportedOperatorError:
        print("UnsupportedOperatorError")
