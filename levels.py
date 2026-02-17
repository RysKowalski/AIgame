from dataclasses import dataclass


@dataclass
class LevelData:
    startCutsceneID: str
    endCutsceneID: str
    inputCount: int


class GameLevel:
    id: str
    reward: float
    end: bool
    variables: list[float]
    levelData: LevelData

    def tick(self, inputs: list[float]) -> None: ...
