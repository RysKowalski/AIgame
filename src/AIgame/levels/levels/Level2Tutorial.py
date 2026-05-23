from AIgame.levels import GameLevel, LevelData, LevelState
from math import sin


class Level2Tutorial(GameLevel):
    def __init__(self) -> None:
        super().__init__(LevelData("tutorial1", 1, 200))

    def tick(self, state: LevelState, inputs: tuple[float, ...]) -> None:
        state.variables[0] = 100 * sin(state.tick_count / 3)

        userValue: float = inputs[0]
        target: float = state.variables[0]
        noPointsRadius: int = 50
        maxScore: int = 30

        state.reward += maxScore * max(
            0, 1 - (abs(userValue - target) / noPointsRadius)
        )
