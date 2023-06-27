import pygame
import math


class RobotSimulation:
    def __init__(self):
        pygame.init()

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 800
        self.FPS = 80

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        self.start_x, self.start_y = 10, 10

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Automatic robot simulation")
        self.clock = pygame.time.Clock()

        self.robot = pygame.Rect((self.start_x, self.start_y, 25, 25))

        # self.path = [(self.start_x, self.start_y), (100, 10), (100, 60), (50, 20)]
        self.path = [(self.start_x, self.start_y), (50, 10), (50, 80), (20, 70)]
        self.room = [(5, 5, 495, 5), (495, 5, 495, 495), (495, 495, 5, 495), (5, 495, 5, 5)]
        self.iterator = 0
        self.finished_path = False
        self.trail_points = []

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
                if (dx == 0 and dy != 0) or (dy == 0 and dx != 0) or (dx == dy):  # ruch, pionowo i horyzontalnie
                    print("PIERWSZY PRZYPADEK")
                    if dx != 0:
                        self.robot.x += speed if dx > 0 else -speed
                    if dy != 0:
                        self.robot.y += speed if dy > 0 else -speed
                elif dx != 0 and dy != 0 and dx != dy:  # ruch na ukos
                    print("DRUGI PRZYPADEK")
                    if distance != 0:
                        if (dx < dy) and (dx > 0 and dy > 0):
                            ratio = abs(dy / dx)
                            speed_x = ratio * speed
                            speed_y = speed
                            print(f"RATIO = {ratio}")
                            print(f"speed_x = {speed_x}")
                            print(f"speed_y = {speed_y}")
                        elif (dx > dy) and (dx > 0 and dy > 0):
                            ratio = abs(dx / dy)
                            speed_x = speed
                            speed_y = ratio * speed
                            print(f"RATIO = {ratio}")
                            print(f"speed_x = {speed_x}")
                            print(f"speed_y = {speed_y}")
                        elif (dx < dy) and (dx < 0 and dy < 0):
                            ratio = abs(dx / dy)
                            speed_x = ratio * speed * (-1)
                            speed_y = speed * (-1)
                            print(f"RATIO = {ratio}")
                            print(f"speed_x = {speed_x}")
                            print(f"speed_y = {speed_y}")
                        elif (dx > dy) and (dx < 0 and dy < 0):
                            ratio = abs(dy / dx)
                            speed_x = speed * (-1)
                            speed_y = ratio * speed * (-1)
                            print(f"RATIO = {ratio}")
                            print(f"speed_x = {speed_x}")
                            print(f"speed_y = {speed_y}")

                        self.robot.x += speed_x
                        self.robot.y += speed_y
                else:  # nie ma innej możliwości ruchu
                    raise Exception("Not possible")

                print(f"dx = {dx}")
                print(f"dy = {dy}")
                # print(f"distance = {distance}")
                print(f"self.robot.x = {self.robot.x}")
                print(f"self.robot.y = {self.robot.y}")

                if distance <= tolerance:
                    print(f"Iteration: {self.iterator}")
                    self.iterator += 1
                    if self.iterator >= len(self.path):
                        self.iterator = 0
                        self.finished_path = True
                        # print(f"Path = {self.path}")
                        # self.path = self.path[::-1]
                        # print(f"Reversed path = {self.path}")

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
