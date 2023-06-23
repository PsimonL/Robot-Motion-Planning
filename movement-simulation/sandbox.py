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

    def validate_path(self, *point):
        p_x1, p_y1 = point[0]
        p_x2, p_y2 = point[1]

        for line in self.room:
            l_x1, l_y1, l_x2, l_y2 = line




    def main(self):

        if not all(self.validate_path(points) for points in zip(self.path[:-1], self.path[1:])):
            raise Exception("Path leads outside the room")

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
