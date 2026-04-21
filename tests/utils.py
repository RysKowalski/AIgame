from pygame import Surface
from script_engine import ScriptEngine
from levels import GameLevel, LevelData
from game_objects import GameObject
from script_engine.script_context import ScriptContext


class ExampleLevel(GameLevel):
    levelData = LevelData("none", "none", 2, 100)
    id = "test"

    def __init__(self) -> None:
        self.end = False
        self.variables = [0, 0]
        self.reward = 0

    def tick(self, inputs: tuple) -> None:
        pass


class ExampleObject(GameObject):
    def __init__(
        self, script: str, screen: "Surface", scriptEngine: ScriptEngine
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
    return ExampleObject("default", example_surface(), example_script_engine())


def example_script_engine() -> ScriptEngine:
    return ScriptEngine(ScriptContext(ExampleLevel()))


def example_surface() -> "Surface":
    return Surface((1, 1))
