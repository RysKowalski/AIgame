from game_objects import GameObjectStore, GameObject


class ExampleObject(GameObject):
    def draw(self) -> None:
        pass

    def get_default_script(self) -> str:
        return "0"

    def contains_point(self, pos: tuple[int, int]) -> bool:
        return pos == (0, 0)


# def test_add_and_get() -> None:
#     exampleObject: GameObject = ExampleObject("default", None, None)
#     objectStore: GameObjectStore
