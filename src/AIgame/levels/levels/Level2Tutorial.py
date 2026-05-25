from AIgame.levels import GameLevel, LevelData, LevelState
from math import sin


class Level2Tutorial(GameLevel):
    data = LevelData("tutorial2", 1, 200)

    def tick(self, state: LevelState, inputs: tuple[float, ...]) -> None:
        state.variables[0] = 100 * sin(state.tick_count / 3)

        userValue: float = inputs[0]
        target: float = state.variables[0]
        noPointsRadius: int = 50
        maxScore: int = 30

        state.reward += maxScore * max(
            0, 1 - (abs(userValue - target) / noPointsRadius)
        )

        self.check_and_set_end(state)

    def check_and_set_end(self, state: LevelState) -> None:
        state.ended = state.reward > self.data.rewardTreshhold
