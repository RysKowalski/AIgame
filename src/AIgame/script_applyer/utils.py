class Utils:
    @staticmethod
    def load_number(text: str, pos: int) -> tuple[int, int | float]:
        num: str = ""

        while text[pos].isdigit() or text[pos] == "." or text[pos] == "-":
            num += text[pos]
            pos += 1

        fnum = float(num)
        return pos, int(fnum) if fnum == int(fnum) else fnum

    @staticmethod
    def get_name(expression: str, pos: int) -> tuple[int, str]:
        var = ""
        while expression[pos] not in "+-/*^%,() ":
            var += expression[pos]
            pos += 1
        pos -= 1
        return pos, var
