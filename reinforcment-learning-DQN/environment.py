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
        self.target_distance = None
        self.trail_points, self.robot, self.obstacles = None, None, None
        self.flag = None

        self.reset_env()

    def distance_to_finish(self):
        return math.dist([self.robot.x, self.robot.y], [self.finish_x, self.finish_y])

    def get_states(self):
        return self.robot.x, self.robot.y, self.distance_to_finish()

    def reset_env(self):
        self.frame_iteration = 0

        self.start_x = 0
        self.start_y = 0
        self.finish_x = 150
        self.finish_y = 150
        self.target_distance = 0

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

        d = 5

        if action == 1:  # move left - L
            dx = -d
        elif action == 2:  # move right - R
            dx = d
        elif action == 3:  # move up - U
            dy = -d
        elif action == 4:  # move down - D
            dy = d
        elif action == 5:  # move up and left - UL
            dx, dy = -d, -d
        elif action == 6:  # move up and right - UR
            dx, dy = d, -d
        elif action == 7:  # move down and left - DL
            dx, dy = -d, d
        elif action == 8:  # move down and right - DR
            dx, dy = d, d

        speed = d
        self.robot.x = max(0, min(self.SCREEN_WIDTH - self.robot.width, self.robot.x + dx * speed))
        self.robot.y = max(0, min(self.SCREEN_HEIGHT - self.robot.height, self.robot.y + dy * speed))
        self.trail_points.append((self.robot.x + self.robot.width / 2, self.robot.y + self.robot.height / 2))

    def ui_runner(self):
        # runner = True
        # while runner:
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
        pygame.display.update()

    def do_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.move_robot(action)

        reset_flag = False

        # reward for becoming closer to aim
        # end if finish
        if self.distance_to_finish() <= 5:
            self.reward = 100
            reset_flag = True
            return self.reward, reset_flag

        self.reward = 100 / self.distance_to_finish()

        # collision penalty
        for obstacle in self.obstacles:
            if geometry.check_collision(self.robot, obstacle.rect):
                self.reward = -75
                reset_flag = True
                return self.reward, reset_flag

        # too long time penalty
        if len(self.trail_points) > 1000:
            self.reward = -100
            reset_flag = True
            return self.reward, reset_flag

        self.ui_runner()
        return self.reward, reset_flag
