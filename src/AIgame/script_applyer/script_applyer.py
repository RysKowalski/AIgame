from collections.abc import Callable
from typing import TYPE_CHECKING

from .utils import Utils

if TYPE_CHECKING:
    from AIgame.game_objects import GameObject

    from .context import Context

Token = int | float | str | tuple[str, list[list["Token"]]]


class ScriptApplyer:
    def __init__(self, context: "Context") -> None:
        self._context: "Context" = context

    def update_script(self, gameObjects: list["GameObject"]) -> None:
        for obj in gameObjects:
            obj.data = self._process_obj(obj)

    def _process_obj(self, obj: "GameObject") -> dict[str, object]:
        data: dict[str, object] = {}
        for line_number, line in enumerate(obj.script.splitlines()):
            parts: list[str] = line.split(maxsplit=2)

            if not parts:
                continue

            if len(parts) != 3 or parts[1] != "=":
                raise ValueError(f"Invalid assignment at line {line_number}: {line}")

            identifier: str = parts[0]
            expression: str = parts[2]

            _, tokens = self._tokenize_expression(expression)

            data[identifier] = self._run(tokens)
        return data

    def _tokenize_expression(
        self, expression: str, pos: int = 0
    ) -> tuple[int, list[Token]]:

        tokens: list[Token] = []

        while pos < len(expression):
            char: str = expression[pos]

            if char.isspace():
                pos += 1
                continue

            if char == ")":
                break

            if char == ",":
                pos += 1
                continue

            if char in "+-*/^%":
                tokens.append(char)
                pos += 1
                continue

            if char.isdigit() or char == ".":
                pos, number = Utils.load_number(expression, pos)
                tokens.append(number)
                continue

            if char in "$#":
                variable_type: str = char
                pos += 1

                pos, name = Utils.get_name(expression, pos)

                if not name:
                    raise ValueError("Expected variable name")

                if variable_type == "$":
                    index: int = int(name)

                    if not 0 <= index < len(self._context.level_variables):
                        raise IndexError(f"Invalid level variable: {index}")

                    tokens.append(self._context.level_variables[index])

                else:
                    if name not in self._context.global_variables:
                        raise NameError(f"Unknown variable: {name}")

                    value = self._context.global_variables[name]

                    if not isinstance(value, (int, float)):
                        raise TypeError(f"Variable {name} is not numeric")

                    tokens.append(value)

                continue

            pos, name = Utils.get_name(expression, pos)

            if not name:
                raise ValueError(f"Unexpected character {char!r} at position {pos}")

            if name not in self._context.functions:
                raise NameError(f"Unknown function: {name}")

            while pos < len(expression) and expression[pos].isspace():
                pos += 1

            if pos >= len(expression) or expression[pos] != "(":
                raise ValueError(f"Expected '(' after function {name}")

            pos += 1

            args: list[list[Token]] = []

            while True:
                while pos < len(expression) and expression[pos].isspace():
                    pos += 1

                if pos >= len(expression):
                    raise ValueError(f"Unclosed function call: {name}")

                if expression[pos] == ")":
                    pos += 1
                    break

                pos, arg = self._tokenize_expression(expression, pos)

                if not arg:
                    raise ValueError(f"Empty argument in function {name}")

                args.append(arg)

                while pos < len(expression) and expression[pos].isspace():
                    pos += 1

                if pos >= len(expression):
                    raise ValueError(f"Unclosed function call: {name}")

                if expression[pos] == ")":
                    pos += 1
                    break

                if expression[pos] == ",":
                    pos += 1
                    break

                raise ValueError(f"Expected ',' or ')' at position {pos}")

            tokens.append((name, args))

        return pos, tokens

    def _run(self, tokens: list[Token]) -> float:
        values: list[float] = []
        operators: list[str] = []

        last_operator: str = "+"

        for token in tokens:
            if isinstance(token, (float, int)):
                values.append(float(token))
                operators.append(last_operator)

            elif isinstance(token, str):
                last_operator = token

            elif isinstance(token, tuple):
                name, args = token

                function: Callable[..., float] = self._context.functions[name]

                print(tokens)
                print(args)
                fargs: list[float] = [self._run([arg]) for arg in args[0]]

                result: float = function(fargs)

                values.append(float(result))
                operators.append(last_operator)

        if not values:
            return 0.0

        index: int = 1
        while index < len(values):
            operator: str = operators[index]

            if operator in ("*", "/", "%", "^"):
                left: float = values[index - 1]
                right: float = values[index]

                match operator:
                    case "*":
                        result: float = left * right
                    case "/":
                        result = left / right
                    case "%":
                        result = left % right
                    case "^":
                        result = left**right

                values[index - 1] = result
                del values[index]
                del operators[index]
            else:
                index += 1

        result: float = values[0]

        for index in range(1, len(values)):
            match operators[index]:
                case "+":
                    result += values[index]
                case "-":
                    result -= values[index]

        return result
