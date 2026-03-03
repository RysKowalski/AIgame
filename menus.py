import pygame
from game_objects import GameObject


def add_element_menu(screen: pygame.Surface, elementList: list[GameObject]):
    running: bool = True
    while running:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(12, 12, 12, 12))
