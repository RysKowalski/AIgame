# from script_engine import ScriptEngine
from etsts import ScriptEngine
from levels import GameLevel, LevelData


class TestLevel(GameLevel):
    levelData = LevelData("none", "none", 2, 100)
    id = "test"

    def __init__(self) -> None:
        self.end = False
        self.variables = [0, 0]
        self.reward = 0

    def process_input(self, inputs: tuple[float]) -> float:
        maxValue: float = 10
        return min(inputs[0], maxValue)


def test_script_calculate_expression_empty() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = ""
    correctOutput: float = 0

    output: float = engine.calculate_expression(expression)

    assert output == correctOutput


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


def test_script_calculate_expression_power() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "2 ^ 3"
    correctOutput: float = 8.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_three_numbers() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "2 + 2 * 2"
    correctOutput: float = 6.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_parentheses() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "2 + ( 2 * 2 )"
    correctOutput: float = 6.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_two_parentheses() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "( 2 * 2 ) - ( 2 * 3 )"
    correctOutput: float = -2.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_nested_parentheses() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "( ( ( ( ( ( 4 ) ) ) * ( 2 ) ) ) )"
    correctOutput: float = 8.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_subtraction() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "3 - 2"
    correctOutput: float = 1

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_division() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "3 / 2"
    correctOutput: float = 1.5

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_division_by_zero() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "3 / 0"
    correctOutput: float = 0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_multiplication() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "3 * 2"
    correctOutput: float = 6.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_modulo() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "3 % 2"
    correctOutput: float = 1.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_function_max() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "max [ 1, 2, 3, ]"
    correctOutput: float = 3.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_function_min() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "min [ 1, 2, 3 ]"
    correctOutput: float = 1.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_function_with_calculation() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "2 + max [ 1, 2, 3 ]"
    correctOutput: float = 5.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_nested_function() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "max [ 1, min ( 2, 4 ), 3 ]"
    correctOutput: float = 3

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_calculation_inside_function() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    expression: str = "max [ 1, 2 + 3 * ( 3 / 2 ), 3 ]"
    correctOutput: float = 6.5

    output = engine.calculate_expression(expression)

    assert output == correctOutput
