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
        next_state, reward, done = self.env.step(a)
        return next_state, reward, done


if __name__ == "__main__":
    state_size = 2  # pozycja robota, x i y, czyli stany
    action_size = 8  # możliwe akcje, czyli ruchy

    env = environment.RobotSimulation(a_start_x=10, a_start_y=10)
    agent = DQNagent(env, start_point=(10, 10), end_point=(200, 200))

    directions = [8, 2, 4]
    end_points = [(100, 100), (100, 10), (10, 100)]
    episodes = len(directions)

    print("BEFORE")
    for episode in range(episodes):
        env.reset()
        done = False
        env.finish_setter(end_points[episode])
        while not done:
            print("INSIDE ")
            next_state, reward, done = agent.action(directions[episode])

        print(f"Episode: {episode + 1}")
    print("AFTER")
