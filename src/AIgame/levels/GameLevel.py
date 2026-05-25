from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LevelData:
    name: str
    inputCount: int
    rewardTreshhold: float


@dataclass
class LevelState:
    reward: float
    tick_count: int
    variables: list[float]
    ended: bool


class GameLevel(Protocol):
    data: LevelData

    def tick(self, state: LevelState, inputs: tuple[float, ...]) -> None: ...

    def check_and_set_end(self, state: LevelState) -> None: ...
