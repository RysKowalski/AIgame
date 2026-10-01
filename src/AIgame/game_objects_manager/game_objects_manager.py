from __future__ import annotations

from AIgame.game_objects import GameObject
from AIgame.script_applyer import ScriptApplyer


class ObjectDoesNotExistError(Exception):
    def __init__(self, objectId: int) -> None:
        self.objectId: int = objectId
        super().__init__(f"object with ID {objectId} does not exist")


class GameObjectManager:
    def __init__(self) -> None:
        self._gameObjects: dict[int, GameObject] = {}
        self._inputObjects: dict[int, GameObject] = {}

        self._idCounter: int = 0

    def add(self, gameObject: GameObject) -> None:
        self._idCounter += 1
        gameObject.id = self._idCounter
        self._gameObjects[self._idCounter] = gameObject
        print(gameObject.id, type(gameObject))
        self.update_script()

    def delete(self, id: int) -> None:
        """throws ObjectDoesNotExistError"""
        try:
            del self._gameObjects[id]
        except KeyError:
            raise ObjectDoesNotExistError(id)

    def get(self, id: int) -> GameObject:
        """throws ObjectDoesNotExistError"""
        try:
            return self._gameObjects[id]
        except KeyError:
            raise ObjectDoesNotExistError(id)

    def draw(self) -> None:
        for gameObject in self._gameObjects.values():
            gameObject.run_script()
            gameObject.draw()

    def get_on_pos(self, pos: tuple[int, int]) -> GameObject | None:
        for obj in reversed(self._gameObjects.values()):
            if obj.contains_point(pos):
                return obj

    def update_script(self) -> None:
        ScriptApplyer().update_script(list(self._gameObjects.values()))
