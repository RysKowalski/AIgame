from levels.levels import GameLevel
from .utils import ExampleLevel


def test_GameLevel_check_and_set_end_over() -> None:
    level: GameLevel = ExampleLevel()
    level.reward = level.levelData.rewardTreshhold + 1

    level.check_and_set_end()

    assert level.end


def test_GameLevel_check_and_set_end_under() -> None:
    level: GameLevel = ExampleLevel()
    level.reward = level.levelData.rewardTreshhold - 1

    level.check_and_set_end()

    assert not level.end
