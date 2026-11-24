from enum import Enum

import pygame
import pygame.freetype


class TextAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class TextDisplay:
    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.freetype.Font,
        position: tuple[float, float],
        text: str,
        padding: int = 5,
        borderWidth: int = 2,
        borderColor: pygame.Color = pygame.Color(255, 255, 255),
        backgroundColor: pygame.Color = pygame.Color(0, 0, 0),
        textColor: pygame.Color = pygame.Color(255, 255, 255),
        fontSize: float = 22,
        minWidth: int = 1,
        minHeight: int = 1,
        textAlign: TextAlign = TextAlign.RIGHT,
    ) -> None:
        self.screen: pygame.Surface = screen
        self.font: pygame.freetype.Font = font
        self.text: str = text

        self.padding: int = padding
        self.borderWidth: int = borderWidth
        self.borderColor: pygame.Color = borderColor
        self.backgroundColor: pygame.Color = backgroundColor
        self.textColor: pygame.Color = textColor
        self.fontSize: float = fontSize
        self.minWidth: int = minWidth
        self.minHeight: int = minHeight
        self.textAlign: TextAlign = textAlign

        self.rect: pygame.Rect = self._generate_rect(position)

    def _generate_rect(self, position: tuple[float, float]) -> pygame.Rect:
        rect: pygame.Rect = self.font.get_rect(self.text, size=self.fontSize)

        rect.height = max(
            rect.height + self.padding * 2,
            self.minHeight,
        )
        rect.width = max(
            rect.width + self.padding * 2,
            self.minWidth,
        )

        rect.x, rect.y = (int(position[0]), int(position[1]))

        return rect

    def _compute_text_x(self, text_rect: pygame.Rect) -> int:
        inner_left: int = self.rect.x + self.padding + self.borderWidth
        inner_right: int = self.rect.right - self.padding - self.borderWidth
        inner_width: int = inner_right - inner_left

        if self.textAlign == TextAlign.LEFT:
            return inner_left

        if self.textAlign == TextAlign.CENTER:
            return inner_left + (inner_width - text_rect.width) // 2

        return inner_right - text_rect.width

    def draw(self) -> None:  # TODO: vibecoded
        pygame.draw.rect(self.screen, self.backgroundColor, self.rect)

        pygame.draw.rect(
            self.screen,
            self.borderColor,
            self.rect,
            self.borderWidth,
        )

        text_rect: pygame.Rect = self.font.get_rect(
            self.text,
            size=self.fontSize,
        )

        text_rect.x = self._compute_text_x(text_rect)
        text_rect.centery = self.rect.centery

        self.font.render_to(
            self.screen,
            text_rect.topleft,
            self.text,
            self.textColor,
            size=self.fontSize,
        )
