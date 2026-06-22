from typing import Any
import re

from AIgame.game_objects import (
    GameObject,
)


class ScriptApplyer:
    def __init__(self) -> None:
        self.line_data_extraction_pattern: re.Pattern[str] = re.compile(
            r"this\.(\w+)\s*=\s*(.+)"
        )

    def update_script(self, gameObjects: list[GameObject]) -> None:
        dynamicClass: str = self._class_base()

        for obj in gameObjects:
            func: list[str] = []

            func.extend(self._indent(1, self._function_def(str(obj.id))))
            func.extend(self._indent(2, self._function_base()))
            func.extend(self._indent(2, self._function_body(obj.script)))

            func += self._indent(2, self._function_return())

            dynamicClass += "\n".join(func) + "\n"

        DynamicClass: type = self._interpreted_class(dynamicClass)
        self._set_functions(DynamicClass, gameObjects)

    def _class_base(self) -> str:
        return """
class Script:
    def __init__(self):
        self.reward = 0
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
            if line.startswith("this."):
                match = self.line_data_extraction_pattern.fullmatch(line)
                if match:
                    property_name = match.group(1)
                    expression = match.group(2)

            if (not property_name) or (not expression):
                raise

            body.append(f"data['{property_name}'] = {expression}")

        return body

    def _indent(self, level: int, lines: list[str] | str) -> list[str]:
        INDENT: str = "    "

        indented: list[str] = []

        if isinstance(lines, list):
            for line in lines:
                indented.append(INDENT * level + line)
        else:
            indented.append(INDENT * level + lines)

        return indented

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
            obj.get_data = getattr(dynamicClass, "f" + str(obj.id))
