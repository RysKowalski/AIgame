Expression = str


class UiElement:
    id: str
    children: list["UiElement"]
    x: Expression
    y: Expression
