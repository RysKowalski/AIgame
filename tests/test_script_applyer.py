from AIgame.script_applyer.utils import Utils


def test_load_number_int() -> None:
    text: str = "12 "
    expected: int = int(text)

    output = Utils.load_number(text, 0)[1]

    assert isinstance(output, int)
    assert output == expected


def test_load_number_float() -> None:
    text: str = "1.234 "
    expected: float = float(text)

    output = Utils.load_number(text, 0)[1]

    assert isinstance(output, float)
    assert output == expected


def test_load_number_negative() -> None:
    text: str = "-1.234 "
    expected: float = float(text)

    output = Utils.load_number(text, 0)[1]

    assert output == expected


def test_load_number_consumes_pos() -> None:
    text: str = "1234 "
    expected_pos: int = len(text) - 1

    pos = Utils.load_number(text, 0)[0]

    assert pos == expected_pos


def test_get_name_terminates() -> None:
    text: str = "text"
    termination_symbols = "+-/*^%,() "

    outputs = [Utils.get_name(text + symbol, 0)[1] for symbol in termination_symbols]

    for o in outputs:
        assert o == text


def test_get_name_consumes_pos() -> None:
    text: str = "1234 "
    expected_pos: int = len(text) - 1

    pos = Utils.get_name(text, 0)[0]

    assert pos == expected_pos
