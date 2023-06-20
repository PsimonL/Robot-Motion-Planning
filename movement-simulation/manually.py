import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
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
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speed_x = 0
        self.speed_y = 0
        self.kolka = pygame.sprite.Group()

    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        if keys[pygame.K_UP]:
            self.speed_y = -5
        if keys[pygame.K_DOWN]:
            self.speed_y = 5
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

        # Generowanie białych kółek
        if self.speed_x != 0 or self.speed_y != 0:
            kolko = Circle(self.rect.x, self.rect.y)
            self.kolka.add(kolko)

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
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x + 25, y + 25)

all_sprites = pygame.sprite.Group()
przeszkody = pygame.sprite.Group()
robot = Robot()
all_sprites.add(robot)

for _ in range(6):
    przeszkoda = Obstacle()
    all_sprites.add(przeszkoda)
    przeszkody.add(przeszkoda)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    if pygame.sprite.spritecollide(robot, przeszkody, False):
        robot.rect.x -= robot.speed_x
        robot.rect.y -= robot.speed_y

    screen.fill(BLACK)
    all_sprites.draw(screen)
    robot.kolka.draw(screen)
    pygame.display.flip()

pygame.quit()
