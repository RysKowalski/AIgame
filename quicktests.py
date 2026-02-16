import pygame

pygame.init()

screen: pygame.Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width: int
height: int
width, height = screen.get_size()

rect: pygame.Rect = pygame.Rect(150, 150, 50, 50)

deltax: int = 1
deltay: int = 1

running: bool = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    rect.x += deltax
    rect.y += deltay

    if rect.right >= width:
        deltax = -1
    if rect.left <= 0:
        deltax = 1
    if rect.bottom >= height:
        deltay = -1
    if rect.top <= 0:
        deltay = 1

    screen.fill((255, 255, 255))
    pygame.draw.rect(
        screen,
        (
            0,
            int(255 * (rect.x / screen.get_size()[0])),
            int(255 * (rect.y / screen.get_size()[1])),
        ),
        rect,
    )
    pygame.display.flip()
