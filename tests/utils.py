from pygame import Surface

from AIgame.game_objects import GameObject
from AIgame.levels import GameLevel, LevelData, LevelState


class ExampleLevel(GameLevel):
    data = LevelData("test", 2, 100)

    def tick(self, state: LevelState, inputs: tuple[float, ...]) -> None:
        pass

    def check_and_set_end(self, state: LevelState) -> None:
        state.ended = state.reward > self.data.rewardTreshhold


BLANK_DEFAULT_SCRIPT: str = "default script"


def get_example_object() -> "ExampleObject":
    return ExampleObject(example_surface())


def example_surface() -> "Surface":
    return Surface((1, 1))


class BlankGameObject(GameObject):
    name = "ExampleObject"
    id = 0
    script = BLANK_DEFAULT_SCRIPT
    data = {}

    def __init__(self, screen: "Surface" = example_surface()) -> None:
        super().__init__(screen)

    def draw(self) -> None:
        pass

    def contains_point(self, pos: tuple[int, int]) -> bool:
        return False


class ExampleObject(GameObject):
    name = "ExampleObject"
    id = 0
    script = ""
    data = {}

    def __init__(self, screen: "Surface" = example_surface()) -> None:
        super().__init__(screen)
        self.draw_call_count: int = 0
        self.contains_point_count: int = 0
        self.contains_point_returns: bool = False

    def draw(self) -> None:
        self.draw_call_count += 1

    def contains_point(self, pos: tuple[int, int]) -> bool:
        pos[0]
        self.contains_point_count += 1
        return self.contains_point_returns

    def returns_true(self) -> None:
        self.contains_point_returns = True
