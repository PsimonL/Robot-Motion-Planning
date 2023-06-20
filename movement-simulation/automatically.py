import pygame
import random

pygame.init()

WIDTH = 500
HEIGHT = 500
FPS = 60

WHITE = (255, 255, 255)
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
        self.path = [(self.rect.x, self.rect.y), (250, 250), (250, 400)]
        self.current_point = 0

    def update(self):
        target_x, target_y = self.path[self.current_point]
        # print(self.rect.x)
        # print(self.rect.y)
        # print(target_x)
        # print(target_y)
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        print(dx)
        print(dy)

        if dx != 0:
            self.diff_x = dx / abs(dx) * 5
        else:
            self.diff_x = 0

        if dy != 0:
            self.diff_y = dy / abs(dy) * 5
        else:
            self.diff_y = 0

        self.rect.x += self.diff_x
        self.rect.y += self.diff_y

        if abs(dx) < 5 and abs(dy) < 5:
            self.current_point += 1
            if self.current_point >= len(self.path):
                self.current_point = 0
                self.path = self.path[::-1]

        if self.diff_x != 0 or self.diff_y != 0:
            circle = Circle(self.rect.x, self.rect.y)
            self.circles.add(circle)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


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

        if pygame.sprite.spritecollide(robot, obstacles, False):
            robot.rect.x -= robot.diff_x
            robot.rect.y -= robot.diff_y

        screen.fill(BLACK)
        all_sprites.draw(screen)
        robot.circles.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
