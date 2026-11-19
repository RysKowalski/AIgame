from __future__ import annotations

from typing import TYPE_CHECKING


import pygame

from AIgame.widgets.toggle import Toggle


if TYPE_CHECKING:
    from AIgame.script_applyer.context import Context
    from pygame.event import Event

from .GameObject import InputObject


class ToggleObject(InputObject):
    """
    x
    y
    off
    on
    name
    """

    name = "Toggle"
    id = 0
    script = """x = 1
y = 1
off = 0
on = 1
name = 0"""

    def __init__(self, screen: pygame.Surface, context: Context) -> None:
        super().__init__(screen)
        self.data = {}
        self.context: Context = context

        self.toggle: Toggle = Toggle(screen, 0, 0, 100, 40)

    def draw(self) -> None:
        self.toggle._x = int(self.data.get("x", 0))
        self.toggle._y = int(self.data.get("y", 0))
        self.toggle.setWidth(int(self.data.get("width", 100)))

        name: str = str(int(self.data.get("name", 0)))

        if self.toggle.getValue():
            self.context.user_variables[name] = self.data.get("on", 1)
        else:
            self.context.user_variables[name] = self.data.get("off", 0)

        self.toggle.draw()

    def contains_point(self, pos: tuple[int, int]) -> bool:
        return self.toggle.contains(pos[0], pos[1])

    def process_event(self, events: list["Event"]) -> None:
        # self.toggle.listen(events)
        pass
