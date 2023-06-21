import pygame

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Automatic robot simulation")
clock = pygame.time.Clock()

robot = pygame.Rect((250, 250, 25, 25))

path = [(10, 10), (200, 10), (200, 250), (100, 250)]
iterator = 0
finished_path = False
trail_points = []

def move_robot(robot):
    global iterator, finished_path
    if path:
        if not finished_path:
            target_x, target_y = path[iterator]
            dx = target_x - robot.x
            dy = target_y - robot.y
            speed = 2

            if dx != 0:
                robot.x += speed if dx > 0 else -speed

            if dy != 0:
                robot.y += speed if dy > 0 else -speed

            if abs(dx) == 0 and abs(dy) == 0:
                iterator += 1
                if iterator >= len(path):
                    iterator = 0
                    finished_path = True

            # dodawanie punktu do śladu
            trail_points.append((robot.x + robot.width / 2, robot.y + robot.height / 2))

    else:
        raise Exception("Empty 'path'")

def main():
    runner = True
    while runner:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runner = False
        move_robot(robot)
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, robot)

        if len(trail_points) > 1:
            pygame.draw.lines(screen, WHITE, False, trail_points, 1)

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
