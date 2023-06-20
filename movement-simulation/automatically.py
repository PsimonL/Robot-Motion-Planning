import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Symulacja Robota")
clock = pygame.time.Clock()


class Robot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speed = 2
        self.target = None

    def set_target(self, target):
        self.target = target

    def update(self):
        if self.target is not None:
            dx = self.target[0] - self.rect.centerx
            dy = self.target[1] - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance > self.speed:
                direction_x = dx / distance
                direction_y = dy / distance
                self.rect.x += direction_x * self.speed
                self.rect.y += direction_y * self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


all_sprites = pygame.sprite.Group()
robot = Robot()
all_sprites.add(robot)

start_point = (100, 100)
end_point = (700, 500)

robot.set_target(end_point)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, start_point, end_point, 2)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
