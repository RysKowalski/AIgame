from dataclasses import dataclass
from typing import Callable

import pygame
import pygame.freetype

from game_objects import GameObject


@dataclass
class EditSettings:
    backgroundColor: pygame.Color
    borderColor: pygame.Color
    editingBorderColor: pygame.Color
    borderWidth: int
    menuHorizontalPadding: int
    topPadding: int
    bottomPadding: int
    textPadding: int
    nameSize: int


class TextDisplay:
    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.freetype.Font,
        rect: pygame.Rect,
        text: str,
        padding: int,
        borderWidth: int,
        borderColor: pygame.Color,
        backgroundColor: pygame.Color,
        textColor: pygame.Color,
    ) -> None:
        self.screen: pygame.Surface = screen
        self.font: pygame.freetype.Font = font
        self.rect: pygame.Rect = rect
        self.text: str = text
        self.padding: int = padding
        self.borderWidth: int = borderWidth
        self.borderColor: pygame.Color = borderColor
        self.backgroundColor: pygame.Color = backgroundColor
        self.textColor: pygame.Color = textColor

        self._create()

    def _create(self) -> None:
        pass

    def draw(self) -> None:
        pygame.draw.rect(self.screen, self.backgroundColor, self.rect)
        pygame.draw.rect(self.screen, self.borderColor, self.rect, self.borderWidth)

        text_pos: tuple[int, int] = (
            self.rect.x + self.padding + self.borderWidth,
            self.rect.centery - self.padding - self.borderWidth,
        )

        self.font.render_to(self.screen, text_pos, self.text, self.textColor)


class TextBox:
    """Simple focusable text input widget for pygame.
    VIBECODED :sob:
    """

    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.freetype.Font,
        rect: pygame.Rect,
        text: str,
        applyFunc: Callable[[], None],
        textBoxes: list["TextBox"],
        padding: int,
    ) -> None:
        self.screen: pygame.Surface = screen
        self.font: pygame.freetype.Font = font
        self.rect: pygame.Rect = rect
        self.text: str = text
        self.applyFunc: Callable[[], None] = applyFunc
        self.textBoxes: list[TextBox] = textBoxes
        self.padding: int = padding

        self.active: bool = False
        self.cursor_pos: int = len(text)
        self.cursor_visible: bool = True
        self.cursor_timer: float = 0.0
        self.cursor_interval: float = 0.5

    def focus(self) -> None:
        """Activate this textbox and deactivate others."""
        for tb in self.textBoxes:
            tb.active = False
        self.active = True
        self.cursor_pos = len(self.text)

    def deactivate(self) -> None:
        """Deactivate the textbox and apply the current value."""
        if self.active:
            self.applyFunc()
        self.active = False

    def process_events(self, event: pygame.event.Event) -> None:
        """Handle pygame events for text input and focus control."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.focus()
            else:
                self.deactivate()

        if not self.active:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.deactivate()

            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.text = (
                        self.text[: self.cursor_pos - 1] + self.text[self.cursor_pos :]
                    )
                    self.cursor_pos -= 1

            elif event.key == pygame.K_DELETE:
                if self.cursor_pos < len(self.text):
                    self.text = (
                        self.text[: self.cursor_pos] + self.text[self.cursor_pos + 1 :]
                    )

            elif event.key == pygame.K_LEFT:
                if self.cursor_pos > 0:
                    self.cursor_pos -= 1

            elif event.key == pygame.K_RIGHT:
                if self.cursor_pos < len(self.text):
                    self.cursor_pos += 1

            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0

            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.text)

            else:
                if event.unicode and event.unicode.isprintable():
                    self.text = (
                        self.text[: self.cursor_pos]
                        + event.unicode
                        + self.text[self.cursor_pos :]
                    )
                    self.cursor_pos += 1

    def draw(self) -> None:
        """Render textbox, text, and cursor."""
        bg_color: tuple[int, int, int] = (40, 40, 40)
        border_color: tuple[int, int, int] = (
            (200, 200, 200) if self.active else (120, 120, 120)
        )
        text_color: tuple[int, int, int] = (240, 240, 240)

        pygame.draw.rect(self.screen, bg_color, self.rect)
        pygame.draw.rect(self.screen, border_color, self.rect, 2)

        text_pos: tuple[int, int] = (
            self.rect.x + self.padding,
            self.rect.y + self.padding,
        )

        self.font.render_to(self.screen, text_pos, self.text, text_color)

        if self.active:
            prefix: str = self.text[: self.cursor_pos]
            cursor_x: int = (
                self.font.get_rect(prefix).width + self.rect.x + self.padding
            )
            cursor_y1: int = self.rect.y + self.padding
            cursor_y2: int = self.rect.y + self.rect.height - self.padding

            pygame.draw.line(
                self.screen,
                (240, 240, 240),
                (cursor_x, cursor_y1),
                (cursor_x, cursor_y2),
                1,
            )


class EditElementMenu:
    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.freetype.Font,
        settings: EditSettings,
    ) -> None:
        self.screen: pygame.Surface = screen
        self.font: pygame.freetype.Font = font
        self.settings: EditSettings = settings

        self.visible: bool = False
        self.position: tuple[int, int] = (0, 0)
        self.options: list[tuple[TextDisplay, TextBox]] = []
        self.gameObject: GameObject
        self.fontHeight: int = font.get_rect("").height
        self.maxOptionWidth: int = 1

        self.wholeMenu: pygame.Rect = pygame.Rect(1, 1, 1, 1)
        self.name: TextDisplay

    def show(self, gameObject: GameObject, position: tuple[int, int]) -> None:
        self.visible = True
        self.gameObject = gameObject
        self.position = position

        self.maxOptionWidth = self.font.get_rect(
            get_longest_option(self.gameObject.script) + " = "
        ).width

        self._generate_options()
        self._generate_name()
        self.generate_whole_menu()

    def _generate_options(self) -> None:
        self.options.clear()
        for i, line in enumerate(self.gameObject.script.splitlines()):
            posY: float = self.position[1] + i * self.fontHeight

            textBoxRect: pygame.Rect = pygame.Rect(
                self.position[0],
                posY,
                500,
                self.fontHeight,
            )

            optionNameRect: pygame.Rect = pygame.Rect(
                self.position[0] - self.maxOptionWidth,
                posY,
                self.maxOptionWidth,
                self.fontHeight,
            )

            self.options.append(
                (
                    TextDisplay(
                        self.screen,
                        self.font,
                        optionNameRect,
                        get_option_name(line) + " = ",
                        5,
                        3,
                        pygame.Color(255, 255, 255),
                        pygame.Color(0, 0, 0),
                        pygame.Color(255, 255, 255),
                    ),
                    TextBox(
                        self.screen,
                        self.font,
                        textBoxRect,
                        get_option_expression(line),
                        self._apply_change,
                        [opt[1] for opt in self.options],
                        self.settings.textPadding,
                    ),
                )
            )

    def _apply_change(self) -> None:
        script: list[str] = []

        for option in self.options:
            script.append("this." + option[0].text + option[1].text)
        self.gameObject.script = "\n".join(script)

    def _generate_name(self) -> None:
        rect: pygame.Rect = self.font.get_rect(
            self.gameObject.name, size=self.settings.nameSize
        )

        self.name = TextDisplay(
            self.screen,
            self.font,
            rect,
            self.gameObject.name,
            4,
            3,
            pygame.Color(255, 255, 255),
            pygame.Color(0, 0, 0),
            pygame.Color(255, 255, 255),
        )

    def generate_whole_menu(self) -> None:
        self.wholeMenu = pygame.Rect(
            10,
            10,
            self.options[0][0].rect.width
            + self.options[0][1].rect.width
            + 2 * self.settings.menuHorizontalPadding,
            self.options[0][0].rect.height * len(self.options)
            + self.settings.bottomPadding
            + self.settings.topPadding
            + self.name.rect.height,
        )

    def draw(self) -> None:
        if not self.visible:
            return

        self.name.draw()

        for textbox in self.options:
            textbox[0].draw()
            textbox[1].draw()

    def process_event(self, event: pygame.event.Event) -> None:
        if not self.visible:
            return

        for textbox in self.options:
            textbox[1].process_events(event)


def get_longest_option(script: str) -> str:
    lines: list[str] = script.splitlines()

    return max([get_option_name(line) for line in lines], key=len)


def get_option_name(line: str) -> str:
    try:
        return line.split()[0].removeprefix("this.")
    except IndexError:
        return "empty"


def get_option_expression(line: str) -> str:
    lineSplit: list[str] = line.split()
    expression: str = " ".join(lineSplit[2:])
    return expression
