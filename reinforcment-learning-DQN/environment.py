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

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("DQN Path Finding")
        self.clock = pygame.time.Clock()

        self.start_x, self.start_y, self.finish_x, self.finish_y = None, None, None, None
        self.reward, self.frame_iteration = 0, 0
        self.trail_points, self.robot, self.obstacles = None, None, None
        self.flag = None

        self.reset_env()

    def get_state(self):
        return self.robot.x, self.robot.y

    def reset_env(self):
        self.frame_iteration = 0

        self.start_x = 0
        self.start_y = 0
        self.finish_x = 150
        self.finish_y = 150

        self.reward = 0
        self.robot = shapes.FloatRect(self.start_x, self.start_y, 25, 25)

        self.trail_points = []

        self.obstacles = [
            shapes.Obstacle(200, 100, 100, 50),
            shapes.Obstacle(400, 300, 50, 100)
        ]

        self.flag = 0

    def move_robot(self, action):
        dx, dy = 0, 0

        if action == 1:  # move left - L
            dx = -1
        elif action == 2:  # move right - R
            dx = 1
        elif action == 3:  # move up - U
            dy = -1
        elif action == 4:  # move down - D
            dy = 1
        elif action == 5:  # move up and left - UL
            dx, dy = -1, -1
        elif action == 6:  # move up and right - UR
            dx, dy = 1, -1
        elif action == 7:  # move down and left - DL
            dx, dy = -1, 1
        elif action == 8:  # move down and right - DR
            dx, dy = 1, 1

        speed = 1
        self.robot.x = max(0, min(self.SCREEN_WIDTH - self.robot.width, self.robot.x + dx * speed))
        self.robot.y = max(0, min(self.SCREEN_HEIGHT - self.robot.height, self.robot.y + dy * speed))
        self.trail_points.append((self.robot.x + self.robot.width / 2, self.robot.y + self.robot.height / 2))

    def ui_runner(self):
        # runner = True
        # while runner:
        print("Flag6")
        self.clock.tick(self.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.screen.fill(self.BLACK)

        pygame.draw.rect(self.screen, self.RED,
                         pygame.Rect(self.robot.x, self.robot.y, self.robot.width, self.robot.height))

        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, obstacle.BLUE, obstacle.rect)

        if len(self.trail_points) > 1:
            pygame.draw.lines(self.screen, self.WHITE, False, self.trail_points, 1)
        print("Flag7")
        pygame.display.update()

    def do_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.move_robot(action)

        print("Flag4")

        game_over = False
        distance_to_finish = math.sqrt((self.finish_x - self.robot.x) ** 2 + (self.finish_y - self.robot.y) ** 2)

        # reward for becoming closer to aim
        self.reward = 100 / distance_to_finish

        # end if finish
        if distance_to_finish < 2:
            self.reward = 100
            game_over = True
            return self.reward, game_over

        # collision penalty
        for obstacle in self.obstacles:
            if geometry.check_collision(self.robot, obstacle.rect):
                self.reward = -75
                game_over = True
                self.reset_env()
                return self.reward, game_over

        # too long time penalty
        if len(self.trail_points) > 1000:
            self.reward = -100
            game_over = True
            return self.reward, game_over

        print("Flag5")

        self.ui_runner()
        return self.reward, game_over
