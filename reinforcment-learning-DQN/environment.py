import pygame
import math
import numpy as np
import shapes
import geometry
from typing import Tuple


class RobotSimulation:
    def __init__(self):
        pygame.init()

        self.SCREEN_WIDTH = 700
        self.SCREEN_HEIGHT = 700
        self.FPS = 600

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 255, 0)

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("DQN Path Finding")
        self.clock = pygame.time.Clock()

        self.start_x, self.start_y, self.finish_x, self.finish_y = None, None, None, None
        self.time_penalty_margin = None
        self.correction_xy_start = None
        self.reward, self.frame_iteration = 0, -1
        self.trail_points, self.robot, self.obstacles = None, None, None

        self.flag_x, self.flag_y = None, None

        self.previous_distance_to_finish = 6
        self.current_distance_to_finish = 6

        self.reset_env()

    def reset_env(self):
        print("RESET ENV CALL")
        self.frame_iteration = 0

        self.start_x = 150
        self.start_y = 350
        self.finish_x = 600
        self.finish_y = 350

        self.reward = 0
        self.time_penalty_margin = 100
        self.correction_xy_start = 20
        self.robot = shapes.FloatRect(self.start_x, self.start_y, self.correction_xy_start, self.correction_xy_start)

        self.flag_x = 2
        self.flag_y = 2

        self.trail_points = []

        self.obstacles = [
            # shapes.Obstacle(200, 100, 100, 50),
            # shapes.Obstacle(400, 300, 50, 100)
        ]

    def obstacles_placement(self):  # TODO: add states that gives info about obstacles
        pass

    def current_distance_to_aim(self):
        self.current_distance_to_finish = math.dist([self.robot.x, self.robot.y], [self.finish_x, self.finish_y])

    def current_direction_to_aim(self):
        # 0 - increment, 1 - decrement, 2 - no change
        if self.robot.x < self.finish_x:
            self.flag_x = 0
        if self.robot.y < self.finish_y:
            self.flag_y = 0
        if self.robot.x > self.finish_x:
            self.flag_x = 1
        if self.robot.y > self.finish_y:
            self.flag_y = 1
        if self.robot.x == self.finish_x:
            self.flag_x = 2
        if self.robot.y == self.finish_y:
            self.flag_y = 2

    def get_states(self) -> np.array:
        print(f"GET_STATES() self.robot.x, self.robot.y = ({self.robot.x}, {self.robot.y})")
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
        print(f"MOVE_ROBOT() self.robot.x, self.robot.y = ({self.robot.x}, {self.robot.y})")
        self.trail_points.append((self.robot.x + self.robot.width / 2, self.robot.y + self.robot.height / 2))

    def ui_runner(self):
        self.clock.tick(self.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.screen.fill(self.BLACK)

        pygame.draw.circle(self.screen, self.YELLOW, (self.start_x, self.start_y), 10)
        pygame.draw.circle(self.screen, self.GREEN, (self.finish_x, self.finish_y), 10)

        pygame.draw.rect(self.screen, self.RED,
                         pygame.Rect(self.robot.x, self.robot.y, self.robot.width, self.robot.height))

        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, obstacle.BLUE, obstacle.rect)

        if len(self.trail_points) > 1:
            pygame.draw.lines(self.screen, self.WHITE, False, self.trail_points, 1)
        pygame.display.update()

    def do_step(self, action: int) -> Tuple[int, bool, bool]:
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print(f"frame {self.frame_iteration}")
        self.move_robot(action)

        reset_flag = False
        game_finished = False

        # end if finish
        self.current_distance_to_aim()
        if self.current_distance_to_finish <= 5:
            self.reward = 100
            reset_flag = True
            game_finished = True
            return self.reward, reset_flag, game_finished
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
        print(f"distance_difference = {distance_difference}")
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
                return self.reward, reset_flag, game_finished

        # too long time penalty
        if len(self.trail_points) > self.time_penalty_margin:
            self.reward += -100
            reset_flag = True
            return self.reward, reset_flag, game_finished

        self.ui_runner()
        return self.reward, reset_flag, game_finished
