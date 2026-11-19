import math

import pygame
from pygame import gfxdraw

from .mouse import Mouse, MouseState
from .widget import WidgetBase


class Slider(WidgetBase):
    def __init__(
        self,
        win: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        *,
        valueColour: tuple[int, int, int] = (0, 35, 255),
        minValue: float = 0,
        maxValue: float = 99,
        step: float = 1,
        colour: tuple[int, int, int] = (200, 200, 200),
        handleColour: tuple[int, int, int] = (0, 0, 0),
        borderThickness: int = 3,
        borderColour: tuple[int, int, int] = (0, 0, 0),
        initial: float | None = None,
        curved: bool = True,
        vertical: bool = False,
        draggableAnywhere: bool = True,
        handleRadius: int | None = 10,
    ) -> None:
        super().__init__(win, x, y, width, height)

        self.selected: bool = False
        self.valueColour: tuple[int, int, int] = valueColour

        print(minValue, maxValue)
        self.min: float = minValue
        self.max: float = maxValue
        self.step: float = step

        self.colour: tuple[int, int, int] = colour
        self.handleColour: tuple[int, int, int] = handleColour

        self.borderThickness: int = borderThickness
        self.borderColour: tuple[int, int, int] = borderColour

        if self.step <= 0:
            raise ValueError("step must be greater than zero")

        if self.max <= self.min:
            raise ValueError("max must be greater than min")

        if initial is None:
            initial = (self.max + self.min) / 2

        self.value: float = self.round(initial)
        self.value = max(min(self.value, self.max), self.min)

        self.curved: bool = curved
        self.vertical: bool = vertical
        self.draggableAnywhere: bool = draggableAnywhere

        if self.curved:
            if self.vertical:
                self.radius: int = self._width // 2
            else:
                self.radius = self._height // 2

        if handleRadius is None:
            if self.vertical:
                handleRadius = int(self._width / 1.3)
            else:
                handleRadius = int(self._height / 1.3)

        self.handleRadius: int = handleRadius

    def listen(self, events: list[pygame.event.Event]) -> None:
        if not self._hidden and not self._disabled:
            mouseState: MouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                if mouseState == MouseState.CLICK:
                    self.selected = True

            if mouseState == MouseState.RELEASE:
                self.selected = False

            if self.selected:
                if self.vertical:
                    self.value = self.max - self.round(
                        (y - self._y) / self._height * (self.max - self.min)
                    )
                else:
                    self.value = self.round(
                        (x - self._x) / self._width * (self.max - self.min) + self.min
                    )

                self.value = max(min(self.value, self.max), self.min)

    def draw(self) -> None:
        if not self._hidden:
            pygame.draw.rect(
                self.win,
                self.colour,
                (self._x, self._y, self._width, self._height),
            )

            if self.vertical:
                if self.curved:
                    pygame.draw.circle(
                        self.win,
                        self.colour,
                        (self._x + self._width // 2, self._y),
                        self.radius,
                    )
                    pygame.draw.circle(
                        self.win,
                        self.colour,
                        (self._x + self._width // 2, self._y + self._height),
                        self.radius,
                    )

                circle: tuple[int, int] = (
                    self._x + self._width // 2,
                    int(
                        self._y
                        + (self.max - self.value) / (self.max - self.min) * self._height
                    ),
                )

                pygame.draw.circle(
                    self.win,
                    self.valueColour,
                    (self._x + self._width // 2, self._y + self._height),
                    self.radius if self.curved else 0,
                )

                pygame.draw.rect(
                    self.win,
                    self.valueColour,
                    (
                        self._x,
                        self._y
                        + int(
                            self._height
                            * (self.max - self.value)
                            / (self.max - self.min)
                        ),
                        self._width,
                        int(
                            (1 - (self.max - self.value) / (self.max - self.min))
                            * self._height
                        ),
                    ),
                )

            else:
                if self.curved:
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

                circle = (
                    int(
                        self._x
                        + (self.value - self.min) / (self.max - self.min) * self._width
                    ),
                    self._y + self._height // 2,
                )

                pygame.draw.circle(
                    self.win,
                    self.valueColour,
                    (self._x, self._y + self._height // 2),
                    self.radius if self.curved else 0,
                )

                pygame.draw.rect(
                    self.win,
                    self.valueColour,
                    (
                        self._x,
                        self._y,
                        int(
                            (self.value - self.min)
                            / (self.max - self.min)
                            * self._width
                        )
                        - (self.radius if self.curved else 0),
                        self._height,
                    ),
                )

            gfxdraw.filled_circle(
                self.win, *circle, self.handleRadius, self.handleColour
            )
            gfxdraw.aacircle(self.win, *circle, self.handleRadius, self.handleColour)

    def contains(self, x: int, y: int) -> bool:
        if self.vertical:
            handleX: int = self._x + self._width // 2
            handleY: int = int(
                self._y + (self.max - self.value) / (self.max - self.min) * self._height
            )
        else:
            handleX = int(
                self._x + (self.value - self.min) / (self.max - self.min) * self._width
            )
            handleY = self._y + self._height // 2

        if math.sqrt((handleX - x) ** 2 + (handleY - y) ** 2) <= self.handleRadius:
            return True

        if self.draggableAnywhere:
            return pygame.Rect(
                self._x, self._y, self._width, self._height
            ).collidepoint(x, y)

        return False

    def round(self, value: float) -> float:
        return self.step * round(value / self.step)

    def getValue(self) -> float:
        return self.value

    def setValue(self, value: float) -> None:
        self.value = max(min(self.round(value), self.max), self.min)


if __name__ == "__main__":
    from AIgame import widgets
    from .textbox import TextBox

    pygame.init()
    win: pygame.Surface = pygame.display.set_mode((1000, 600))

    slider: Slider = Slider(
        win,
        100,
        100,
        800,
        5,
        minValue=100,
        maxValue=200,
        step=1,
        handleRadius=15,
    )
    output: TextBox = TextBox(win, 475, 200, 100, 50, fontSize=30)

    v_slider: Slider = Slider(
        win,
        900,
        200,
        40,
        300,
        minValue=100,
        maxValue=200,
        step=1,
        vertical=True,
    )
    v_output: TextBox = TextBox(win, 750, 320, 100, 50, fontSize=30)

    output.disable()
    v_output.disable()

    run: bool = True

    while run:
        events: list[pygame.event.Event] = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill((255, 255, 255))

        output.setText(str(slider.getValue()))
        v_output.setText(str(v_slider.getValue()))

        widgets.update(events)
        pygame.display.update()
