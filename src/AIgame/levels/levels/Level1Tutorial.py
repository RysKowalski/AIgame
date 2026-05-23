from AIgame.levels import GameLevel, LevelData, LevelState


class Level1Tutorial(GameLevel):
    def __init__(self) -> None:
        super().__init__(LevelData("tutorial1", 1, 100))

    def tick(self, state: LevelState, inputs: tuple[float, ...]) -> None:
        state.reward += inputs[0]
