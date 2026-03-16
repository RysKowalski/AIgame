from game_objects import GameObject


class GameObjectStore:
    def __init__(self) -> None:
        self.gameObjects: dict[int, GameObject] = {}
        self.idCounter: int = 0

    def add(self, gameObject: GameObject) -> None:
        gameObject.id = self.idCounter
        self.gameObjects[self.idCounter] = gameObject
        self.idCounter += 1

    def delete(self, id: int) -> None:
        del self.gameObjects[id]

    def get(self, id: int) -> GameObject:
        return self.gameObjects[id]

    def draw(self) -> None:
        for gameObject in self.gameObjects.values():
            gameObject.draw()
