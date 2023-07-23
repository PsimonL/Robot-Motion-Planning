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

    def action(self, a):
        next_state, reward, done = env.step(a)
        return next_state, reward, done


if __name__ == "__main__":
    state_size = 2  # pozycja robota, x i y, czyli stany
    action_size = 8  # możliwe akcje, czyli ruchy

    agent = DQNagent(state_size, action_size)
    env = environment.RobotSimulation(a_start_x=10, a_start_y=10, a_finish_x=200, a_finish_y=200)

    episodes = 2
    actions = [2, 8]
    for episode in range(episodes):
        done = False
        while not done:
            action = agent.action(actions[episode])

        print(f"Episode: {episode + 1}")
