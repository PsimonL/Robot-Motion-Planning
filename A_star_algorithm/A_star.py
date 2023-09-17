import pygame
import math
import queue

import shapes

class A_star:
    def __int__(self):
        pygame.init()

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 800
        self.FPS = 80

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 255, 0)
        self.FUCHSIA = (255, 0, 255)
        self.GOLD = (255, 215, 0)
        self.ORANGE = (255, 165, 0)
        self.TURQUOISE = (0, 255, 255)
        self.LIGHT_BLUE = (0, 180, 255)

        self.start_x, self.start_y = 10, 10

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("A* Path Finding")
        self.clock = pygame.time.Clock()

        self.robot = shapes.FloatRect(self.start_x, self.start_y, 25, 25)

        self.obstacles = [
            shapes.Obstacle(200, 100, 100, 50),
            shapes.Obstacle(400, 300, 50, 100)
        ]

    def funcA(self):
        pass

    def funcB(self):
        pass


if __name__ == "__main__":
    path = A_star()
