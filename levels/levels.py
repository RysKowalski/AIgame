from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class LevelData:
    id: str
    inputCount: int
    rewardTreshhold: float


@dataclass
class LevelState:
    reward: float
    tick_count: int
    variables: list[float]
    ended: bool


class GameLevel(ABC):
    def __init__(self, data: LevelData) -> None:
        self.data: LevelData = data

    @abstractmethod
    def tick(self, state: LevelState, inputs: tuple[float, ...]) -> None: ...

    def check_and_set_end(self, state: LevelState) -> None:
        state.ended = state.reward > self.data.rewardTreshhold
