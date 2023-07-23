import environment

class DQNagent:
    def __init__(self, env, start_point, end_point):
        self.env = env
        self.start_point = start_point
        self.end_point = end_point

    def build_model(self):
        pass

    def update_model(self):
        pass

    def train_model(self):
        pass

    def action(self, a):
        self.env.main([a])


if __name__ == "__main__":
    state_size = 2  # pozycja robota, x i y, czyli stany
    action_size = 8  # możliwe akcje, czyli ruchy

    env = environment.RobotSimulation(a_start_x=10, a_start_y=10, a_finish_x=200, a_finish_y=200)
    agent = DQNagent(env, start_point=(10, 10), end_point=(200, 200))

    episodes = 2
    actions = [8, 2]
    for episode in range(episodes):
        env.reset()
        done = False
        while not done:
            agent.action(actions[episode])

        print(f"Episode: {episode + 1}")
