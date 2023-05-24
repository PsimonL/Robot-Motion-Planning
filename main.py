import pygame
import math

pygame.init()

width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Symulacja robota")

robot_x = width // 2
robot_y = height // 2
robot_angle = 0
robot_speed = 5

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        robot_angle -= 0.1
    if keys[pygame.K_RIGHT]:
        robot_angle += 0.1
    if keys[pygame.K_UP]:
        robot_x += math.sin(robot_angle) * robot_speed
        robot_y -= math.cos(robot_angle) * robot_speed
    if keys[pygame.K_DOWN]:
        robot_x -= math.sin(robot_angle) * robot_speed
        robot_y += math.cos(robot_angle) * robot_speed


    window.fill((255, 255, 255))


    pygame.draw.circle(window, (0, 0, 255), (int(robot_x), int(robot_y)), 20)
    pygame.draw.line(window, (255, 0, 0), (robot_x, robot_y),
                     (robot_x + math.sin(robot_angle) * 30, robot_y - math.cos(robot_angle) * 30), 3)


    pygame.display.flip()

    clock.tick(60)

pygame.quit()