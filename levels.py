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


class Level1Tutorial(GameLevel):
    levelData = LevelData("none", "none", 1, 100)
    id = "tutorial1"

    def __init__(self) -> None:
        self.end = False
        self.variables = [0, 0]
        self.reward = 0

    def tick(self, inputs: tuple[float]) -> None:
        self.variables[0] += inputs[0]
        self.variables[1] -= inputs[0] / 2
        self.reward = sum(self.variables)

    def process_input(self, inputs: tuple[float]) -> float:
        maxValue: float = 10
        return min(inputs[0], maxValue)


if __name__ == "__main__":
    level: GameLevel = Level1Tutorial()
    print(level.levelData)
    for i in range(20):
        print(level.variables, level.reward)
        print()
        level.tick((5.0,))
