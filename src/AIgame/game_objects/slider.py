from __future__ import annotations

from typing import TYPE_CHECKING


import pygame

from AIgame.widgets.slider import Slider


if TYPE_CHECKING:
    from AIgame.script_applyer.context import Context
    import pygame.freetype
    from pygame.event import Event

from .GameObject import InputObject


class SliderObject(InputObject):
    """
    x
    y
    left
    right
    width
    name
    """

    name = "Slider"
    id = 0
    script = """x = 1
y = 1
left = 10
right = 20
width = 100
name = 0"""

    def __init__(
        self, screen: pygame.Surface, font: "pygame.freetype.Font", context: Context
    ) -> None:
        super().__init__(screen)
        self.font: "pygame.freetype.Font" = font
        self.data = {}
        self.context: Context = context

        self.slider: Slider = Slider(
            screen,
            0,
            0,
            100,
            40,
            handleColour=(255, 0, 0),
            minValue=0,
            maxValue=100,
            colour=(150, 150, 150),
            handleRadius=10,
        )

    def draw(self) -> None:
        self.slider._x = int(self.data.get("x", 0))
        self.slider._y = int(self.data.get("y", 0))

        left: int = int(self.data.get("left", -1))
        right: int = int(self.data.get("right", 1))

        offset: int = max(0, -left)

        self.slider.min = left + offset
        self.slider.max = right + offset

        self.slider.setWidth(int(self.data.get("width", 100)))

        name: str = str(int(self.data.get("name", 0)))

        value: float = self.slider.getValue() - offset
        self.context.user_variables[name] = value

        self.slider.draw()

    def contains_point(self, pos: tuple[int, int]) -> bool:
        return self.slider.contains(pos[0], pos[1])

    def process_event(self, events: list["Event"]) -> None:
        self.slider.listen(events)
