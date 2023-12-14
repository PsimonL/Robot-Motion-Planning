import pygame
import math
import numpy as np
import shapes
import geometry
from typing import Tuple
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from numba import cuda, jit




class RobotSimulation:
    def __init__(self):
        self.shouldVisualize = True

        self.size, self.inner_size = 650, 600
        self.SCREEN_WIDTH = self.size
        self.SCREEN_HEIGHT = self.size
        self.ADJUST_VECTOR = (self.size - self.inner_size) // 2

        self.FPS = 40

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 255, 0)
        self.ORANGE = (255, 165, 0)
        self.finish_x = 400
        self.finish_y = 400
        self.start_x = 200
        self.start_y = 200
        self.time_penalty_margin = None
        self.correction_xy_start = None
        self.reward, self.step_iterator = 0, -1
        self.trail_points, self.robot, self.obstacles, self.room_coords = None, None, None, None

        self.flag_x, self.flag_y = None, None

        self.room = None
        self.look_forward_flags = [0] * 8

        self.previous_distance_to_finish = 6
        self.current_distance_to_finish = 6

        if self.shouldVisualize:
            pygame.init()
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            pygame.display.set_caption("DQN Path Finding")
            self.clock = pygame.time.Clock()

        self.reset_env()

    def reset_env(self):
        # print("RESET ENV CALL")
        self.step_iterator = 0


        self.reward = 0
        self.time_penalty_margin = 15
        self.correction_xy_start = 20
        self.robot = shapes.FloatRect(self.start_x, self.start_y, 20, 20)

        self.flag_x = 2
        self.flag_y = 2

        self.trail_points = [(self.start_x, self.start_y)]

        self.room_coords = [(0, 0), (600, 0), (600, 600), (0, 600)]
        self.room = Polygon(self.room_coords)

        self.obstacles = [
            # shapes.Obstacle(300, 150, 10, 400),
            # shapes.Obstacle(400, 300, 50, 100)
        ]

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
        # print(f"GET_STATES() self.robot.x, self.robot.y = ({self.robot.x}, {self.robot.y})")
        return np.array([
            self.robot.x, self.robot.y,
            self.current_distance_to_finish,
            self.flag_x, self.flag_y
        ])

    # def get_states(self) -> np.array:
    #     # print(f"GET_STATES() self.robot.x, self.robot.y = ({self.robot.x}, {self.robot.y})")
    #     return np.array([
    #         self.robot.x, self.robot.y,
    #         self.current_distance_to_finish,
    #         self.look_forward_flags[0], self.look_forward_flags[1],
    #         self.look_forward_flags[2], self.look_forward_flags[3],
    #         self.look_forward_flags[4], self.look_forward_flags[5],
    #         self.look_forward_flags[6], self.look_forward_flags[7]
    #     ])

    def will_collision_occur(self, direction):
        # Oblicz nowe położenie robota na podstawie kierunku ruchu
        future_x = self.robot.x
        future_y = self.robot.y

        if direction == 'left':
            future_x -= 5  # Przyjmuję, że robot przesuwa się o 5 jednostek w każdym ruchu
        elif direction == 'right':
            future_x += 5
        elif direction == 'up':
            future_y -= 5
        elif direction == 'down':
            future_y += 5
        elif direction == 'up_left':
            future_x -= 5
            future_y -= 5
        elif direction == 'up_right':
            future_x += 5
            future_y -= 5
        elif direction == 'down_left':
            future_x -= 5
            future_y += 5
        elif direction == 'down_right':
            future_x += 5
            future_y += 5

        # Czy nowe położenie koliduje z przeszkodami
        robot_rect = pygame.Rect(future_x, future_y, self.robot.width, self.robot.height)
        for obstacle in self.obstacles:
            if obstacle.rect.colliderect(robot_rect):
                return True  # Zderzenie występuje

        return False  # Brak zderzenia

    def update_look_forward_flags(self):
        self.look_forward_flags = [0] * 8  # Zerowanie flag przed aktualizacją

        left_LF = self.will_collision_occur('left')
        if left_LF:
            self.look_forward_flags[0] = 1  # Lewo
            self.reward -= 10
        right_LF = self.will_collision_occur('right')
        if right_LF:
            self.look_forward_flags[1] = 1  # Prawo
            self.reward -= 10
        up_LF = self.will_collision_occur('up')
        if up_LF:
            self.look_forward_flags[2] = 1  # Góra
            self.reward -= 10
        down_LF = self.will_collision_occur('down')
        if down_LF:
            self.look_forward_flags[3] = 1  # Dół
            self.reward -= 10
        up_left_LF = self.will_collision_occur('up_left')
        if up_left_LF:
            self.look_forward_flags[4] = 1  # Góra-Lewo
            self.reward -= 10
        up_right_LF = self.will_collision_occur('up_right')
        if up_right_LF:
            self.look_forward_flags[5] = 1  # Góra-Prawo
            self.reward -= 10
        down_left_LF = self.will_collision_occur('down_left')
        if down_left_LF:
            self.look_forward_flags[6] = 1  # Dół-Lewo
            self.reward -= 10
        down_right_LF = self.will_collision_occur('down_right')
        if down_right_LF:
            self.look_forward_flags[7] = 1  # Dół-Prawo
            self.reward -= 10

    def move_robot(self, action):
        dx, dy = 0, 0

        dd = 5

        if action == 0:  # move left - L
            dx = -dd
        elif action == 1:  # move right - R
            dx = dd
        elif action == 2:  # move up - U
            dy = -dd
        elif action == 3:  # move down - D
            dy = dd
        elif action == 4:  # move up and left - UL
            dx, dy = -dd, -dd
        elif action == 5:  # move up and right - UR
            dx, dy = dd, -dd
        elif action == 6:  # move down and left - DL
            dx, dy = -dd, dd
        elif action == 7:  # move down and right - DR
            dx, dy = dd, dd

        speed = dd
        self.robot.x = max(0, min(self.SCREEN_WIDTH - self.robot.width, self.robot.x + dx * speed))
        self.robot.y = max(0, min(self.SCREEN_HEIGHT - self.robot.height, self.robot.y + dy * speed))
        # print(f"MOVE_ROBOT() self.robot.x, self.robot.y = ({self.robot.x}, {self.robot.y})")
        self.trail_points.append((self.robot.x + self.robot.width / 2, self.robot.y + self.robot.height / 2))

    def ui_runner(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.screen.fill(self.BLACK)

        pygame.draw.rect(self.screen, self.YELLOW,
                         pygame.Rect(self.start_x, self.start_y, self.robot.width, self.robot.height))
        pygame.draw.rect(self.screen, self.GREEN,
                         pygame.Rect(self.finish_x, self.finish_y, self.robot.width, self.robot.height))

        pygame.draw.rect(self.screen, self.RED,
                         pygame.Rect(self.robot.x, self.robot.y, self.robot.width, self.robot.height))

        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, obstacle.BLUE, obstacle.rect)

        if len(self.room_coords) > 1:
            pygame.draw.lines(self.screen, self.ORANGE, True,
                              [(x + self.ADJUST_VECTOR, y + self.ADJUST_VECTOR) for x, y in self.room_coords], 1)

        if len(self.trail_points) > 1:
            pygame.draw.lines(self.screen, self.WHITE, False, self.trail_points, 1)
        pygame.display.update()

    def do_step(self, action: int) -> Tuple[int, bool, bool, list]:
        self.step_iterator += 1

        # self.update_look_forward_flags()

        if self.shouldVisualize:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        self.move_robot(action)

        reset_flag = False
        game_finished = False

        # end if finish
        self.current_distance_to_aim()
        if self.current_distance_to_finish <= 5:
            self.reward = 1000
            reset_flag = True
            game_finished = True
            return self.reward, reset_flag, game_finished, self.trail_points

        # penalty/price for direction
        # self.current_direction_to_aim()
        # if self.flag_x == 2 or self.flag_y == 2:
        #     self.reward += 1
        # else:
        #     self.reward += -10

        # if robot getting closer
        print("self.previous_distance_to_finish = ", self.previous_distance_to_finish)
        print("self.current_distance_to_finish = ", self.current_distance_to_finish)
        distance_difference = self.previous_distance_to_finish - self.current_distance_to_finish
        if distance_difference < 0:  # bad
            self.reward -= 10
        elif distance_difference > 0:  # good
            self.reward += distance_difference
        elif distance_difference == 0:  # bad
            self.reward -= 100
        # self.reward += distance_difference
        self.previous_distance_to_finish = self.current_distance_to_finish

        # # obstacle collision penalty
        # for obstacle in self.obstacles:
        #     if geometry.check_collision(self.robot, obstacle.rect):
        #         print("COLLISION!")
        #         self.reward -= 2000
        #         reset_flag = True
        #         return self.reward, reset_flag, game_finished, self.trail_points

        # room wall penalty
        current_coords = Point(self.robot.x, self.robot.y)
        is_inside_room = self.room.contains(current_coords)
        if not is_inside_room:
            self.reward -= 100
            reset_flag = True
            return self.reward, reset_flag, game_finished, self.trail_points

        # too long time penalty
        if self.step_iterator > self.time_penalty_margin:
            self.reward -= 100
            reset_flag = True
            return self.reward, reset_flag, game_finished, self.trail_points

        if self.shouldVisualize:
            self.ui_runner()
            self.clock.tick(self.FPS)
        return self.reward, reset_flag, game_finished, self.trail_points
