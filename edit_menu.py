from dataclasses import dataclass
from typing import Callable
from enum import Enum

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
    nameBottomGap: int
    topPadding: int
    bottomPadding: int
    textPadding: int
    nameSize: int


class TextAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


@dataclass
class TextDisplaySettings:
    padding: int
    borderWidth: int
    borderColor: pygame.Color
    backgroundColor: pygame.Color
    textColor: pygame.Color
    fontSize: float
    minWidth: int
    minHeight: int
    textAlign: TextAlign = TextAlign.LEFT


class TextDisplay:
    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.freetype.Font,
        position: tuple[float, float],
        text: str,
        settings: TextDisplaySettings,
    ) -> None:
        self.screen: pygame.Surface = screen
        self.font: pygame.freetype.Font = font
        self.text: str = text
        self.settings: TextDisplaySettings = settings
        self.rect: pygame.Rect = self._generate_rect(position)

    def _generate_rect(self, position: tuple[float, float]) -> pygame.Rect:
        rect: pygame.Rect = self.font.get_rect(self.text, size=self.settings.fontSize)

        rect.height = max(
            rect.height + self.settings.padding * 2,
            self.settings.minHeight,
        )
        rect.width = max(
            rect.width + self.settings.padding * 2,
            self.settings.minWidth,
        )

        rect.x, rect.y = (int(position[0]), int(position[1]))

        return rect

    def _compute_text_x(self, text_rect: pygame.Rect) -> int:
        inner_left: int = (
            self.rect.x + self.settings.padding + self.settings.borderWidth
        )
        inner_right: int = (
            self.rect.right - self.settings.padding - self.settings.borderWidth
        )
        inner_width: int = inner_right - inner_left

        if self.settings.textAlign == TextAlign.LEFT:
            return inner_left

        if self.settings.textAlign == TextAlign.CENTER:
            return inner_left + (inner_width - text_rect.width) // 2

        return inner_right - text_rect.width

    def draw(self) -> None:  # TODO: vibecoded
        pygame.draw.rect(self.screen, self.settings.backgroundColor, self.rect)

        pygame.draw.rect(
            self.screen,
            self.settings.borderColor,
            self.rect,
            self.settings.borderWidth,
        )

        text_rect: pygame.Rect = self.font.get_rect(
            self.text,
            size=self.settings.fontSize,
        )

        text_rect.x = self._compute_text_x(text_rect)
        text_rect.centery = self.rect.centery

        self.font.render_to(
            self.screen,
            text_rect.topleft,
            self.text,
            self.settings.textColor,
            size=self.settings.fontSize,
        )


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

    def unfocus(self) -> None:
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
                self.unfocus()

        if not self.active:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.unfocus()

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
        bg_color: tuple[int, int, int] = (10, 10, 10)
        border_color: tuple[int, int, int] = (
            (150, 150, 255) if self.active else (220, 220, 220)
        )
        text_color: tuple[int, int, int] = (255, 255, 255)

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
        self.width: int = 0

    def show(self, gameObject: GameObject, position: tuple[int, int]) -> None:
        self.visible = True
        self.gameObject = gameObject
        self.position = position

        self.maxOptionWidth = (
            self.font.get_rect(get_longest_option(self.gameObject.script) + " = ").width
            + 2 * self.settings.textPadding
        )

        self._generate_options()
        self._calculate_width()
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

            self.options.append(
                (
                    TextDisplay(
                        self.screen,
                        self.font,
                        (self.position[0] - self.maxOptionWidth, posY),
                        get_option_name(line) + " = ",
                        TextDisplaySettings(
                            padding=5,
                            borderWidth=2,
                            borderColor=pygame.Color(255, 255, 255),
                            backgroundColor=pygame.Color(0, 0, 0),
                            textColor=pygame.Color(255, 255, 255),
                            fontSize=22,
                            minWidth=self.maxOptionWidth,
                            minHeight=textBoxRect.height,
                            textAlign=TextAlign.RIGHT,
                        ),
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

    def _calculate_width(self) -> None:
        self.width = (
            self.options[0][0].rect.width
            + self.options[0][1].rect.width
            + 2 * self.settings.menuHorizontalPadding
        )

    def _generate_name(self) -> None:
        self.name = TextDisplay(
            self.screen,
            self.font,
            (
                1,
                self.position[1] - self.settings.nameBottomGap,
            ),
            self.gameObject.name,
            TextDisplaySettings(
                padding=10,
                borderWidth=3,
                borderColor=pygame.Color(255, 255, 255),
                backgroundColor=pygame.Color(0, 0, 0),
                textColor=pygame.Color(255, 255, 255),
                fontSize=35,
                minWidth=int(self.width * 0.75),  # FIXME:
                minHeight=22,
                textAlign=TextAlign.CENTER,
            ),
        )
        self.name.rect.centerx = int(
            self.position[0] + self.options[0][1].rect.width - self.width / 2
        )
        self.name.rect.y = int(
            self.position[1] - self.settings.nameBottomGap - self.name.rect.height
        )

    def generate_whole_menu(self) -> None:
        left: int = self.options[0][0].rect.left - self.settings.menuHorizontalPadding
        top: int = self.name.rect.y - self.settings.menuHorizontalPadding
        width: int = self.width
        height: int = (
            self.settings.bottomPadding
            + (self.options[0][0].rect.height * len(self.options))
            + self.settings.nameBottomGap
            + self.name.rect.height
            + self.settings.topPadding
        )

        self.wholeMenu = pygame.Rect(left, top, width, height)

    def draw(self) -> None:
        if not self.visible:
            return

        self._draw_whole_menu()

        self.name.draw()

        for textbox in self.options:
            textbox[0].draw()
            textbox[1].draw()

    def _draw_whole_menu(self) -> None:
        pygame.draw.rect(self.screen, self.settings.backgroundColor, self.wholeMenu)
        pygame.draw.rect(
            self.screen,
            self.settings.borderColor,
            self.wholeMenu,
            width=self.settings.borderWidth,
        )

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
