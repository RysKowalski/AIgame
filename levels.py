class CutsceneText: ...


class GameLevel:
    id: str
    reward: float
    end: bool
    startCutscene: CutsceneText
    endCutscene: CutsceneText
    variables: list[float]
    inputCount: int

    def tick(self, inputs: list[float]) -> None: ...
