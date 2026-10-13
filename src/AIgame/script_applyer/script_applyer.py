import re
from typing import Any, Callable

from AIgame.game_objects import (
    GameObject,
)

Token = int | float | str | tuple[str, list["Token"]] | list["Token"]


class Utils:
    @staticmethod
    def indent(level: int, lines: list[str] | str) -> list[str]:
        INDENT: str = "    "

        indented: list[str] = []

        if isinstance(lines, list):
            for line in lines:
                indented.append(INDENT * level + line)
        else:
            indented.append(INDENT * level + lines)

        return indented

    @staticmethod
    def load_number(text: str, pos: int) -> tuple[int, int | float]:
        num: str = ""

        while (
            text[pos].isdigit()
            or text[pos] == "."
            or text[pos] == "-"
            or text[pos] == "+"
            or text[pos] == "e"
        ):
            num += text[pos]
            pos += 1

        fnum = float(num)
        return pos, int(fnum) if fnum == int(fnum) else fnum

    @staticmethod
    def get_name(expression: str, pos: int) -> tuple[int, str]:
        var = ""
        while expression[pos] not in "+-/*^%,()":
            var += expression[pos]
            pos += 1
        pos -= 1
        return pos, var


class ScriptApplyer:
    def __init__(self) -> None:
        self.line_data_extraction_pattern: re.Pattern[str] = re.compile(
            r"(\w+)\s*=\s*(.+)"
        )

    def update_script(self, gameObjects: list[GameObject]) -> None:
        dynamicClass: str = self._class_base()

        for obj in gameObjects:
            func: list[str] = []

            func.extend(Utils.indent(1, self._function_def(str(obj.id))))
            func.extend(Utils.indent(2, self._function_base()))
            func.extend(Utils.indent(2, self._function_body(obj.script)))

            func += Utils.indent(2, self._function_return())

            dynamicClass += "\n".join(func) + "\n"

        DynamicClass: type = self._interpreted_class(dynamicClass)
        self._set_functions(DynamicClass, gameObjects)

    def _class_base(self) -> str:
        return """
class Script:
    def __init__(self):
        self.reward = 0
        self.total_reward = 0
        self.level_name = ""
        self.inputs = []
        self.outputs = ()
"""

    def _function_def(self, name: str) -> str:
        return f"def f{name}(self):"

    def _function_base(self) -> str:
        return "data = {}"

    def _function_return(self) -> str:
        return "return data"

    def _function_body(self, script: str) -> list[str]:
        body: list[str] = []

        property_name: str | None = None
        expression: str | None = None
        for line in script.splitlines():
            if line == "":
                continue
            match = self.line_data_extraction_pattern.fullmatch(line)
            if match:
                property_name = match.group(1)
                expression = match.group(2)

            if (not property_name) or (not expression):
                raise Exception(f"line: {line}")

            body.append(f"data['{property_name}'] = {expression}")

        return body

    def _interpreted_class(self, dynamicClass: str) -> type:
        namespace: dict[str, Any] = {}
        try:
            exec(dynamicClass, namespace)
        except Exception as e:
            print(dynamicClass, e)

        return namespace["Script"]

    def _set_functions(self, DynamicClass: type, gameObjects: list[GameObject]) -> None:
        dynamicClass = DynamicClass()
        for obj in gameObjects:
            obj.data = getattr(dynamicClass, "f" + str(obj.id))()


class Functions:
    @staticmethod
    def avg(*args: float) -> float:
        return sum(args) / len(args)


class Context:
    global_variables: dict[str, float | str] = {
        "reward": 10,
        "total_reward": 100,
        "level_name": "level_name",
    }
    level_variables: list[float] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    functions: dict[str, Callable] = {
        "min": min,
        "max": max,
        "avg": Functions.avg,
        "round": round,
    }


class NewScriptApplyer:
    def __init__(self) -> None:
        self.context: Context = Context()

    def update_script(self, gameObjects: list[GameObject]) -> None:
        for obj in gameObjects:
            obj.data = self._process_obj(obj)

    def _process_obj(self, obj: GameObject) -> dict[str, object]:
        data: dict[str, Any] = {}
        for line in obj.script.splitlines():
            identifier: str = line.split()[0]
            _, tokens = self._tokenize_expression(
                " ".join(line.split()[2:])  # everything after "identifier = "
            )

            data[identifier] = self._run(tokens)
        return data

    def _tokenize_expression(
        self, expression: str, pos: int = -1
    ) -> tuple[int, list[Token]]:
        expression += " "
        tokens: list[Token] = []
        print(expression)
        while pos + 1 < len(expression):
            pos += 1
            if expression[pos] in ",)":
                break
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
                pos += 1  # (
                fargs: list[Token] = []
                while expression[pos] != ")":
                    pos, farg = self._tokenize_expression(expression, pos)
                    fargs.append(farg)
                tokens.append((fname, fargs))

            print(pos, expression[pos], tokens)

        return pos, tokens

    def _run(self, tokens: list[Token]) -> float:
        result: float = 0

        last_operator: str = "+"
        for token in tokens:
            if isinstance(token, float | int):
                match last_operator:
                    case "+":
                        result += token
                    case "-":
                        result -= token
                    case "*":
                        result *= token
                    case "/":
                        result /= token
                    case "^":
                        result **= token
                    case "%":
                        result %= token

        return result


if __name__ == "__main__":

    class DGameObject(GameObject):
        script = "x = #reward+max($0,$1)/2"
        id = 0
        name = ""
        data = {}

        def __init__(self) -> None: ...

        def draw(self) -> None: ...
        def contains_point(self, pos: tuple[int, int]) -> bool:
            return True

    sa = NewScriptApplyer()
    go = DGameObject()
    sa.update_script([go])
    print(go.data)
