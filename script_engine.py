from dataclasses import dataclass


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
    def __init__(self) -> None:
        
