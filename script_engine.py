from dataclasses import dataclass
from levels import GameLevel


@dataclass(frozen=True)
class ScriptSquareData:
    x: float
    y: float
    width: float
    height: float
    rotation: float
    backgroundColor: tuple[float, float, float]
    borderWidth: float
    borderColor: tuple[float, float, float]


class ScriptEngine:
    def __init__(self, game: GameLevel) -> None:
        self.game: GameLevel = game
        self.globalVariables: dict[str, float] = {}

    def calculate_expression(self, expression: str) -> float:
        """
        $1 + $2 / 3
        """
        ...
