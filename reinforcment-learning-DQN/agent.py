import tensorflow
import environment


class DQNAgent:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def generate_path(self):
        pass

    def choose_action(self, state):
        pass

    def update(self, state, action, reward, next_state):
        pass