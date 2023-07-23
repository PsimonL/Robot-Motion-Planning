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

    def action(self, state):
        print(f"STATE={state}")
        return 8


if __name__ == "__main__":
    state_size = 2  # pozycja robota, x i y, czyli stany
    action_size = 8  # możliwe akcje, czyli ruchy

    agent = DQNagent(state_size, action_size)
    env = environment.RobotSimulation(a_start_x=10, a_start_y=10, a_finish_x=200, a_finish_y=200)

    episodes = 2
    for episode in range(episodes):
        state = (env.robot.x, env.robot.y)
        done = False
        total_reward = 0

        while not done:
            action = agent.action(state)
            next_state, reward, done = env.step(action)
            total_reward += reward
            state = next_state
        print(f"Episode: {episode + 1}, Total Reward: {total_reward}")
        env.reset()

    env.main()
