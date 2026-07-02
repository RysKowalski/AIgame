from typing import Any, Callable, Sequence, TypeAlias
import pygame

from .mouse import Mouse, MouseState
from .widget import WidgetBase


Colour: TypeAlias = tuple[int, int, int]
Callback: TypeAlias = Callable[..., None]


class Button(WidgetBase):
    def __init__(
        self,
        win: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        isSubWidget: bool = False,
        *,
        inactiveColour: Colour = (150, 150, 150),
        hoverColour: Colour = (125, 125, 125),
        pressedColour: Colour = (100, 100, 100),
        colour: Colour | None = None,
        shadowDistance: int = 0,
        shadowColour: Colour = (210, 210, 180),
        onClick: Callback | None = None,
        onRelease: Callback | None = None,
        onHover: Callback | None = None,
        onHoverRelease: Callback | None = None,
        onClickParams: Sequence[Any] = (),
        onReleaseParams: Sequence[Any] = (),
        onHoverParams: Sequence[Any] = (),
        onHoverReleaseParams: Sequence[Any] = (),
        textColour: Colour = (0, 0, 0),
        fontSize: int = 20,
        text: str = "",
        font: pygame.font.Font | None = None,
        textHAlign: str = "centre",
        textVAlign: str = "centre",
        margin: int = 20,
        image: pygame.Surface | None = None,
        imageHAlign: str = "centre",
        imageVAlign: str = "centre",
        borderThickness: int = 0,
        inactiveBorderColour: Colour = (0, 0, 0),
        hoverBorderColour: Colour = (80, 80, 80),
        pressedBorderColour: Colour = (100, 100, 100),
        borderColour: Colour | None = None,
        radius: int = 0,
    ) -> None:
        super().__init__(win, x, y, width, height, isSubWidget)

        self.inactiveColour = colour or inactiveColour
        self.hoverColour = hoverColour
        self.pressedColour = pressedColour
        self.colour = self.inactiveColour

        self.shadowDistance = shadowDistance
        self.shadowColour = shadowColour

        self.onClick = onClick or (lambda *args: None)
        self.onRelease = onRelease or (lambda *args: None)
        self.onHover = onHover or (lambda *args: None)
        self.onHoverRelease = onHoverRelease or (lambda *args: None)

        self.onClickParams = onClickParams
        self.onReleaseParams = onReleaseParams
        self.onHoverParams = onHoverParams
        self.onHoverReleaseParams = onHoverReleaseParams

        self.clicked = False

        self.textColour = textColour
        self.fontSize = fontSize
        self.string = text
        self.font = font or pygame.font.SysFont("calibri", fontSize)

        self.text = self.font.render(self.string, True, self.textColour)
        self.textHAlign = textHAlign
        self.textVAlign = textVAlign
        self.margin = margin

        self.textRect = self.text.get_rect()
        self.alignTextRect()

        self.image = image
        self.imageHAlign = imageHAlign
        self.imageVAlign = imageVAlign

        self.imageRect = None
        if image is not None:
            self.imageRect = image.get_rect()
            self.alignImageRect()

        self.borderThickness = borderThickness
        self.inactiveBorderColour = borderColour or inactiveBorderColour
        self.hoverBorderColour = hoverBorderColour
        self.pressedBorderColour = pressedBorderColour
        self.borderColour = self.inactiveBorderColour

        self.radius = radius
        self.mouseWasInside = False

    def alignImageRect(self) -> None:
        if self.imageRect is None:
            return

        self.imageRect.center = (
            self._x + self._width // 2,
            self._y + self._height // 2,
        )

        if self.imageHAlign == "left":
            self.imageRect.left = self._x + self.margin
        elif self.imageHAlign == "right":
            self.imageRect.right = self._x + self._width - self.margin

        if self.imageVAlign == "top":
            self.imageRect.top = self._y + self.margin
        elif self.imageVAlign == "bottom":
            self.imageRect.bottom = self._y + self._height - self.margin

    def alignTextRect(self) -> None:
        self.textRect.center = (
            self._x + self._width // 2,
            self._y + self._height // 2,
        )

        if self.textHAlign == "left":
            self.textRect.left = self._x + self.margin
        elif self.textHAlign == "right":
            self.textRect.right = self._x + self._width - self.margin

        if self.textVAlign == "top":
            self.textRect.top = self._y + self.margin
        elif self.textVAlign == "bottom":
            self.textRect.bottom = self._y + self._height - self.margin

    def listen(self, events: list[pygame.event.Event]) -> None:
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                if mouseState == MouseState.RELEASE and self.clicked:
                    self.clicked = False
                    self.onRelease(*self.onReleaseParams)

                elif mouseState == MouseState.CLICK:
                    self.clicked = True
                    self.onClick(*self.onClickParams)
                    self.colour = self.pressedColour
                    self.borderColour = self.pressedBorderColour

                elif mouseState == MouseState.DRAG and self.clicked:
                    self.colour = self.pressedColour
                    self.borderColour = self.pressedBorderColour

                elif mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    self.colour = self.hoverColour
                    self.borderColour = self.hoverBorderColour
                    self.onHover(*self.onHoverParams)

                self.mouseWasInside = True

            elif self.mouseWasInside:
                self.onHoverRelease(*self.onHoverReleaseParams)
                self.mouseWasInside = False

            else:
                self.clicked = False
                self.colour = self.inactiveColour
                self.borderColour = self.inactiveBorderColour

    def draw(self) -> None:
        if not self._hidden:
            if pygame.version.vernum[0] < 2:
                borderRects: list[tuple[int, int, int, int]] = [
                    (
                        self._x + self.radius,
                        self._y,
                        self._width - self.radius * 2,
                        self._height,
                    ),
                    (
                        self._x,
                        self._y + self.radius,
                        self._width,
                        self._height - self.radius * 2,
                    ),
                ]

                borderCircles: list[tuple[int, int]] = [
                    (self._x + self.radius, self._y + self.radius),
                    (self._x + self.radius, self._y + self._height - self.radius),
                    (self._x + self._width - self.radius, self._y + self.radius),
                    (
                        self._x + self._width - self.radius,
                        self._y + self._height - self.radius,
                    ),
                ]

                backgroundRects: list[tuple[int, int, int, int]] = [
                    (
                        self._x + self.borderThickness + self.radius,
                        self._y + self.borderThickness,
                        self._width - 2 * (self.borderThickness + self.radius),
                        self._height - 2 * self.borderThickness,
                    ),
                    (
                        self._x + self.borderThickness,
                        self._y + self.borderThickness + self.radius,
                        self._width - 2 * self.borderThickness,
                        self._height - 2 * (self.borderThickness + self.radius),
                    ),
                ]

                backgroundCircles: list[tuple[int, int]] = [
                    (
                        self._x + self.radius + self.borderThickness,
                        self._y + self.radius + self.borderThickness,
                    ),
                    (
                        self._x + self.radius + self.borderThickness,
                        self._y + self._height - self.radius - self.borderThickness,
                    ),
                    (
                        self._x + self._width - self.radius - self.borderThickness,
                        self._y + self.radius + self.borderThickness,
                    ),
                    (
                        self._x + self._width - self.radius - self.borderThickness,
                        self._y + self._height - self.radius - self.borderThickness,
                    ),
                ]

                for rect in borderRects:
                    pygame.draw.rect(self.win, self.borderColour, rect)

                for circle in borderCircles:
                    pygame.draw.circle(
                        self.win,
                        self.borderColour,
                        circle,
                        self.radius,
                    )

                for rect in backgroundRects:
                    pygame.draw.rect(self.win, self.colour, rect)

                for circle in backgroundCircles:
                    pygame.draw.circle(
                        self.win,
                        self.colour,
                        circle,
                        self.radius,
                    )

            else:
                pygame.draw.rect(
                    self.win,
                    self.shadowColour,
                    (
                        self._x + self.shadowDistance,
                        self._y + self.shadowDistance,
                        self._width,
                        self._height,
                    ),
                    border_radius=self.radius,
                )

                pygame.draw.rect(
                    self.win,
                    self.borderColour,
                    (self._x, self._y, self._width, self._height),
                    border_radius=self.radius,
                )

                pygame.draw.rect(
                    self.win,
                    self.colour,
                    (
                        self._x + self.borderThickness,
                        self._y + self.borderThickness,
                        self._width - self.borderThickness * 2,
                        self._height - self.borderThickness * 2,
                    ),
                    border_radius=self.radius,
                )

            if self.image is not None:
                self.imageRect = self.image.get_rect()
                self.alignImageRect()
                self.win.blit(self.image, self.imageRect)

            self.text = self.font.render(
                self.string,
                True,
                self.textColour,
            )

            self.textRect = self.text.get_rect()
            self.alignTextRect()
            self.win.blit(self.text, self.textRect)

    def setText(self, text: str) -> None:
        self.string = text
        self.text = self.font.render(
            self.string,
            True,
            self.textColour,
        )
        self.textRect = self.text.get_rect()
        self.alignTextRect()

    def setImage(self, image: pygame.Surface) -> None:
        self.image = image
        self.imageRect = image.get_rect()
        self.alignImageRect()

    def setOnClick(
        self,
        onClick: Callback,
        params: Sequence[Any] = (),
    ) -> None:
        self.onClick = onClick
        self.onClickParams = params

    def setOnRelease(
        self,
        onRelease: Callback,
        params: Sequence[Any] = (),
    ) -> None:
        self.onRelease = onRelease
        self.onReleaseParams = params

    def setOnHover(
        self,
        onHover: Callback,
        params: Sequence[Any] = (),
    ) -> None:
        self.onHover = onHover
        self.onHoverParams = params

    def setInactiveColour(self, colour: Colour) -> None:
        self.inactiveColour = colour

    def setPressedColour(self, colour: Colour) -> None:
        self.pressedColour = colour

    def setHoverColour(self, colour: Colour) -> None:
        self.hoverColour = colour

    def get(self, attr: str) -> Any:
        parent = super().get(attr)
        if parent is not None:
            return parent

        if attr == "colour":
            return self.colour

        return None

    def set(self, attr: str, value: Any) -> None:
        super().set(attr, value)

        if attr == "colour":
            self.inactiveColour = value


class ButtonArray(WidgetBase):
    def __init__(
        self,
        win: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        shape: tuple[int, int],
        *,
        colour: tuple[int, int, int] = (210, 210, 180),
        border: int = 10,
        topBorder: int | None = None,
        bottomBorder: int | None = None,
        leftBorder: int | None = None,
        rightBorder: int | None = None,
        borderRadius: int = 0,
        separationThickness: int | None = None,
        inactiveColours: Sequence[tuple[int, int, int]] | None = None,
        hoverColours: Sequence[tuple[int, int, int]] | None = None,
        pressedColours: Sequence[tuple[int, int, int]] | None = None,
        shadowDistances: Sequence[int] | None = None,
        shadowColours: Sequence[tuple[int, int, int]] | None = None,
        onClicks: Sequence[Callable[..., Any] | None] | None = None,
        onReleases: Sequence[Callable[..., Any] | None] | None = None,
        onHovers: Sequence[Callable[..., Any] | None] | None = None,
        onClickParams: Sequence[Any] | None = None,
        onReleaseParams: Sequence[Any] | None = None,
        onHoverParams: Sequence[Any] | None = None,
        textColours: Sequence[tuple[int, int, int]] | None = None,
        fontSizes: Sequence[int] | None = None,
        texts: Sequence[str] | None = None,
        fonts: Sequence[pygame.font.Font | None] | None = None,
        textHAligns: Sequence[str] | None = None,
        textVAligns: Sequence[str] | None = None,
        margins: Sequence[int] | None = None,
        images: Sequence[pygame.Surface | None] | None = None,
        imageHAligns: Sequence[str] | None = None,
        imageVAligns: Sequence[str] | None = None,
        imageRotations: Sequence[float] | None = None,
        imageFills: Sequence[bool] | None = None,
        imageZooms: Sequence[float] | None = None,
        radii: Sequence[int] | None = None,
    ) -> None:
        """A collection of buttons."""

        super().__init__(win, x, y, width, height)

        self.shape: tuple[int, int] = shape
        self.numButtons: int = shape[0] * shape[1]

        self.colour: tuple[int, int, int] = colour
        self.border: int = border
        self.topBorder: int = border if topBorder is None else topBorder
        self.bottomBorder: int = border if bottomBorder is None else bottomBorder
        self.leftBorder: int = border if leftBorder is None else leftBorder
        self.rightBorder: int = border if rightBorder is None else rightBorder
        self.borderRadius: int = borderRadius
        self.separationThickness: int = (
            border if separationThickness is None else separationThickness
        )

        self.buttonAttributes: dict[str, Sequence[Any] | None] = {
            "inactiveColour": inactiveColours,
            "hoverColour": hoverColours,
            "pressedColour": pressedColours,
            "shadowDistance": shadowDistances,
            "shadowColour": shadowColours,
            "onClick": onClicks,
            "onRelease": onReleases,
            "onHover": onHovers,
            "onClickParams": onClickParams,
            "onReleaseParams": onReleaseParams,
            "onHoverParams": onHoverParams,
            "textColour": textColours,
            "fontSize": fontSizes,
            "text": texts,
            "font": fonts,
            "textHAlign": textHAligns,
            "textVAlign": textVAligns,
            "margin": margins,
            "image": images,
            "imageHAlign": imageHAligns,
            "imageVAlign": imageVAligns,
            "imageRotation": imageRotations,
            "imageFill": imageFills,
            "imageZoom": imageZooms,
            "radius": radii,
        }

        self.buttons: list[Button] = []
        self.createButtons()

    def createButtons(self) -> None:
        across, down = self.shape

        width = (
            self._width
            - self.separationThickness * (across - 1)
            - self.leftBorder
            - self.rightBorder
        ) // across

        height = (
            self._height
            - self.separationThickness * (down - 1)
            - self.topBorder
            - self.bottomBorder
        ) // down

        count = 0

        for i in range(across):
            for j in range(down):
                button_x = (
                    self._x + i * (width + self.separationThickness) + self.leftBorder
                )

                button_y = (
                    self._y + j * (height + self.separationThickness) + self.topBorder
                )

                self.buttons.append(
                    Button(
                        self.win,
                        button_x,
                        button_y,
                        width,
                        height,
                        isSubWidget=True,
                        **{
                            key: values[count]
                            for key, values in self.buttonAttributes.items()
                            if values is not None
                        },
                    )
                )

                count += 1

    def listen(self, events: list[pygame.event.Event]) -> None:
        """Wait for inputs."""

        if not self._hidden and not self._disabled:
            for button in self.buttons:
                button.listen(events)

    def draw(self) -> None:
        """Display to surface."""

        if self._hidden:
            return

        rects: list[tuple[int, int, int, int]] = [
            (
                self._x + self.borderRadius,
                self._y,
                self._width - self.borderRadius * 2,
                self._height,
            ),
            (
                self._x,
                self._y + self.borderRadius,
                self._width,
                self._height - self.borderRadius * 2,
            ),
        ]

        circles: list[tuple[int, int]] = [
            (self._x + self.borderRadius, self._y + self.borderRadius),
            (
                self._x + self.borderRadius,
                self._y + self._height - self.borderRadius,
            ),
            (
                self._x + self._width - self.borderRadius,
                self._y + self.borderRadius,
            ),
            (
                self._x + self._width - self.borderRadius,
                self._y + self._height - self.borderRadius,
            ),
        ]

        for rect in rects:
            pygame.draw.rect(self.win, self.colour, rect)

        for circle in circles:
            pygame.draw.circle(
                self.win,
                self.colour,
                circle,
                self.borderRadius,
            )

        for button in self.buttons:
            button.draw()

    def getButtons(self) -> list[Button]:
        return self.buttons


if __name__ == "__main__":
    import AIgame.widgets

    pygame.init()
    win = pygame.display.set_mode((600, 600))

    button = Button(
        win,
        100,
        100,
        300,
        150,
        text="Hello",
        fontSize=50,
        margin=20,
        inactiveColour=(255, 0, 0),
        pressedColour=(0, 255, 0),
        radius=20,
        onClick=lambda: print("Click"),
        font=pygame.font.SysFont("calibri", 10),
        textVAlign="bottom",
        imageHAlign="centre",
        imageVAlign="centre",
        borderThickness=3,
        onRelease=lambda: print("Release"),
        shadowDistance=5,
        borderColour=(0, 0, 0),
        onHover=lambda: print("Hover"),
        onHoverRelease=lambda: print("Hover Release"),
    )

    buttonArray = ButtonArray(
        win,
        50,
        50,
        500,
        500,
        (2, 2),
        border=100,
        texts=("1", "2", "3", "4"),
        onClicks=(
            lambda: print(1),
            lambda: print(2),
            lambda: print(3),
            lambda: print(4),
        ),
    )

    buttonArray.hide()

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill((255, 255, 255))

        AIgame.widgets.update(events)
        pygame.display.update()
