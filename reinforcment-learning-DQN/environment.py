import pygame
import math
import shapes

class RobotSimulation:
    def __init__(self):
        pygame.init()

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 800
        self.FPS = 80

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 255, 0)

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Automatic robot simulation")
        self.clock = pygame.time.Clock()

        self.robot = shapes.FloatRect(10, 10, 25, 25)

        self.trail_points = []

        self.obstacles = [
            shapes.Obstacle(200, 100, 100, 50),
            shapes.Obstacle(400, 300, 50, 100)
        ]

    def move_robot(self, action):
        dx, dy = 0, 0

        if action == 0:  # move left
            dx = -1
        elif action == 1:  # move right
            dx = 1
        elif action == 2:  # move up
            dy = -1
        elif action == 3:  # move down
            dy = 1
        elif action == 4:  # move up and left
            dx, dy = -1, -1
        elif action == 5:  # move up and right
            dx, dy = 1, -1
        elif action == 6:  # move down and left
            dx, dy = -1, 1
        elif action == 7:  # move down and right
            dx, dy = 1, 1

        speed = 1
        self.robot.x = max(0, min(self.SCREEN_WIDTH - self.robot.width, self.robot.x + dx * speed))
        self.robot.y = max(0, min(self.SCREEN_HEIGHT - self.robot.height, self.robot.y + dy * speed))

        self.trail_points.append((self.robot.x + self.robot.width / 2, self.robot.y + self.robot.height / 2))

    def reset(self):
        pass

    def step(self, action):
        next_state = (self.robot.x, self.robot.y)
        self.move_robot(action)

        reward = -1
        done = False

        if self.robot.x > 500 and self.robot.y > 500:
            reward = 100
            done = True

        return next_state, reward, done, {}

    def main(self):
        runner = True
        while runner:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runner = False


            action = 1



            next_state, reward, done, _ = self.step(action)
            current_state = next_state

            self.screen.fill(self.BLACK)

            pygame.draw.rect(self.screen, self.RED,
                             pygame.Rect(self.robot.x, self.robot.y, self.robot.width, self.robot.height))

            for obstacle in self.obstacles:
                pygame.draw.rect(self.screen, obstacle.BLUE, obstacle.rect)

            if len(self.trail_points) > 1:
                pygame.draw.lines(self.screen, self.WHITE, False, self.trail_points, 1)

            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    simulation = RobotSimulation()
    simulation.main()
