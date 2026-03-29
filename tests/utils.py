import pygame
from script_engine import ScriptEngine
from levels import GameLevel, LevelData
from game_objects import GameObject


class TestLevel(GameLevel):
    levelData = LevelData("none", "none", 2, 100)
    id = "test"

    def __init__(self) -> None:
        self.end = False
        self.variables = [0, 0]
        self.reward = 0

    def process_input(self, inputs: tuple[float]) -> float:
        maxValue: float = 10
        return min(inputs[0], maxValue)


class ExampleObject(GameObject):
    def __init__(
        self, script: str, screen: pygame.Surface, scriptEngine: ScriptEngine
    ) -> None:
        super().__init__(script, screen, scriptEngine)
        self.draw_call_count: int = 0
        self.contains_point_count: int = 0
        self.contains_point_returns: bool = False

    def draw(self) -> None:
        self.draw_call_count += 1

    def get_default_script(self) -> str:
        return "0"

    def contains_point(self, pos: tuple[int, int]) -> bool:
        self.contains_point_count += 1
        return self.contains_point_returns


def get_example_object() -> ExampleObject:
    return ExampleObject("default", test_surface(), test_script_engine())


def test_script_engine() -> ScriptEngine:
    return ScriptEngine(TestLevel())


def test_surface() -> pygame.Surface:
    return pygame.Surface((1, 1))
