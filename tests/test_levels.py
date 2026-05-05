from levels import GameLevel, LevelState
from .utils import ExampleLevel


def test_GameLevel_check_and_set_end_over() -> None:
    level: GameLevel = ExampleLevel()
    state: LevelState = LevelState(0, 0, [], False)
    state.reward = level.data.rewardTreshhold + 1

    level.check_and_set_end(state)

    assert state.ended


def test_GameLevel_check_and_set_end_under() -> None:
    level: GameLevel = ExampleLevel()
    state: LevelState = LevelState(0, 0, [], False)
    state.reward = level.data.rewardTreshhold - 1

    level.check_and_set_end(state)

    assert not state.ended
