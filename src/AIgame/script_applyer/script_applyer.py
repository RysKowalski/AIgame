from typing import Callable

from AIgame.game_objects import (
    GameObject,
)

Token = int | float | str | tuple[str, list["Token"]] | list["Token"]


class Utils:
    @staticmethod
    def load_number(text: str, pos: int) -> tuple[int, int | float]:
        num: str = ""

        while text[pos].isdigit() or text[pos] == "." or text[pos] == "-":
            num += text[pos]
            pos += 1

        fnum = float(num)
        return pos, int(fnum) if fnum == int(fnum) else fnum

    @staticmethod
    def get_name(expression: str, pos: int) -> tuple[int, str]:
        var = ""
        while expression[pos] not in "+-/*^%,() ":
            var += expression[pos]
            pos += 1
        pos -= 1
        return pos, var


class Context:
    global_variables: dict[str, float | str] = {
        "reward": 10,
        "total_reward": 100,
    }
    level_variables: list[float] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    functions: dict[str, Callable[..., float]] = {
        "min": min,
        "max": max,
        "avg": lambda args: sum(args) / len(args),
        "round": round,
    }


class ScriptApplyer:
    def __init__(self, context: Context) -> None:
        self.context: Context = context

    def update_script(self, gameObjects: list[GameObject]) -> None:
        for obj in gameObjects:
            obj.data = self._process_obj(obj)

    def _process_obj(self, obj: GameObject) -> dict[str, object]:
        data: dict[str, object] = {}
        for line in obj.script.splitlines():
            identifier: str = line.split()[0]
            expression: str = " ".join(line.split()[2:])  # ignoring first part
            expression += " "  # adding padding for tokenizing
            _, tokens = self._tokenize_expression(expression)

            data[identifier] = self._run(tokens)
        return data

    def _tokenize_expression(
        self, expression: str, pos: int = -1
    ) -> tuple[int, list[Token]]:
        tokens: list[Token] = []
        while pos + 1 < len(expression):
            pos += 1

            if expression[pos] in ",)":
                return pos, tokens

            elif expression[pos] == "$":
                pos += 1
                pos, var = Utils.get_name(expression, pos)
                tokens.append(self.context.level_variables[int(var)])

            elif expression[pos] == "#":
                pos += 1
                pos, var = Utils.get_name(expression, pos)
                tokens.append(self.context.global_variables[var])

            elif expression[pos] in "+-/*^%":
                tokens.append(expression[pos])

            elif expression[pos].isdigit():
                pos, n = Utils.load_number(expression, pos)
                tokens.append(n)

            elif expression[pos] == " ":
                continue

            else:
                pos, fname = Utils.get_name(expression, pos)
                pos += 1
                fargs: list[Token] = []
                while pos < len(expression):
                    if expression[pos] == ")":
                        break

                    pos, farg = self._tokenize_expression(expression, pos)
                    fargs.extend(farg)
                    pos -= 1

                    if pos < len(expression) and expression[pos] == ",":
                        pos += 1

                    elif pos < len(expression) and expression[pos] == ")":
                        break

                    else:
                        raise ValueError(f"Expected ',' or ')' at position {pos}")
                tokens.append((fname, fargs))

        return pos, tokens

    def _run(self, tokens: list[Token]) -> float:
        values: list[float] = []
        operators: list[str] = []

        last_operator: str = "+"

        for token in tokens:
            if isinstance(token, float | int):
                values.append(float(token))
                operators.append(last_operator)
            elif isinstance(token, str):
                if token in "+-*/^%":
                    last_operator = token
            elif isinstance(token, tuple):
                fargs: list[float] = [self._run([t]) for t in token[1]]
                fresult: float = Context.functions[token[0]](fargs)
                values.append(fresult)
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
