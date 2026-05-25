from AIgame.levels import GameLevel, LevelData, LevelState


class Level1Tutorial(GameLevel):
    data = LevelData("tutorial1", 1, 100)

    def tick(self, state: LevelState, inputs: tuple[float, ...]) -> None:
        state.reward += inputs[0]
        self.check_and_set_end(state)

    def check_and_set_end(self, state: LevelState) -> None:
        state.ended = state.reward > self.data.rewardTreshhold
