from AIgame.game_objects import GameObject
from .utils import BLANK_DEFAULT_SCRIPT, BlankGameObject
from unittest.mock import MagicMock


def test_game_object_set_script() -> None:
    expectedScript: str = "expected"

    gameObject: GameObject = BlankGameObject(expectedScript, MagicMock())

    assert gameObject.script == expectedScript


def test_game_object_set_script_default() -> None:
    gameObject: GameObject = BlankGameObject("default", MagicMock())

    assert gameObject.script == BLANK_DEFAULT_SCRIPT
