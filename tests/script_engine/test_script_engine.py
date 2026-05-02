from script_engine import ScriptEngine, ScriptSquareData
from script_engine.script_context import ScriptContext
from script_engine.script_engine import ScriptInputObjectData, ScriptTextDisplayData
from tests.utils import ExampleLevel


def test_script_calculate_expression_empty() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = ""
    correctOutput: float = 0

    output: float = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_single_number() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "132.058"
    correctOutput: float = float(expression)

    output: float = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_number_addition() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "3.5 + 4.2"
    correctOutput: float = 7.7

    output: float = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_single_variable() -> None:
    level: ExampleLevel = ExampleLevel()
    level.variables[0] = 0.6
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "$0"
    correctOutput: float = 0.6

    output: float = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_variable_addition() -> None:
    level: ExampleLevel = ExampleLevel()
    level.variables[0] = 0.6
    level.variables[1] = 0.4
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "$0 + $1"
    correctOutput: float = 1.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_power() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "2 ^ 3"
    correctOutput: float = 8.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_three_numbers() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "2 + 2 * 2"
    correctOutput: float = 6.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_parentheses() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "2 + ( 2 * 2 )"
    correctOutput: float = 6.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_two_parentheses() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "( 2 * 2 ) - ( 2 * 3 )"
    correctOutput: float = -2.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_nested_parentheses() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "( ( ( ( ( ( 4 ) ) ) * ( 2 ) ) ) )"
    correctOutput: float = 8.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_subtraction() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "3 - 2"
    correctOutput: float = 1

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_division() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "3 / 2"
    correctOutput: float = 1.5

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_division_by_zero() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "3 / 0"
    correctOutput: float = 0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_multiplication() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "3 * 2"
    correctOutput: float = 6.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_modulo() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "3 % 2"
    correctOutput: float = 1.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_function_max() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "max [ 1, 2, 3, ]"
    correctOutput: float = 3.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_function_min() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "min [ 1, 2, 3 ]"
    correctOutput: float = 1.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_function_with_calculation() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "2 + max [ 1, 2, 3 ]"
    correctOutput: float = 5.0

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_nested_function() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "max [ 1, min ( 2, 4 ), 3 ]"
    correctOutput: float = 3

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_expression_calculation_inside_function() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    expression: str = "max [ 1, 2 + 3 * ( 3 / 2 ), 3 ]"
    correctOutput: float = 6.5

    output = engine.calculate_expression(expression)

    assert output == correctOutput


def test_script_calculate_square_const_numbers() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
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
    level: ExampleLevel = ExampleLevel()
    level.variables[0] = 6
    level.variables[1] = 3
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
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
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
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


def test_script_expression_variable_reward() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    level.reward = 123.456
    correctOutput: float = 123.456
    script: str = "$reward"

    output: float = engine.calculate_expression(script)

    assert output == correctOutput


def test_get_data_empty() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))

    output: dict[str, float] = engine.get_data("")

    assert output == {}


def test_get_data_multiple_data() -> None:
    level: ExampleLevel = ExampleLevel()
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    script: str = """
        this.var1 = 123
        this.var2 = 456
        this.var3 = 789
    """

    output: dict[str, float] = engine.get_data(script)

    assert output == {"var1": 123, "var2": 456, "var3": 789}


def test_calculate_text_display() -> None:
    level: ExampleLevel = ExampleLevel()
    level.variables[0] = 6
    level.variables[1] = 3
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    correctOutput: ScriptTextDisplayData = ScriptTextDisplayData(
        x=10.0,
        y=10.0,
        backgroundColor=(255, 255, 255),
        textColor=(0, 0, 0),
        value="0.0",
    )
    script: str = """
        this.x = 10
        this.y = 10
        this.red = 255
        this.green = 255
        this.blue = 255
        this.text_red = 0
        this.text_green = 0
        this.text_blue = 0
        this.value = 0
        this.round = 1
    """

    output: ScriptTextDisplayData = engine.calculate_text_display(script)

    assert output == correctOutput


def test_calculate_text_display_invalid_rounding_defaults_0() -> None:
    level: ExampleLevel = ExampleLevel()
    level.variables[0] = 6
    level.variables[1] = 3
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    correctOutput: ScriptTextDisplayData = ScriptTextDisplayData(
        x=10.0,
        y=10.0,
        backgroundColor=(255, 255, 255),
        textColor=(0, 0, 0),
        value="0",
    )
    script: str = """
        this.x = 10
        this.y = 10
        this.red = 255
        this.green = 255
        this.blue = 255
        this.text_red = 0
        this.text_green = 0
        this.text_blue = 0
        this.value = 0
        this.round = 0
    """

    output: ScriptTextDisplayData = engine.calculate_text_display(script)

    assert output == correctOutput


def test_calculate_input_object() -> None:
    level: ExampleLevel = ExampleLevel()
    level.variables[0] = 6
    level.variables[1] = 3
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    correctOutput: ScriptInputObjectData = ScriptInputObjectData(
        x=10.0,
        y=10.0,
        padding=0,
        borderWidth=0,
        backgroundColor=(255, 255, 255),
        textColor=(0, 0, 0),
        fontSize=1,
        borderColor=(100, 100, 100),
        value="0.0",
    )
    script: str = """
        this.x = 10
        this.y = 10
        this.padding = 0
        this.text_size = 1
        this.red = 255
        this.green = 255
        this.blue = 255
        this.text_red = 0
        this.text_green = 0
        this.text_blue = 0
        this.border_width = 0
        this.border_red = 100
        this.border_green = 100
        this.border_blue = 100
        this.value = 0
        this.round = 1
    """

    output: ScriptInputObjectData = engine.calculate_input_object(script)

    assert output == correctOutput


def test_calculate_input_object_invalid_rounding_defaults_0() -> None:
    level: ExampleLevel = ExampleLevel()
    level.variables[0] = 6
    level.variables[1] = 3
    engine: ScriptEngine = ScriptEngine(ScriptContext(level))
    correctOutput: ScriptInputObjectData = ScriptInputObjectData(
        x=10.0,
        y=10.0,
        padding=0,
        borderWidth=0,
        backgroundColor=(255, 255, 255),
        textColor=(0, 0, 0),
        fontSize=1,
        borderColor=(100, 100, 100),
        value="0",
    )
    script: str = """
        this.x = 10
        this.y = 10
        this.padding = 0
        this.text_size = 1
        this.red = 255
        this.green = 255
        this.blue = 255
        this.text_red = 0
        this.text_green = 0
        this.text_blue = 0
        this.border_width = 0
        this.border_red = 100
        this.border_green = 100
        this.border_blue = 100
        this.value = 0
        this.round = 0
    """

    output: ScriptInputObjectData = engine.calculate_input_object(script)

    assert output == correctOutput
