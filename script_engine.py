from dataclasses import dataclass
from levels import GameLevel


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
    """VIBE CODED :sob:"""

    _ARGUMENT_SENTINEL: str = "__ARG_START__"

    def __init__(self, level: GameLevel) -> None:
        self.level: GameLevel = level

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
                stack.append(self._resolve_variable(token))
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

    def _resolve_variable(self, token: str) -> float:
        return self.level.variables[int(token[1:])]

    def _is_operator(self, token: str) -> bool:
        return token in "+-*/%^"

    def _is_function(self, token: str) -> bool:
        return token in ("max", "min")

    def calculate_square(self, script: str) -> ScriptSquareData:
        lines: list[str] = script.splitlines()
        x: float = -1
        y: float = -1
        width: float = -1
        height: float = -1
        rotation: float = -1
        backgroundRed: float = -1
        backgroundGreen: float = -1
        backgroundBlue: float = -1
        borderWidth: float = -1
        borderRed: float = -1
        borderGreen: float = -1
        borderBlue: float = -1

        for _line in lines:
            line: str = _line.strip()
            if line == "":
                continue

            if line.startswith("this."):
                # TODO: possible optimalization by adding start and end
                firstSpaceIndex: int = line.find(" ")
                value: float = self.calculate_expression(
                    line[firstSpaceIndex + 3 :]  # cut out " = "
                )
                match line[5:firstSpaceIndex]:
                    case "x":
                        x = value
                    case "y":
                        y = value
                    case "width":
                        width = value
                    case "height":
                        height = value
                    case "rotation":
                        rotation = value
                    case "red":
                        backgroundRed = value
                    case "green":
                        backgroundGreen = value
                    case "blue":
                        backgroundBlue = value
                    case "border_width":
                        borderWidth = value
                    case "border_red":
                        borderRed = value
                    case "border_green":
                        borderGreen = value
                    case "border_blue":
                        borderBlue = value
                    case _:
                        continue

        squareData: ScriptSquareData = ScriptSquareData(
            x=x,
            y=y,
            width=width,
            height=height,
            rotation=rotation,
            backgroundColor=(backgroundRed, backgroundGreen, backgroundBlue),
            borderWidth=borderWidth,
            borderColor=(borderRed, borderGreen, borderBlue),
        )
        return squareData
