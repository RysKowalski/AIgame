class Utils:
    @staticmethod
    def load_number(text: str, pos: int) -> tuple[int, int | float]:
        start: int = pos

        if pos < len(text) and text[pos] == "-":
            pos += 1

        has_dot: bool = False

        while pos < len(text):
            char: str = text[pos]

            if char.isdigit():
                pos += 1
            elif char == "." and not has_dot:
                has_dot = True
                pos += 1
            else:
                break

        num: float = float(text[start:pos])
        return pos, int(num) if num == int(num) else num

    @staticmethod
    def get_name(expression: str, pos: int) -> tuple[int, str]:
        start: int = pos

        while pos < len(expression):
            char: str = expression[pos]

            if not (char.isalnum() or char == "_"):
                break

            pos += 1

        return pos, expression[start:pos]
