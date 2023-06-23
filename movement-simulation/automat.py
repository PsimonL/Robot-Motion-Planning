import pygame


class RobotSimulation:
    def __init__(self):
        pygame.init()

        self.SCREEN_WIDTH = 500
        self.SCREEN_HEIGHT = 500
        self.FPS = 60

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
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

        self.robot = pygame.Rect((self.start_x, self.start_y, 25, 25))

        self.path = [(self.start_x, self.start_y), (200, 10), (200, 250), (100, 250), (100, 300), (300, 300),
                     (300, 450), (10, 450)]
        self.iterator = 0
        self.finished_path = False
        self.trail_points = []
        self.room = [(5, 5, 495, 5), (495, 5, 495, 495), (495, 495, 5, 495), (5, 495, 5, 5)]

    def move_robot(self):
        if self.path:
            if not self.finished_path:
                target_x, target_y = self.path[self.iterator]
                dx = target_x - self.robot.x
                dy = target_y - self.robot.y
                speed = 2

                if dx != 0:
                    self.robot.x += speed if dx > 0 else -speed

                if dy != 0:
                    self.robot.y += speed if dy > 0 else -speed

                if abs(dx) == 0 and abs(dy) == 0:
                    print(self.iterator)
                    self.iterator += 1
                    if self.iterator >= len(self.path):
                        self.iterator = 0
                        # self.finished_path = True
                        print(self.path)
                        self.path = self.path[::-1]
                        print(self.path)

                    # Dodawanie żółtego kółka w punkcie, przez który przechodzi robot
                    self.trail_points.append((target_x, target_y))

                # Dodawanie punktu do śladu
                self.trail_points.append((self.robot.x + self.robot.width / 2, self.robot.y + self.robot.height / 2))

        else:
            raise Exception("Empty 'path'")

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

            pygame.draw.rect(self.screen, self.RED, self.robot)

            for point in self.path:
                pygame.draw.circle(self.screen, self.YELLOW, point, 5)

            if len(self.trail_points) > 1:
                pygame.draw.lines(self.screen, self.WHITE, False, self.trail_points, 1)

            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    simulation = RobotSimulation()
    simulation.main()
