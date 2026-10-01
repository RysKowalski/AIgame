from .Level1Tutorial import Level1Tutorial
from .Level1TutorialTemporary import Level1TutorialTemporary
from .Level2Tutorial import Level2Tutorial

from AIgame.levels import GameLevel

defaultLevels: dict[str, type[GameLevel]] = {
    Level1TutorialTemporary.data.name: Level1TutorialTemporary,
    Level1Tutorial.data.name: Level1Tutorial,
    Level2Tutorial.data.name: Level2Tutorial,
}

__all__ = ["Level1Tutorial", "Level1TutorialTemporary", "Level2Tutorial"]
