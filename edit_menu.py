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
        self.textBoxes: list[TextBox] = []
        self.gameObject: GameObject
        self.fontHeight: int = font.get_rect("").height

    def show(self, gameObject: GameObject, position: tuple[int, int]) -> None:
        self.visible = True
        self.gameObject = gameObject
        self.position = position
        self._generate_textboxes()

    def _generate_textboxes(self) -> None:
        self.textBoxes.clear()
        for i, line in enumerate(self.gameObject.script.splitlines()):
            textBoxRect: pygame.Rect = pygame.Rect(
                self.position[0],
                self.position[1] + i * self.fontHeight,
                500,
                self.fontHeight,
            )
            self.textBoxes.append(
                TextBox(
                    self.screen,
                    self.font,
                    textBoxRect,
                    line,
                    self._apply_change,
                    self.textBoxes,
                    self.settings.textPadding,
                )
            )

    def _apply_change(self) -> None:
        self.gameObject.script = "\n".join(textbox.text for textbox in self.textBoxes)

    def draw(self) -> None:
        if not self.visible:
            return

        for textbox in self.textBoxes:
            textbox.draw()

    def process_event(self, event: pygame.event.Event) -> None:
        if not self.visible:
            return

        for textbox in self.textBoxes:
            textbox.process_events(event)
