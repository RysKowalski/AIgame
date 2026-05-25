from typing import TYPE_CHECKING
from .GameLevel import GameLevel, LevelState
from .levels import Level1Tutorial, Level2Tutorial, Level1TutorialTemporary

from AIgame.script_engine import ScriptContext

if TYPE_CHECKING:
    from AIgame.script_engine import ScriptEngine


levels: dict[str, type[GameLevel]] = {
    Level1TutorialTemporary.data.name: Level1TutorialTemporary,
    Level1Tutorial.data.name: Level1Tutorial,
    Level2Tutorial.data.name: Level2Tutorial,
}

levelNames: list[str] = [
    Level1TutorialTemporary.data.name,
    Level2Tutorial.data.name,
    Level2Tutorial.data.name,
]


class LevelManager:  # TODO: end
    def __init__(self, levelName: str, scriptEngine: "ScriptEngine"):
        self.scriptEngine = scriptEngine
        self._set_level(levelName)

    def tick(self, inputs: tuple[float, ...]):
        self.level.tick(self.levelState, inputs)
        print(
            self.level.data.rewardTreshhold,
            self.levelState.reward,
            self.levelState.ended,
        )
        if self.levelState.ended:
            self._next_level()

    def _set_level(self, levelName) -> None:
        self.level: GameLevel = levels[levelName]()
        self.levelState: LevelState = LevelState(
            0, 0, [0 for _ in range(self.level.data.inputCount)], False
        )
        self.scriptEngine.context = ScriptContext(self.levelState)
        print(levelName)

    def _next_level(self) -> None:
        currentIndex: int = levelNames.index(self.level.data.name)
        if currentIndex >= len(levelNames) - 1:
            self._set_level(levelNames[0])
        nextName: str = levelNames[currentIndex + 1]
        self._set_level(nextName)
