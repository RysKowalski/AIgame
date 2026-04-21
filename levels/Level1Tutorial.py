from .levels import GameLevel, LevelData


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
