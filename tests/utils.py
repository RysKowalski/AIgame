from pygame import Surface

from AIgame.game_objects import GameObject
from AIgame.levels import GameLevel, LevelData, LevelState
from AIgame.script_engine import ScriptEngine
from AIgame.script_engine.script_context import ScriptContext


class ExampleLevel(GameLevel):
    data = LevelData("test", 2, 100)

    def tick(self, state: LevelState, inputs: tuple[float, ...]) -> None:
        pass

    def check_and_set_end(self, state: LevelState) -> None:
        state.ended = state.reward > self.data.rewardTreshhold


BLANK_DEFAULT_SCRIPT: str = "default script"


class BlankGameObject(GameObject):
    name = "ExampleObject"
    id = 0

    def get_data() -> None:
        pass

    def draw(self) -> None:
        pass

    def get_default_script(self) -> str:
        return BLANK_DEFAULT_SCRIPT

    def contains_point(self, pos: tuple[int, int]) -> bool:
        return False


class ExampleObject(GameObject):
    name = "ExampleObject"
    id = 0

    def get_data() -> None:
        pass

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
        pos[0]
        self.contains_point_count += 1
        return self.contains_point_returns

    def returns_true(self) -> None:
        self.contains_point_returns = True


def get_example_object() -> ExampleObject:
    return ExampleObject("default", example_surface(), example_script_engine())


def example_script_engine() -> ScriptEngine:
    return ScriptEngine(ScriptContext(LevelState(0, 0, [0, 0], False)))


def example_surface() -> "Surface":
    return Surface((1, 1))
