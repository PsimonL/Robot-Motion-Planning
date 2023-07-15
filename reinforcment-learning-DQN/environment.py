import pygame
import math
import shapes
import geometry




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
        self.FUCHSIA = (255, 0, 255)
        self.GOLD = (255, 215, 0)
        self.ORANGE = (255, 165, 0)
        self.TURQUOISE = (0, 255, 255)
        self.LIGHT_BLUE = (0, 180, 255)

        self.__start_x, self.__start_y = 10, 10

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Automatic robot simulation")
        self.clock = pygame.time.Clock()

        self.robot = shapes.FloatRect(self.__start_x, self.__start_y, 25, 25)

        self.path = [(self.__start_x, self.__start_y), (50, 10), (50, 80), (20, 70), (20, 100), (100, 100), (200, 200),
                     (300, 200), (370, 290)]
        self.room = [(5, 5, 495, 5), (495, 5, 495, 495), (495, 495, 5, 495), (5, 495, 5, 5)]
        self.iterator = 0
        self.finished_path = False
        self.trail_points = []
        self.obstacles = [
            shapes.Obstacle(200, 100, 100, 50),
            shapes.Obstacle(400, 300, 50, 100)
        ]

    def move_robot(self):
        global speed_x, speed_y
        if self.path:
            if not self.finished_path:
                target_x, target_y = self.path[self.iterator]
                dx = target_x - self.robot.x
                dy = target_y - self.robot.y

                distance = math.sqrt(dx ** 2 + dy ** 2)
                tolerance = 1
                speed = 1

                if (dx == 0 and dy != 0) or (dy == 0 and dx != 0) or (dx == dy):
                    if dx != 0:
                        self.robot.x += speed if dx > 0 else -speed
                    if dy != 0:
                        self.robot.y += speed if dy > 0 else -speed
                elif (dx != 0 and dy != 0) or (dx == 0 and dy == 0):
                    if distance != 0:
                        if (dx < dy) and (dx > 0 and dy > 0):
                            ratio = abs(dy / dx)
                            speed_x = speed
                            speed_y = ratio * speed
                        elif (dx > dy) and (dx > 0 and dy > 0):
                            ratio = abs(dx / dy)
                            speed_x = ratio * speed
                            speed_y = speed
                        elif (dx < dy) and (dx < 0 and dy < 0):
                            ratio = abs(dx / dy)
                            speed_x = ratio * speed * (-1)
                            speed_y = speed * (-1)
                        elif (dx > dy) and (dx < 0 and dy < 0):
                            ratio = abs(dy / dx)
                            speed_x = speed * (-1)
                            speed_y = ratio * speed * (-1)

                        self.robot.x += speed_x
                        self.robot.y += speed_y
                else:
                    raise Exception("Not possible")

                if distance <= tolerance:
                    self.iterator += 1
                    if self.iterator >= len(self.path):
                        self.iterator = 0
                        # self.finished_path = True
                        self.path = self.path[::-1]

                    self.trail_points.append((target_x, target_y))

                self.trail_points.append((self.robot.x + self.robot.width / 2, self.robot.y + self.robot.height / 2))

    def reset(self):
        pass

    def step(self, action):
        pass

    def main(self):
        for i in range(len(self.path) - 1):
            if geometry.check_pair(self.path[i], self.path[i + 1]):
                raise Exception(f"NOT good for line: from {self.path[i]} to {self.path[i + 1]}")
            else:
                print(f"All good for line: from {self.path[i]} to {self.path[i + 1]}")

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

            pygame.draw.rect(self.screen, self.RED,
                             pygame.Rect(self.robot.x, self.robot.y, self.robot.width, self.robot.height))

            for obstacle in self.obstacles:
                pygame.draw.rect(self.screen, obstacle.BLUE, obstacle.rect)

            for point in self.path:
                pygame.draw.circle(self.screen, self.YELLOW, point, 5)

            if len(self.trail_points) > 1:
                pygame.draw.lines(self.screen, self.WHITE, False, self.trail_points, 1)

            for obstacle in self.obstacles:
                if geometry.check_collision(self.robot, obstacle.rect):
                    raise Exception(f"Collision occurred between {self.robot} and {obstacle.rect}")

            pygame.display.update()
        pygame.quit()



if __name__ == '__main__':
    simulation = RobotSimulation()
    simulation.main()