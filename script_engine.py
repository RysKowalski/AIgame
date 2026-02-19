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
        code: list[str] = expression.split()

        if len(code) == 1:
            if code[0][0] == "$":
                return self.get_variable(code[0])
            else:
                try:
                    return float(code[0])
                except ValueError:
                    return 0.0

        return 0.0

    def get_variable(self, variable: str) -> float:
        variableIndex: int = int(variable[1:])
        return self.game.variables[variableIndex]
