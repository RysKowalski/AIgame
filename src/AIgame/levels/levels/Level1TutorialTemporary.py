from AIgame.levels import GameLevel, LevelData, LevelState


class Level1TutorialTemporary(GameLevel):
    def __init__(self) -> None:
        super().__init__(LevelData("tutorial1", 1, 100))

    def tick(self, state: LevelState, inputs: tuple[float, ...]) -> None:
        input: float = self._process_input(inputs)
        state.variables[0] += input
        state.variables[1] -= input / 2
        state.reward = sum(state.variables)
        self.check_and_set_end(state)

    def _process_input(self, inputs: tuple[float, ...]) -> float:
        maxValue: float = 10
        return min(inputs[0], maxValue)
