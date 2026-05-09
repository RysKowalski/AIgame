from typing import Callable
from dataclasses import dataclass

import pygame
import pygame.freetype


@dataclass
class TextBoxSettings:
    rect: pygame.Rect
    fontSize: float
    padding: int
    backgroundColor: pygame.Color
    borderColor: pygame.Color
    textColor: int


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
