from __future__ import annotations

from typing import Any

from AIgame.script_engine.script_engine import ScriptSquareData, ScriptTextDisplayData
from .text_display import TextDisplayObject
from .square import SquareObject
from .game_objects import GameObject


class ScriptApplyer:
    def update_script(self, gameObjects: list[GameObject]) -> None:
        dynamicClass: str = self._get_class_base()

        for obj in gameObjects:
            func: str = ""
            func += self._get_function_def(str(obj.id))

            if isinstance(obj, SquareObject):
                func += self._get_func_body_square(obj)
            elif isinstance(obj, TextDisplayObject):
                func += self._get_func_body_text_display(obj)
            else:
                raise

            dynamicClass += func

        DynamicClass: type = self._get_executed_class(dynamicClass)
        self._set_functions(DynamicClass, gameObjects)

    def _get_class_base(self) -> str:
        return """
class Script:
    def __init__(self):
        self.reward = 0
        self.inputs = []
        self.outputs = ()
"""

    def _get_function_def(self, name: str) -> str:
        return f"    def f{name}(self):"

    def _get_func_body_square(self, obj: GameObject) -> str:
        body: str = ""
        body += self._get_square_function_base()
        for line in obj.script.splitlines():
            if line.startswith("this."):
                body += "        " + line[5:] + "\n"

        body += self._get_square_return()
        return body

    def _get_square_function_base(self) -> str:
        return """
        x = 0
        y = 0
        width = 100
        height = 100
        rotation = 0
        red = 255
        green = 255
        blue = 255
        border_width = 5
        border_red = 0
        border_green = 0
        border_blue = 0
"""

    def _get_square_return(self) -> str:
        return "        return ScriptSquareData(x, y, width, height, rotation, (red, green, blue), border_width, (border_red, border_green, border_blue))\n"

    def _get_func_body_text_display(self, obj: GameObject) -> str:
        body: str = ""
        body += self._get_text_display_function_base()
        for line in obj.script.splitlines():
            if line.startswith("this."):
                body += "        " + line[5:] + "\n"

        body += self._get_text_display_value_processing()
        body += self._get_text_display_return()
        return body

    def _get_text_display_function_base(self) -> str:
        return """
        y = 0
        value = 0
        round_digits = 2
        red = 155
        green = 155
        blue = 155
        text_red = 255
        text_green = 255
        text_blue = 255
"""

    def _get_text_display_value_processing(self) -> str:
        return """
        if round_digits > 0:
            final_value: str = str(round(value, round_digits))
        else:
            final_value = str(round(value))
"""

    def _get_text_display_return(self) -> str:
        return "        return ScriptTextDisplayData(x, y, (red, green, blue), (text_red, text_green, text_blue), final_value )\n"

    def _get_executed_class(self, dynamicClass: str) -> type:
        print(dynamicClass)
        namespace: dict[str, Any] = {
            "ScriptSquareData": ScriptSquareData,
            "ScriptTextDisplayData": ScriptTextDisplayData,
        }
        try:
            exec(dynamicClass, namespace)
        except Exception as e:
            print(dynamicClass, e)

        return namespace["Script"]

    def _set_functions(self, DynamicClass: type, gameObjects: list[GameObject]) -> None:
        dynamicClass = DynamicClass()
        for obj in gameObjects:
            obj.get_data = getattr(dynamicClass, "f" + str(obj.id))


class ObjectDoesNotExistError(Exception):
    def __init__(self, objectId: int) -> None:
        self.objectId: int = objectId
        super().__init__(f"object with ID {objectId} does not exist")


class GameObjectStore:
    def __init__(self) -> None:
        self._gameObjects: dict[int, GameObject] = {}
        self._idCounter: int = 0

    def add(self, gameObject: GameObject) -> int:
        self._idCounter += 1
        gameObject.id = self._idCounter
        self._gameObjects[self._idCounter] = gameObject
        print(gameObject.id, type(gameObject))
        self.update_script()
        return self._idCounter

    def delete(self, id: int) -> None:
        """throws ObjectDoesNotExistError"""
        try:
            del self._gameObjects[id]
        except KeyError:
            raise ObjectDoesNotExistError(id)
        self.update_script()

    def get(self, id: int) -> GameObject:
        """throws ObjectDoesNotExistError"""
        try:
            return self._gameObjects[id]
        except KeyError:
            raise ObjectDoesNotExistError(id)

    def draw(self) -> None:
        for gameObject in self._gameObjects.values():
            gameObject.draw()

    def get_on_pos(self, pos: tuple[int, int]) -> int | None:
        for obj_id in reversed(self._gameObjects):
            obj: GameObject = self._gameObjects[obj_id]
            if obj.contains_point(pos):
                return obj_id

    def update_script(self) -> None:
        ScriptApplyer().update_script(list(self._gameObjects.values()))
