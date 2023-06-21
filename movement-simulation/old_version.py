import pygame
import random

pygame.init()

WIDTH = 500
HEIGHT = 500
FPS = 1000

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Symulacja Robota")
clock = pygame.time.Clock()


class Robot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.diff_x = 0
        self.diff_y = 0
        self.circles = pygame.sprite.Group()
        # self.path = [(self.rect.x, self.rect.y), (10, 250), (10, 400), (250, 400), (350, 400)]
        # self.path = [(self.rect.x, self.rect.y), (250, 250), (250, 400), (450, 400)]
        self.path = [(self.rect.x, self.rect.y), (10, 10), (200, 10), (200, 250), (150, 200)]
        # self.path = [(self.rect.x, self.rect.y), (450, 450), (50, 450), (150, 150)]
        # self.path = [(self.rect.x, self.rect.y), (100, 100), (200, 200), (300, 300), (400, 400)]
        self.iterator = 0

    def update(self):
        target_x, target_y = self.path[self.iterator]
        # print(f"(rect.x, rect.y) = ({self.rect.x}, {self.rect.y})")
        # print(f"(target_x, target_y) = ({target_x}, {target_y})")
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        print(f"(dx, dy) = ({dx-25}, {dy-25})")

        if dx != 0:
            self.diff_x = dx / abs(dx) * 1
        else:
            self.diff_x = 0

        if dy != 0:
            self.diff_y = dy / abs(dy) * 1
        else:
            self.diff_y = 0

        self.rect.x += self.diff_x
        self.rect.y += self.diff_y

        if abs(dx) < 5 and abs(dy) < 5:
            self.iterator += 1
            if self.iterator >= len(self.path):
                self.iterator = 0
                self.path = self.path[::-1]

        if self.diff_x != 0 or self.diff_y != 0:
            circle = Circle(self.rect.x, self.rect.y)

            self.circles.add(circle)

    # def draw(self, screen):
    #     pygame.draw.rect(screen, WHITE, self.rect)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 100))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)


class Circle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x + 25, y + 25)


def main():
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    robot = Robot()
    all_sprites.add(robot)

    for _ in range(0):
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        # if pygame.sprite.spritecollide(robot, obstacles, False):
        #     robot.rect.x -= robot.diff_x
        #     robot.rect.y -= robot.diff_y

        screen.fill(BLACK)
        all_sprites.draw(screen)
        robot.circles.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
