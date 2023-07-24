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

    def action(self, x):
        a, b, c = env.main(x)
        return a, b, c

if __name__ == "__main__":
    state_size = 2  # pozycja robota, x i y, czyli stany
    action_size = 8  # możliwe akcje, czyli ruchy

    env = environment.RobotSimulation(a_start_x=10, a_start_y=10)
    agent = DQNagent(start_point=(10, 10), end_point=(200, 200))

    end_points = [(100, 100), (100, 10), (10, 100)]
    directions = [8, 2, 4]
    episodes = len(directions)

    print("BEFORE")
    for episode in range(episodes):
        # env.reset()
        # done = False
        env.finish_setter(end_points[episode])
        # while not done:
        print("INSIDE ")
        print(f"directions[episode] = {directions[episode]}")
        next_state, reward, done = agent.action([directions[episode]])

        print(f"end_points = {end_points[episode]}")
        print("a = {}".format(next_state))
        print("b = {}".format(reward))
        print("c = {}".format(done))
        print("=================================================")

        print(f"Episode: {episode + 1}")
    print("AFTER")
