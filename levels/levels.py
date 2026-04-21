from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class LevelData:
    startCutsceneID: str
    endCutsceneID: str
    inputCount: int
    rewardTreshhold: float


class GameLevel(ABC):
    id: str
    reward: float
    end: bool
    variables: list[float]
    levelData: LevelData

    @abstractmethod
    def tick(self, inputs: tuple) -> None: ...

    def check_and_set_end(self) -> None:
        if self.reward > self.levelData.rewardTreshhold:
            self.end = True
        else:
            self.end = False
