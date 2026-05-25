from AIgame.game_objects.square import SquareObject
from .game_objects import GameObject


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
        dynamicClass: str = """
class Script:
    def __init__(self):
        self.reward = 0
        self.inputs = []
        self.outputs = ()"""

        for obj in self._gameObjects.values():
            if not isinstance(obj, SquareObject):
                continue
            funcBody: str = """
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
            for line in obj.script.splitlines():
                if line.startswith("this."):
                    funcBody += line[5:] + "\n"
            funcBody += """
return ScriptSquareData(x, y, width, height, rotation, (red, green, blue), border_width, (border_red, border_green, border_blue)
            """

            dynamicClass += f"    def {obj.id}:"
            for line in funcBody:
                dynamicClass += "        " + line + "\n"
