import pygame
import math
import numpy as np
import shapes
import geometry


class RobotSimulation:
    def __init__(self):
        pygame.init()

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 800
        self.FPS = 40

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 255, 0)

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("DQN Path Finding")
        self.clock = pygame.time.Clock()

        self.start_x, self.start_y, self.finish_x, self.finish_y = None, None, None, None
        self.correction_xy_start = None
        self.reward, self.frame_iteration = 0, 0
        self.trail_points, self.robot, self.obstacles = None, None, None

        self.flag_x, self.flag_y = None, None

        self.previous_distance_to_finish = float('inf')
        self.current_distance_to_finish = float('inf')

        self.reset_env()

    def reset_env(self):
        print("RESET ENV CALL")
        self.frame_iteration = 0

        self.start_x = 500
        self.start_y = 500
        self.finish_x = 750
        self.finish_y = 750

        self.reward = 0
        self.correction_xy_start = 25
        self.robot = shapes.FloatRect(self.start_x, self.start_y, self.correction_xy_start, self.correction_xy_start)

        self.flag_x = 2
        self.flag_y = 2

        self.trail_points = []

        self.obstacles = [
            # shapes.Obstacle(200, 100, 100, 50),
            # shapes.Obstacle(400, 300, 50, 100)
        ]

    def obstacles_placement(self):  # add states that gives info about obstacles
        pass

    def current_distance_to_aim(self):
        return math.dist([self.robot.x, self.robot.y], [self.finish_x, self.finish_y])

    def current_direction_to_aim(self):
        # 0 - go right, 1 - go left, 2 - don't move
        self.flag_x = 0 if self.robot.x < self.finish_x else (1 if self.robot.x > self.finish_x else 2)
        self.flag_y = 0 if self.robot.y < self.finish_y else (1 if self.robot.y > self.finish_y else 2)

    def get_states(self):
        return np.array([self.robot.x, self.robot.y, self.current_distance_to_finish, self.flag_x, self.flag_y])

    def move_robot(self, action):
        dx, dy = 0, 0

        dd = 5

        if action == 1:  # move left - L
            dx = -dd
        elif action == 2:  # move right - R
            dx = dd
        elif action == 3:  # move up - U
            dy = -dd
        elif action == 4:  # move down - D
            dy = dd
        elif action == 5:  # move up and left - UL
            dx, dy = -dd, -dd
        elif action == 6:  # move up and right - UR
            dx, dy = dd, -dd
        elif action == 7:  # move down and left - DL
            dx, dy = -dd, dd
        elif action == 8:  # move down and right - DR
            dx, dy = dd, dd

        speed = dd
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

        pygame.draw.circle(self.screen, self.YELLOW, (self.start_x + self.correction_xy_start,
                                                      self.start_y + self.correction_xy_start), 5)
        pygame.draw.circle(self.screen, self.GREEN, (self.finish_x, self.finish_y), 5)

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

        # end if finish
        if self.current_distance_to_finish <= 5:
            self.reward = 100
            reset_flag = True
            return self.reward, reset_flag
        else:
            self.reward = 0

        # penalty/price for direction
        self.current_direction_to_aim()
        if self.flag_x == 2 or self.flag_y == 2:
            self.reward += 30
        else:
            self.reward += -30

        # if robot getting closer
        distance_difference = self.previous_distance_to_finish - self.current_distance_to_finish
        if distance_difference < 0:
            self.reward += -10
        elif distance_difference > 0:
            self.reward += 100
        else:
            self.reward += 0
        self.previous_distance_to_finish = self.current_distance_to_finish

        # collision penalty
        for obstacle in self.obstacles:
            if geometry.check_collision(self.robot, obstacle.rect):
                self.reward += -75
                reset_flag = True
                return self.reward, reset_flag

        # too long time penalty
        if len(self.trail_points) > 1000:
            self.reward += -100
            reset_flag = True
            return self.reward, reset_flag

        self.ui_runner()
        return self.reward, reset_flag
