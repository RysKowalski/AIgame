import pytest

from script_engine.script_context import InvalidVariableError, ScriptContext
from tests.utils import ExampleLevel


def test_resolve_variable_existing_var() -> None:
    level: ExampleLevel = ExampleLevel()
    correctVariableValue: float = 5.5
    level.variables[0] = correctVariableValue
    context: ScriptContext = ScriptContext(level)

    output: float = context.resolve_variable("$0")

    assert output == correctVariableValue


def test_resolve_variable_nonexisting_var_throws_invalid_variable_error() -> None:
    level: ExampleLevel = ExampleLevel()
    context: ScriptContext = ScriptContext(level)

    token: str = "$1234"

    with pytest.raises(InvalidVariableError) as exc:
        context.resolve_variable(token)

    assert str(exc.value) == f"invalid token '{token}'. variable does not exist"


def test_resolve_variable_invalid_var_throws_invalid_variable_error() -> None:
    level: ExampleLevel = ExampleLevel()
    context: ScriptContext = ScriptContext(level)

    token: str = "clearly invalid"

    with pytest.raises(InvalidVariableError) as exc:
        context.resolve_variable(token)

    assert str(exc.value) == f"invalid token '{token}'. variable must start with '$'"


def test_resolve_variable_get_reward() -> None:
    level: ExampleLevel = ExampleLevel()
    correctReward: float = 123.4
    level.reward = correctReward
    context: ScriptContext = ScriptContext(level)

    output: float = context.resolve_variable("$reward")

    assert output == correctReward
