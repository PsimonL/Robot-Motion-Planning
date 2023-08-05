import random

import environment
import tensorflow as tf
import random as rd
import numpy as np
import keras.models
import keras.layers
import keras.optimizers

from collections import deque


class DQNagent:
    def __init__(self, start_point, end_point, state_size, action_size, batch_size, no_episodes, memory):
        self.state_size = state_size  # state to zmienna x i y, PLUS: odległość (cel-pozycja aktualna),pozycja przeszkód <- narazie tyle
        self.action_size = action_size  # możliwe akcje, czyli ruchy, 8 możliwych
        self.batch_size = batch_size
        self.no_episodes = no_episodes

        self.memory = deque(maxlen=6000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = 0.001

        self.start_point = start_point
        self.end_point = end_point

        self.model = self._build_model()  # private???

    def _build_model(self):
        model = keras.models.Sequential([
            keras.layers.Input(shape=(self.state_size,)),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(self.action_size, activation='linear')
            # Warstwa wyjściowa bez aktywacji dla Q-wartości, no probability cause of linear
        ])

        # Skonfiguruj optymalizator i funkcję straty
        model.compile(
            optimizer=keras.optimizers.Adam(lr=self.learning_rate),
            loss='mse'
        )

        return model

    def remember(self, state, action, reward, next_sate, done):  # done for episode
        self.memory.append((state, action, reward, next_sate, done))

    def action(self, state):
        if np.random.rand() <= self.epsilon:  # check numpy in if, if it suits
            return random.randrange(self.action_size)
        action_values = self.model.predict(state)
        return np.argmax(action_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_sate, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_sate)[0]))  # Bellman
            target_f = self.model.predict(state)
            target_f[0][action] = target

            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

    def driver(self):
        agent = DQNagent()
        done = False
        for e in range(agent.no_episodes):
            state = env.reset()
            state = np.reshape(state, [1, state_size])
            for time in range(5000):
                # env.render()
                action = agent.action(state)
                next_state, reward, done, _ = env.step(action)
                reward = reward if not done else -10
                next_state = np.reshape(next_state, [1, state_size])
                agent.remember(state, action, reward, next_state, done)
                state = next_state
                if done:
                    print("episode: {}/{}, score: {}, epsilon: {}".format())
                    break
                if len(agent.memory) > agent.batch_size:
                    agent.replay(agent.batch_size)
                if e % 50 == 0:
                    agent.save(output_dir + "weights_" + "{:04d}".format(epsilon) + ".hdf5")






    # def update_model(self):
    #     pass
    #
    # def train_model(self):
    #     pass
    #
    # def action(self, x):
    #     a, b, c = env.main(x)
    #     return a, b, c


if __name__ == "__main__":
    state_size = 2  # pozycja robota, x i y, czyli stany
    action_size = 8
    env = environment.RobotSimulation(a_start_x=10, a_start_y=10)
    agent = DQNagent(start_point=(10, 10), end_point=(200, 200), state_size=2, action_size=8, batch_size=32,
                     no_episodes=101)

    end_points = [(100, 100), (100, 10), (10, 100)]
    directions = [8, 2, 4]
    episodes = len(directions)

    print("BEFORE")
    for episode in range(episodes):
        env.reset()
        done = False
        env.finish_setter(end_points[episode])
        while not done:
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
