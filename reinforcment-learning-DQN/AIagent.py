import tensorflow
import environment


class DQNagent:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def build_model(self):
        pass

    def update_model(self):
        pass

    def train_model(self):
        pass

    def action(self):
        pass


if __name__ == "__main__":
    state_size = 2  # pozycja robota, x i y, czyli stany
    action_size = 8  # możliwe akcje, czyli ruchy

    agent = DQNagent(state_size, action_size)
    env = environment.RobotSimulation()
