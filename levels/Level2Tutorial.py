from .levels import GameLevel, LevelData
from math import sin


class Level2Tutorial(GameLevel):
    def __init__(self) -> None:
        super().__init__(LevelData("tutorial1", 1, 200))
        self.variables = [0.0]

        self.tickCount: int = 0

    def tick(self, inputs: tuple[float]) -> None:
        self.variables[0] = 100 * sin(self.tickCount / 3)

        userValue: float = inputs[0]
        target: float = self.variables[0]
        noPointsRadius: int = 50
        maxScore: int = 30

        self.reward += maxScore * max(0, 1 - (abs(userValue - target / noPointsRadius)))
