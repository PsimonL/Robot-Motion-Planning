import pygame
import math


class RobotSimulation:
    def __init__(self):
        pygame.init()

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 800
        self.FPS = 60

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        self.start_x, self.start_y = 10, 10

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Automatic robot simulation")
        self.clock = pygame.time.Clock()

        self.robot = pygame.Rect((self.start_x, self.start_y, 25, 25))

        self.path = [(self.start_x, self.start_y), (100, 10), (100, 60), (50, 20)]
        self.room = [(5, 5, 495, 5), (495, 5, 495, 495), (495, 495, 5, 495), (5, 495, 5, 5)]
        self.iterator = 0
        self.finished_path = False
        self.trail_points = []

    def move_robot(self):
        if self.path:
            if not self.finished_path:
                target_x, target_y = self.path[self.iterator]
                dx = target_x - self.robot.x
                dy = target_y - self.robot.y

                distance = math.sqrt(dx ** 2 + dy ** 2)
                tolerance = 5

                print(f"dx = {dx}")
                print(f"dy = {dy}")
                print(f"distance = {distance}")

                if distance != 0:
                    if dy != 0:
                        ratio = abs(dx / dy)
                    else:
                        ratio = 0 if dx == 0 else float('inf')

                    if abs(dx) > abs(dy):
                        speed_x = 2
                        speed_y = speed_x / ratio
                    else:
                        speed_y = 2
                        speed_x = speed_y * ratio

                    normalized_dx = dx / distance
                    normalized_dy = dy / distance
                    self.robot.x += speed_x * normalized_dx
                    self.robot.y += speed_y * normalized_dy
                    print(f"self.robot.x = {self.robot.x}")
                    print(f"self.robot.y = {self.robot.y}")

                if distance <= tolerance:
                    print(f"Iteration: {self.iterator}")
                    self.iterator += 1
                    if self.iterator >= len(self.path):
                        self.iterator = 0
                        print(f"Path = {self.path}")
                        self.path = self.path[::-1]
                        print(f"Reversed path = {self.path}")

                self.trail_points.append((self.robot.x + self.robot.width / 2, self.robot.y + self.robot.height / 2))

    def main(self):
        runner = True
        while runner:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runner = False
            self.move_robot()
            self.screen.fill(self.BLACK)

            for line in self.room:
                pygame.draw.line(self.screen, self.GREEN, line[:2], line[2:], width=2)

            pygame.draw.rect(self.screen, self.RED, self.robot)

            if len(self.trail_points) > 1:
                pygame.draw.lines(self.screen, self.WHITE, False, self.trail_points, 1)

            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    simulation = RobotSimulation()
    simulation.main()
