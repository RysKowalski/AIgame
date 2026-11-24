import pygame

from .GameObject import VizObject


class ActionObject(VizObject):
    """
    x
    y
    width
    height
    rotation
    red
    green
    blue
    border_width
    border_red
    border_green
    border_blue
    """

    name = "Action"
    script = """x = 0
y = 0
width = 100
height = 100
rotation = 0
red = 255
green = 255
blue = 255
border_width = 0
border_red = 0
border_green = 0
border_blue = 0"""

    def __init__(
        self,
        screen: pygame.Surface,
    ) -> None:
        super().__init__(screen)

    def draw(self) -> None:
        width = self.data.get("width", 100)
        height = self.data.get("height", 100)
        borderWidth = self.data.get("border_width", 0)

        surface: pygame.Surface = pygame.Surface((width, height), pygame.SRCALPHA)

        rect: pygame.Rect = pygame.Rect(0, 0, width, height)

        pygame.draw.rect(
            surface,
            (
                int(self.data.get("red", 255)),
                int(self.data.get("green", 255)),
                int(self.data.get("blue", 255)),
            ),
            rect,
        )
        if borderWidth > 0:
            pygame.draw.rect(
                surface,
                (
                    int(self.data.get("border_red", 0)),
                    int(self.data.get("border_green", 0)),
                    int(self.data.get("border_blue", 0)),
                ),
                rect,
                int(borderWidth),
            )

        rotatedSurface: pygame.Surface = pygame.transform.rotate(
            surface, self.data.get("rotation", 0)
        )
        center: tuple[float, float] = (
            self.data.get("x", 0) + width / 2,
            self.data.get("y", 0) + height / 2,
        )

        rotatedRect: pygame.Rect = rotatedSurface.get_rect(center=center)

        self.screen.blit(rotatedSurface, rotatedRect)

    def contains_point(self, pos: tuple[int, int]) -> bool:
        width = self.data.get("width", 100)
        height = self.data.get("height", 100)

        surface: pygame.Surface = pygame.Surface((width, height), pygame.SRCALPHA)

        rotatedSurface: pygame.Surface = pygame.transform.rotate(
            surface, self.data.get("rotation", 0)
        )

        center: tuple[float, float] = (
            self.data.get("x", 0) + width / 2,
            self.data.get("y", 0) + height / 2,
        )

        rotatedRect: pygame.Rect = rotatedSurface.get_rect(center=center)

        return rotatedRect.collidepoint(pos)
