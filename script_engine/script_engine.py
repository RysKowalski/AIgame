from __future__ import annotations
from dataclasses import dataclass
from .script_context import ScriptContext


@dataclass(frozen=True)
class ScriptSquareData:
    x: float
    y: float
    width: float
    height: float
    rotation: float
    backgroundColor: tuple[int, int, int]
    borderWidth: float
    borderColor: tuple[int, int, int]


@dataclass(frozen=True)
class ScriptTextDisplayData:
    x: float
    y: float
    backgroundColor: tuple[int, int, int]
    textColor: tuple[int, int, int]
    value: str


class ScriptEngine:
    """VIBE CODED :sob: this is really really bad"""

    _ARGUMENT_SENTINEL: str = "__ARG_START__"

    def __init__(self, context: ScriptContext) -> None:
        self.context: ScriptContext = context

    def calculate_expression(self, expression: str) -> float:
        if self._is_empty_expression(expression):
            return 0.0
        tokens: list[str] = self._tokenize_expression(expression)
        rpn: list[str] = self._convert_tokens_to_reverse_polish_notation(tokens)
        return self._evaluate_reverse_polish_notation(rpn)

    def _is_empty_expression(self, expression: str) -> bool:
        return expression.strip() == ""

    def _tokenize_expression(self, expression: str) -> list[str]:
        tokens: list[str] = []
        current: str = ""

        for ch in expression:
            if ch.isspace():
                self._flush_token(tokens, current)
                current = ""
            elif ch in "+-*/%^(),[]":
                self._flush_token(tokens, current)
                current = ""
                tokens.append(ch)
            else:
                current += ch

        self._flush_token(tokens, current)
        return tokens

    def _flush_token(self, tokens: list[str], token: str) -> None:
        if token:
            tokens.append(token)

    def _convert_tokens_to_reverse_polish_notation(
        self, tokens: list[str]
    ) -> list[str]:
        output: list[str] = []
        stack: list[str] = []

        for token in tokens:
            if self._is_number(token) or self._is_variable(token):
                output.append(token)
            elif self._is_function(token):
                stack.append(token)
            elif token == ",":
                while stack and stack[-1] not in ("(", "["):
                    output.append(stack.pop())
            elif self._is_operator(token):
                self._pop_operators_by_precedence(token, stack, output)
                stack.append(token)
            elif token in ("(", "["):
                if stack and self._is_function(stack[-1]):
                    output.append(self._ARGUMENT_SENTINEL)
                stack.append(token)
            elif token in (")", "]"):
                if token == ")":
                    opening: str = "("
                else:
                    opening: str = "["

                while stack and stack[-1] != opening:
                    output.append(stack.pop())
                stack.pop()
                if stack and self._is_function(stack[-1]):
                    output.append(stack.pop())
            else:
                raise ValueError(token)

        while stack:
            output.append(stack.pop())

        return output

    def _evaluate_reverse_polish_notation(self, rpn: list[str]) -> float:
        stack: list[float | str] = []

        for token in rpn:
            if token == self._ARGUMENT_SENTINEL:
                stack.append(token)
            elif self._is_number(token):
                stack.append(float(token))
            elif self._is_variable(token):
                stack.append(self.context.resolve_variable(token))
            elif self._is_operator(token):
                right: float = float(stack.pop())
                left: float = float(stack.pop())
                stack.append(self._apply_operator(token, left, right))
            elif self._is_function(token):
                self._apply_function(token, stack)
            else:
                raise ValueError(token)

        return float(stack[0]) if stack else 0.0

    def _apply_function(self, name: str, stack: list[float | str]) -> None:
        args: list[float] = []

        while stack:
            value = stack.pop()
            if value == self._ARGUMENT_SENTINEL:
                break
            args.append(float(value))

        if name == "max":
            stack.append(max(args))
        elif name == "min":
            stack.append(min(args))
        else:
            raise ValueError(name)

    def _apply_operator(self, op: str, a: float, b: float) -> float:
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if op == "/":
            return 0.0 if b == 0 else a / b
        if op == "%":
            return 0.0 if b == 0 else a % b
        if op == "^":
            return a**b
        raise ValueError(op)

    def _pop_operators_by_precedence(
        self,
        operator: str,
        stack: list[str],
        output: list[str],
    ) -> None:
        precedence: dict[str, int] = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "%": 2,
            "^": 3,
        }

        while (
            stack
            and stack[-1] in precedence
            and (
                precedence[stack[-1]] > precedence[operator]
                or (precedence[stack[-1]] == precedence[operator] and operator != "^")
            )
        ):
            output.append(stack.pop())

    def _is_number(self, token: str) -> bool:
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _is_variable(self, token: str) -> bool:
        return token.startswith("$")

    def _is_operator(self, token: str) -> bool:
        return token in "+-*/%^"

    def _is_function(self, token: str) -> bool:
        return token in ("max", "min")

    def get_data(self, script: str) -> dict[str, float]:
        output: dict[str, float] = {}
        lines: list[str] = script.splitlines()
        for rawLine in lines:
            line: str = rawLine.strip()
            if line == "":
                continue

            if line.startswith("this."):
                firstSpaceIndex: int = line.find(" ")
                value: float = self.calculate_expression(
                    line[firstSpaceIndex + 3 :]
                )  # cut out " = "

                output[line[5:firstSpaceIndex]] = (
                    value  # text after "this." before space
                )

        return output

    def calculate_square(self, script: str) -> ScriptSquareData:
        data: dict[str, float] = self.get_data(script)

        x: float = data.get("x", -1.0)
        y: float = data.get("y", -1)
        width: float = data.get("width", -1)
        height: float = data.get("height", -1)
        rotation: float = data.get("rotation", -1)
        backgroundRed: float = data.get("red", -1)
        backgroundGreen: float = data.get("green", -1)
        backgroundBlue: float = data.get("blue", -1)
        borderWidth: float = data.get("border_width", -1)
        borderRed: float = data.get("border_red", -1)
        borderGreen: float = data.get("border_green", -1)
        borderBlue: float = data.get("border_blue", -1)

        squareData: ScriptSquareData = ScriptSquareData(
            x=x,
            y=y,
            width=width,
            height=height,
            rotation=rotation,
            backgroundColor=(
                int(backgroundRed),
                int(backgroundGreen),
                int(backgroundBlue),
            ),
            borderWidth=borderWidth,
            borderColor=(int(borderRed), int(borderGreen), int(borderBlue)),
        )
        return squareData

    def calculate_text_display(self, script: str) -> ScriptTextDisplayData:
        data: dict[str, float] = self.get_data(script)

        x: float = data.get("x", -1.0)
        y: float = data.get("y", -1.0)

        background_red: int = int(data.get("red", -1))
        background_green: int = int(data.get("green", -1))
        background_blue: int = int(data.get("blue", -1))

        text_red: int = int(data.get("text_red", -1))
        text_green: int = int(data.get("text_green", -1))
        text_blue: int = int(data.get("text_blue", -1))

        text_value: float = data.get("value", -1.0)
        round_digits: int = int(data.get("round", 1))

        if round_digits > 0:
            final_value: str = str(round(text_value, round_digits))
        else:
            final_value = str(round(text_value))

        return ScriptTextDisplayData(
            x=x,
            y=y,
            backgroundColor=(
                background_red,
                background_green,
                background_blue,
            ),
            textColor=(
                text_red,
                text_green,
                text_blue,
            ),
            value=final_value,
        )
