from game_objects import GameObject


class GameObjectStore:
    def __init__(self) -> None:
        self.gameObjects: dict[int, GameObject] = {}
        self._idCounter: int = 0

    def add(self, gameObject: GameObject) -> int:
        self._idCounter += 1
        gameObject.id = self._idCounter
        self.gameObjects[self._idCounter] = gameObject
        return self._idCounter

    def delete(self, id: int) -> None:
        del self.gameObjects[id]

    def get(self, id: int) -> GameObject:
        return self.gameObjects[id]

    def draw(self) -> None:
        for gameObject in self.gameObjects.values():
            gameObject.draw()

    def get_on_pos(self, pos: tuple[int, int]) -> int | None:
        for obj_id in reversed(self.gameObjects):
            obj: GameObject = self.gameObjects[obj_id]
            if obj.contains_point(pos):
                return obj_id
