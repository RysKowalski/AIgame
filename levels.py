from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class LevelData:
    startCutsceneID: str
    endCutsceneID: str
    inputCount: int
    rewardTreshhold: float


class GameLevel:
    id: str
    reward: float
    end: bool
    variables: list[float]
    levelData: LevelData

    def tick(self, inputs: tuple) -> None: ...

    def check_and_set_end(self) -> None:
        if self.reward > self.levelData.rewardTreshhold:
            self.end = True
        else:
            self.end = False


class Level1Tutorial(GameLevel):
    levelData = LevelData("none", "none", 1, 100)
    id = "tutorial1"

    def __init__(self) -> None:
        self.end = False
        self.variables = [0, 0]
        self.reward = 0

    def tick(self, inputs: tuple[float]) -> None:
        input: float = self.process_input(inputs)
        self.variables[0] += input
        self.variables[1] -= input / 2
        self.reward = sum(self.variables)
        self.check_and_set_end()

    def process_input(self, inputs: tuple[float]) -> float:
        maxValue: float = 10
        return min(inputs[0], maxValue)


if __name__ == "__main__":
    level: GameLevel = Level1Tutorial()
    print(level.levelData)
    while not level.end:
        print(level.variables, level.reward)
        print()
        level.tick((1,))
