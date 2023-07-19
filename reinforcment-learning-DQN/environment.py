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
        pygame.display.set_caption("Automatic robot simulation")
        self.clock = pygame.time.Clock()

        self.start_x = 10
        self.start_y = 10
        self.finish_x = 200
        self.finish_y = 200
        self.total_reward = 0
        self.counter = 0
        self.rewards_per_counter = {self.counter: 0}
        self.robot = shapes.FloatRect(self.start_x, self.start_y, 25, 25)

        self.trail_points = []

        self.obstacles = [
            shapes.Obstacle(200, 100, 100, 50),
            shapes.Obstacle(400, 300, 50, 100)
        ]

    def move_robot(self, action):
        dx, dy = 0, 0

        if action == 1:  # move left
            dx = -1
        elif action == 2:  # move right
            dx = 1
        elif action == 3:  # move up
            dy = -1
        elif action == 4:  # move down
            dy = 1
        elif action == 5:  # move up and left
            dx, dy = -1, -1
        elif action == 6:  # move up and right
            dx, dy = 1, -1
        elif action == 7:  # move down and left
            dx, dy = -1, 1
        elif action == 8:  # move down and right
            dx, dy = 1, 1

        speed = 1
        self.robot.x = max(0, min(self.SCREEN_WIDTH - self.robot.width, self.robot.x + dx * speed))
        self.robot.y = max(0, min(self.SCREEN_HEIGHT - self.robot.height, self.robot.y + dy * speed))

        self.trail_points.append((self.robot.x + self.robot.width / 2, self.robot.y + self.robot.height / 2))

    def reset(self):
        self.robot.x = self.start_x
        self.robot.y = self.start_y
        self.trail_points = []
        self.total_reward = 0
        self.total_reward = 0
        self.counter += 1
        self.rewards_per_counter[self.counter] = 0

    def calculate_distance_to_finish(self):
        distance_x = self.finish_x - self.robot.x
        distance_y = self.finish_y - self.robot.y
        return math.sqrt(distance_x ** 2 + distance_y ** 2)

    def step(self, action):
        next_state = (self.robot.x, self.robot.y)
        self.move_robot(action)

        distance_to_finish = self.calculate_distance_to_finish()

        # reward for becoming closer to aim
        reward = 100 / distance_to_finish

        done = False

        # end if finish
        if distance_to_finish < 20:
            reward = 100
            done = True
            self.total_reward += reward
            self.rewards_per_counter[self.counter] += reward
            self.reset()

        # collision penalty
        for obstacle in self.obstacles:
            if geometry.check_collision(self.robot, obstacle.rect):
                reward = -50
                done = True
                self.total_reward += reward
                self.reset()

        # too long time penalty
        if len(self.trail_points) > 1000:
            reward = -100
            done = True
            self.total_reward += reward
            self.reset()

        self.total_reward += reward

        return next_state, reward, done

    def print_rewards_per_counter(self):
        # TO FIX
        print("Rewards per counter:")
        for counter, total_reward in self.rewards_per_counter.items():
            print(f"Counter: {counter}, Total Reward: {total_reward}")

    def main(self):
        runner = True
        while runner:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runner = False

            action = 8

            next_state, reward, done = self.step(action)
            current_state = next_state
            print(f"current_state = {current_state}")
            print(f"reward = {reward}")

            self.screen.fill(self.BLACK)

            pygame.draw.rect(self.screen, self.RED,
                             pygame.Rect(self.robot.x, self.robot.y, self.robot.width, self.robot.height))

            for obstacle in self.obstacles:
                pygame.draw.rect(self.screen, obstacle.BLUE, obstacle.rect)

            if len(self.trail_points) > 1:
                pygame.draw.lines(self.screen, self.WHITE, False, self.trail_points, 1)

            pygame.display.update()
        pygame.quit()
        self.print_rewards_per_counter()         # TO FIX


if __name__ == '__main__':
    simulation = RobotSimulation()
    simulation.main()
