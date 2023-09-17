import pygame


class FloatRect:
    def __init__(self, x, y, width, height):
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height


class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.BLUE = (0, 0, 255)
