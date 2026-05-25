from typing import TYPE_CHECKING
from .GameLevel import GameLevel, LevelState
from .levels import Level1Tutorial, Level2Tutorial, Level1TutorialTemporary

from AIgame.script_engine import ScriptContext

if TYPE_CHECKING:
    from AIgame.script_engine import ScriptEngine


defaultLevels: dict[str, type[GameLevel]] = {
    Level1TutorialTemporary.data.name: Level1TutorialTemporary,
    Level1Tutorial.data.name: Level1Tutorial,
    Level2Tutorial.data.name: Level2Tutorial,
}


class LevelManager:
    def __init__(
        self,
        levelName: str,
        scriptEngine: "ScriptEngine",
        levels: dict[str, type[GameLevel]] = defaultLevels,
    ):
        self.scriptEngine = scriptEngine
        self.levels: dict[str, type[GameLevel]] = levels
        self.levelNames: list[str] = list(levels.keys())
        self._set_level(levelName)

    def tick(self, inputs: tuple[float, ...]):
        self.level.tick(self.levelState, inputs)
        if self.levelState.ended:
            self._next_level()

    def _set_level(self, levelName) -> None:
        self.level: GameLevel = self.levels[levelName]()
        self.levelState: LevelState = LevelState(
            0, 0, [0 for _ in range(self.level.data.inputCount)], False
        )
        self.scriptEngine.context = ScriptContext(self.levelState)

    def _next_level(self) -> None:
        currentIndex: int = self.levelNames.index(self.level.data.name)
        if currentIndex == len(self.levelNames) - 1:
            self._set_level(self.levelNames[0])
            return

        nextName: str = self.levelNames[currentIndex + 1]
        self._set_level(nextName)
