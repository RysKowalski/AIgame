from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

import pygame
from pygame import gfxdraw
from pygame.event import Event
from pygame.surface import Surface

from .mouse import Mouse, MouseState
from .widget import WidgetBase

Colour = tuple[int, int, int]


class Toggle(WidgetBase):
    def __init__(
        self,
        win: Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        *,
        startOn: bool = False,
        onColour: Colour = (141, 185, 244),
        offColour: Colour = (150, 150, 150),
        handleOnColour: Colour = (26, 115, 232),
        handleOffColour: Colour = (200, 200, 200),
        onClick: Callable[..., None] | None = None,
        onClickParams: tuple[Any, ...] = (),
        handleRadius: int | None = None,
    ) -> None:
        super().__init__(win, x, y, width, height)

        self.value: bool = startOn

        self.onColour: Colour = onColour
        self.offColour: Colour = offColour
        self.handleOnColour: Colour = handleOnColour
        self.handleOffColour: Colour = handleOffColour

        self.onClick: Callable[..., None] = (
            onClick if onClick is not None else lambda *args: None
        )
        self.onClickParams: tuple[Any, ...] = onClickParams

        self.handleRadius: int = (
            handleRadius if handleRadius is not None else int(self._height / 1.3)
        )
        self.radius: int = self._height // 2

        self.colour: Colour = self.onColour if self.value else self.offColour
        self.handleColour: Colour = (
            self.handleOnColour if self.value else self.handleOffColour
        )

    def toggle(self) -> None:
        self.value = not self.value
        self.colour = self.onColour if self.value else self.offColour
        self.handleColour = self.handleOnColour if self.value else self.handleOffColour

    def listen(self, events: Iterable[Event]) -> None:
        del events

        if self._hidden or self._disabled:
            return

        mouse_state: MouseState = Mouse.getMouseState()
        mouse_x: int
        mouse_y: int
        mouse_x, mouse_y = Mouse.getMousePos()

        if self.contains(mouse_x, mouse_y) and mouse_state == MouseState.CLICK:
            self.toggle()
            self.onClick(*self.onClickParams)

    def draw(self) -> None:
        if self._hidden:
            return

        pygame.draw.rect(
            self.win,
            self.colour,
            (self._x, self._y, self._width, self._height),
        )

        pygame.draw.circle(
            self.win,
            self.colour,
            (self._x, self._y + self._height // 2),
            self.radius,
        )

        pygame.draw.circle(
            self.win,
            self.colour,
            (self._x + self._width, self._y + self._height // 2),
            self.radius,
        )

        circle_x: int = self._x + (
            self._width - self.handleRadius + self.radius
            if self.value
            else self.handleRadius - self.radius
        )
        circle_y: int = self._y + self._height // 2

        gfxdraw.filled_circle(
            self.win,
            circle_x,
            circle_y,
            self.handleRadius,
            self.handleColour,
        )
        gfxdraw.aacircle(
            self.win,
            circle_x,
            circle_y,
            self.handleRadius,
            self.handleColour,
        )

    def getValue(self) -> bool:
        return self.value


if __name__ == "__main__":
    import AIgame.widgets

    pygame.init()

    win: Surface = pygame.display.set_mode((1000, 600))

    toggle: Toggle = Toggle(win, 100, 100, 100, 40)
    toggle.onClick = lambda: print(toggle.getValue())

    run: bool = True

    while run:
        events: list[Event] = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                raise SystemExit

        win.fill((255, 255, 255))

        AIgame.widgets.update(events)
        pygame.display.update()
