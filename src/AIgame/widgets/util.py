from typing import Literal

import pygame


def draw_text(
    win: pygame.Surface,
    text: str,
    colour: pygame.Color | tuple[int, int, int] | tuple[int, int, int, int],
    rect: pygame.Rect | tuple[int, int, int, int],
    font: pygame.font.Font,
    align: Literal["left", "center", "right"] = "center",
) -> str:
    """Render wrapped text inside a rectangle.

    Returns the portion of the text that could not be rendered because the
    rectangle ran out of vertical space.
    """
    target_rect: pygame.Rect = pygame.Rect(rect)
    y: int = target_rect.top
    line_spacing: int = -2

    font_height: int = font.size("Tg")[1]

    while text:
        i: int = 1

        if y + font_height > target_rect.bottom:
            break

        while i < len(text) and font.size(text[:i])[0] < target_rect.width:
            i += 1

        if i < len(text):
            space_index: int = text.rfind(" ", 0, i)
            if space_index != -1:
                i = space_index + 1

        image: pygame.Surface = font.render(text[:i], True, colour)
        image_rect: pygame.Rect = image.get_rect()

        image_rect.center = target_rect.center

        if align == "left":
            image_rect.left = target_rect.left
        elif align == "right":
            image_rect.right = target_rect.right

        win.blit(image, (image_rect.left, y))

        y += font_height + line_spacing
        text = text[i:]

    return text
