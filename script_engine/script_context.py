from levels import LevelState


class InvalidVariableError(Exception):
    def __init__(self, token: str, reason: str) -> None:
        super().__init__(f"invalid token '{token}'. {reason}")


class ScriptContext:
    """Holds runtime data and resolves variables/functions"""

    def __init__(self, state: LevelState) -> None:
        self.levelState: LevelState = state

    def resolve_variable(self, token: str) -> float:
        if not token.startswith("$"):
            raise InvalidVariableError(token, "variable must start with '$'")

        variable: str = token[1:]

        if variable == "reward":
            return self.levelState.reward

        variableIndex: int = int(variable)

        if variableIndex < 0:
            raise InvalidVariableError(token, "variable does not exist")

        try:
            return self.levelState.variables[variableIndex]
        except IndexError:
            raise InvalidVariableError(token, "variable does not exist")
