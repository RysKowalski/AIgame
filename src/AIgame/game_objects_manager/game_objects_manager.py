from __future__ import annotations
from typing import TYPE_CHECKING

from AIgame import game_objects
from AIgame.script_applyer import ScriptApplyer

if TYPE_CHECKING:
    from AIgame.script_applyer import Context


class ObjectDoesNotExistError(Exception):
    def __init__(self, objectId: int) -> None:
        self.objectId: int = objectId
        super().__init__(f"object with ID {objectId} does not exist")


class GameObjectManager:
    def __init__(self, script_context: Context) -> None:
        self._script_applyer = ScriptApplyer(script_context)

        self._gameObjects: dict[int, game_objects.GameObject] = {}
        self._inputObjects: dict[int, game_objects.InputObject] = {}
        self._vizObjects: dict[int, game_objects.VizObject] = {}

        self._idCounter: int = 0

    def add(self, gameObject: game_objects.GameObject) -> None:
        self._idCounter += 1
        gameObject.id = self._idCounter

        if isinstance(gameObject, game_objects.InputObject):
            self._inputObjects[self._idCounter] = gameObject
        if isinstance(gameObject, game_objects.VizObject):
            self._vizObjects[self._idCounter] = gameObject

        self._gameObjects[self._idCounter] = gameObject
        self.update_script()

    def delete(self, id: int) -> None:
        """throws ObjectDoesNotExistError"""
        try:
            if isinstance(self._gameObjects[id], game_objects.InputObject):
                del self._inputObjects[id]
            if isinstance(self._gameObjects[id], game_objects.VizObject):
                del self._vizObjects[id]
            del self._gameObjects[id]

        except KeyError:
            raise ObjectDoesNotExistError(id)

    def get(self, id: int) -> game_objects.GameObject:
        """throws ObjectDoesNotExistError"""
        try:
            return self._gameObjects[id]
        except KeyError:
            raise ObjectDoesNotExistError(id)

    def draw(self) -> None:
        for gameObject in self._gameObjects.values():
            gameObject.draw()

    def get_on_pos(self, pos: tuple[int, int]) -> int | None:
        for obj in reversed(self._gameObjects.values()):
            if obj.contains_point(pos):
                return obj.id

    def update_script(self) -> None:
        self._script_applyer.update_script(list(self._gameObjects.values()))

    def process_event(self, event) -> None:
        for obj in self._inputObjects.values():
            obj.process_event(event)
