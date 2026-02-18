from script_engine import ScriptEngine
from levels import GameLevel, LevelData


class TestLevel(GameLevel):
    levelData = LevelData("none", "none", 2, 100)
    id = "test"

    def __init__(self) -> None:
        self.end = False
        self.variables = [0, 0]
        self.reward = 0

    def tick(self, inputs: tuple[float]) -> None:
        input: float = self.process_input(inputs)
        self.variables[0] += input
        self.variables[1] -= input / 2
        self.reward = sum(self.variables)
        self.check_and_set_end()

    def process_input(self, inputs: tuple[float]) -> float:
        maxValue: float = 10
        return min(inputs[0], maxValue)


def test_script_calculate_expression_single_number() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "132.058"
    correctOutput: float = float(expression)

    output: float = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_number_addition() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "3.5 + 4.2"
    correctOutput: float = 7.7

    output: float = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_single_variable() -> None:
    level: TestLevel = TestLevel()
    level.variables[0] = 0.6
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "$0"
    correctOutput: float = 0.6

    output: float = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_variable_addition() -> None:
    level: TestLevel = TestLevel()
    level.variables[0] = 0.6
    level.variables[1] = 0.4
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "$0 + $1"
    correctOutput: float = 1.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput
