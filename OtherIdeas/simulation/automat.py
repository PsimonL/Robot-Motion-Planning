import pygame
import math


class FloatRect:
    def __init__(self, x, y, width, height):
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height


class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.BLUE = (0, 0, 255)



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

        self.start_x, self.start_y = 10, 10

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Automatic robot simulation")
        self.clock = pygame.time.Clock()

        self.robot = FloatRect(self.start_x, self.start_y, 25, 25)

        # self.path = [(self.start_x, self.start_y), (100, 10), (100, 60), (50, 20)]
        self.path = [(self.start_x, self.start_y), (50, 10), (50, 80), (20, 70), (20, 100), (100, 100), (200, 200),
                     (300, 200), (370, 290)]
        # self.path = [(self.start_x, self.start_y), (100, 200)]
        self.room = [(5, 5, 495, 5), (495, 5, 495, 495), (495, 495, 5, 495), (5, 495, 5, 5)]
        self.iterator = 0
        self.finished_path = False
        self.trail_points = []
        self.obstacles = [
            Obstacle(200, 100, 100, 50),
            Obstacle(400, 300, 50, 100)
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

                if (dx == 0 and dy != 0) or (dy == 0 and dx != 0) or (dx == dy):  # ruch, pionowo i horyzontalnie
                    print("PIERWSZY PRZYPADEK")
                    if dx != 0:
                        self.robot.x += speed if dx > 0 else -speed
                    if dy != 0:
                        self.robot.y += speed if dy > 0 else -speed
                elif (dx != 0 and dy != 0) or (dx == 0 and dy == 0):  # ruch na ukos
                    print("DRUGI PRZYPADEK")
                    if distance != 0:
                        if (dx < dy) and (dx > 0 and dy > 0):
                            ratio = abs(dy / dx)
                            speed_x = speed
                            speed_y = ratio * speed
                            print("2.1")
                            print(f"RATIO = {ratio}")
                            print(f"speed_x = {speed_x}")
                            print(f"speed_y = {speed_y}")
                        elif (dx > dy) and (dx > 0 and dy > 0):
                            ratio = abs(dx / dy)
                            speed_x = ratio * speed
                            speed_y = speed
                            print("2.2")
                            print(f"RATIO = {ratio}")
                            print(f"speed_x = {speed_x}")
                            print(f"speed_y = {speed_y}")
                        elif (dx < dy) and (dx < 0 and dy < 0):
                            ratio = abs(dx / dy)
                            speed_x = ratio * speed * (-1)
                            speed_y = speed * (-1)
                            print("2.3")
                            print(f"RATIO = {ratio}")
                            print(f"speed_x = {speed_x}")
                            print(f"speed_y = {speed_y}")
                        elif (dx > dy) and (dx < 0 and dy < 0):
                            ratio = abs(dy / dx)
                            speed_x = speed * (-1)
                            speed_y = ratio * speed * (-1)
                            print("2.4")
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
                        # self.finished_path = True
                        print(f"Path = {self.path}")
                        self.path = self.path[::-1]
                        print(f"Reversed path = {self.path}")

                    self.trail_points.append((target_x, target_y))

                self.trail_points.append((self.robot.x + self.robot.width / 2, self.robot.y + self.robot.height / 2))

    def cross_product(self, X, Y, Z):
        x1, y1 = Z[0] - X[0], Z[1] - X[1]
        x2, y2 = Y[0] - X[0], Y[1] - X[1]
        return x1 * y2 - x2 * y1

    def between(self, X, Y, Z):
        return min(X[0], Y[0]) <= Z[0] <= max(X[0], Y[0]) and min(X[1], Y[1]) <= Z[1] <= max(X[1], Y[1])

    def check_pair(self, pair1, pair2):
        p_x1, p_y1 = pair1
        p_x2, p_y2 = pair2
        print(f"(p_x1, p_y1) = ({p_x1}, {p_y1})")
        print(f"(p_x2, p_y2) = ({p_x2}, {p_y2})")
        print()

        A, B = pair1, pair2

        for i in range(len(self.room) - 1):
            C, D = self.room[i], self.room[i + 1]
            v1 = self.cross_product(C, D, A)
            v2 = self.cross_product(C, D, B)
            v3 = self.cross_product(A, B, C)
            v4 = self.cross_product(A, B, D)

            if (v1 > 0 and v2 < 0 or v1 < 0 and v2 > 0) and (v3 > 0 and v4 < 0 or v3 < 0 and v4 > 0):
                return True

            if v1 == 0 and self.between(C, D, A):
                return True
            if v2 == 0 and self.between(C, D, B):
                return True
            if v3 == 0 and self.between(A, B, C):
                return True
            if v4 == 0 and self.between(A, B, D):
                return True
            return False

    def check_collision(self, rect1, rect2):
        x1, y1, width1, height1 = rect1.x, rect1.y, rect1.width, rect1.height
        x2, y2, width2, height2 = rect2.x, rect2.y, rect2.width, rect2.height

        if x1 < x2 + width2 and x1 + width1 > x2 and y1 < y2 + height2 and y1 + height1 > y2:
            return True
        else:
            return False

    def main(self):

        print("Źródło: http://informatyka.wroc.pl/node/455?page=0,2")
        for i in range(len(self.path) - 1):
            if self.check_pair(self.path[i], self.path[i + 1]):
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
                if self.check_collision(self.robot, obstacle.rect):
                    raise Exception(f"Collision occurred between {self.robot} and {obstacle.rect}")

            pygame.display.update()
        pygame.quit()





if __name__ == '__main__':
    simulation = RobotSimulation()
    simulation.main()