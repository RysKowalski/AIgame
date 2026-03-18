# from script_engine import ScriptEngine
from script_engine import ScriptEngine, ScriptSquareData
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


def test_script_calculate_square_const_numbers() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    correctOutput: ScriptSquareData = ScriptSquareData(
        x=100,
        y=200,
        width=30,
        height=30,
        rotation=0,
        backgroundColor=(
            255,
            0,
            255,
        ),
        borderWidth=3,
        borderColor=(0, 100, 255),
    )
    script: str = f"""
        this.x = {correctOutput.x}
        this.y = {correctOutput.y}
        this.width = {correctOutput.width}
        this.height = {correctOutput.height}
        this.rotation = {correctOutput.rotation}
        this.red = {correctOutput.backgroundColor[0]}
        this.green = {correctOutput.backgroundColor[1]}
        this.blue = {correctOutput.backgroundColor[2]}
        this.border_width = {correctOutput.borderWidth}
        this.border_red = {correctOutput.borderColor[0]}
        this.border_green = {correctOutput.borderColor[1]}
        this.border_blue = {correctOutput.borderColor[2]}
    """

    output: ScriptSquareData = engine.calculate_square(script)

    assert output == correctOutput


def test_script_calculate_square_const_expressions() -> None:
    level: TestLevel = TestLevel()
    level.variables[0] = 6
    level.variables[1] = 3
    engine: ScriptEngine = ScriptEngine(level)
    correctOutput: ScriptSquareData = ScriptSquareData(
        x=3,
        y=6,
        width=30,
        height=30,
        rotation=0,
        backgroundColor=(
            255,
            255,
            50,
        ),
        borderWidth=4,
        borderColor=(110, 56, 2),
    )
    script: str = """
        this.x = $0 / 2
        this.y = $1 * 2
        this.width = 15 + 15
        this.height = 12 + 18
        this.rotation = 3 / 2 - 1.5
        this.red = 100 + 100 + 55
        this.green = 100 + 55 + 100
        this.blue = 100 / 2
        this.border_width = 2 + 2
        this.border_red = 55 + 55
        this.border_green = 66 - 10
        this.border_blue = $0 / $1
    """

    output: ScriptSquareData = engine.calculate_square(script)

    assert output == correctOutput


def test_script_calculate_square_missing_assignations() -> None:
    level: TestLevel = TestLevel()
    engine: ScriptEngine = ScriptEngine(level)
    correctOutput: ScriptSquareData = ScriptSquareData(
        x=-1,
        y=-1,
        width=-1,
        height=-1,
        rotation=-1,
        backgroundColor=(
            -1,
            -1,
            -1,
        ),
        borderWidth=-1,
        borderColor=(-1, -1, -1),
    )
    script: str = ""

    output: ScriptSquareData = engine.calculate_square(script)

    assert output == correctOutput
