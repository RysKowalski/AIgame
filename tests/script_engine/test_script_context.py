import pytest

from levels import LevelState
from script_engine.script_context import InvalidVariableError, ScriptContext


def test_resolve_variable_existing_var() -> None:
    state: LevelState = LevelState(0, 0, [0], False)
    correctVariableValue: float = 5.5
    state.variables[0] = correctVariableValue
    context: ScriptContext = ScriptContext(state)

    output: float = context.resolve_variable("$0")

    assert output == correctVariableValue


def test_resolve_variable_nonexisting_var_throws_invalid_variable_error() -> None:
    state: LevelState = LevelState(0, 0, [], False)
    context: ScriptContext = ScriptContext(state)

    token: str = "$1234"

    with pytest.raises(InvalidVariableError) as exc:
        context.resolve_variable(token)

    assert str(exc.value) == f"invalid token '{token}'. variable does not exist"


def test_resolve_variable_invalid_var_throws_invalid_variable_error() -> None:
    state: LevelState = LevelState(0, 0, [], False)
    context: ScriptContext = ScriptContext(state)

    token: str = "clearly invalid"

    with pytest.raises(InvalidVariableError) as exc:
        context.resolve_variable(token)

    assert str(exc.value) == f"invalid token '{token}'. variable must start with '$'"


def test_resolve_variable_get_reward() -> None:
    state: LevelState = LevelState(0, 0, [], False)
    correctReward: float = 123.4
    state.reward = correctReward
    context: ScriptContext = ScriptContext(state)

    output: float = context.resolve_variable("$reward")

    assert output == correctReward
