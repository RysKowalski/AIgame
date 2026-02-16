import pygame

Expression = str


class UIElement:
    id: str
    children: list["UIElement"]
    x: Expression
    y: Expression
    screen: pygame.Surface

    def draw(self) -> None: ...


class RectElement(UIElement):
    def __init__(
        self,
        x: Expression,
        y: Expression,
        screen: pygame.Surface,
        color: tuple[int, int, int],
    ) -> None:
        self.x = x
        self.y = y
        self.screen = screen
        self.children = []
        self.id = "temporary ID"

        self.color: tuple[int, int, int] = color

    def draw(self) -> None:
        rect: pygame.Rect = pygame.Rect(int(self.x), int(self.y), 40, 40)
        pygame.draw.rect(self.screen, self.color, rect)


pygame.init()
screen = pygame.display.set_mode((800, 600))
rectElement: RectElement = RectElement("200", "200", screen, (255, 0, 0))

running: bool = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    rectElement.draw()
    pygame.display.flip()
