from AIgame.levels import LevelManager

from .utils import example_script_engine


def test_load_level() -> None:  # TODO: end
    manager: LevelManager = LevelManager("tutorial1", example_script_engine())
