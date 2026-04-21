from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class LevelData:
    id: str
    inputCount: int
    rewardTreshhold: float


class GameLevel(ABC):
    def __init__(self, levelData: "LevelData") -> None:
        self.levelData: LevelData = levelData
        self.reward: float = 0
        self.end: bool = False
        self.variables: list[float] = []

    @abstractmethod
    def tick(self, inputs: tuple) -> None: ...

    def check_and_set_end(self) -> None:
        if self.reward > self.levelData.rewardTreshhold:
            self.end = True
        else:
            self.end = False
