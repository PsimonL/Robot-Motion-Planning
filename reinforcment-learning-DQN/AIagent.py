import random
import os
import torch
import environment
import tensorflow as tf
import random as rd
import numpy as np
import keras.models
import keras.layers
import keras.optimizers
from collections import deque

from environment import RobotSimulation


class DQNagent:
    def __init__(self):
        self.state_size = 3
        self.action_size = 8  # możliwe akcje, czyli ruchy, 8 możliwych
        self.batch_size = 10
        self.no_episodes = 10_000
        self.max_memory = 100_000
        self.output_dir = "agent_output/"

        self.memory = deque(maxlen=3000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = 0.001

        self.start_point = (100, 100)
        self.end_point = (500, 500)

        self.model = self._build_model()

    def _build_model(self):
        # model = keras.models.Sequential([
        #     keras.layers.Input(shape=(self.state_size,)),
        #     keras.layers.Dense(64, activation='relu'),
        #     keras.layers.Dense(64, activation='relu'),
        #     keras.layers.Dense(self.action_size, activation='linear')
        # ])
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(keras.layers.Dense(24, activation='relu'))
        model.add(keras.layers.Dense(self.action_size, activation='linear'))

        model.compile(
            optimizer=keras.optimizers.Adam(
                learning_rate=self.learning_rate
            ),
            loss='mse'
        )

        return model

    def remember(self, state, action, reward, next_sate, done):  # done for episode
        self.memory.append((state, action, reward, next_sate, done))

    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        action_values = self.model.predict(state)
        return np.argmax(action_values[0])

    def train_model(self):
        if len(self.memory) > self.batch_size:
            print("FLAG if len(self.memory) > self.batch_size:")
            minibatch = random.sample(self.memory, self.batch_size)
        else:
            print("FLAG else:")
            minibatch = self.memory
        print(f"minibatch = {minibatch}")

        for state, action, reward, next_sate, done in minibatch:
            Q_new = reward
            if not done:
                Q_new = (reward + self.gamma * np.amax(self.model.predict(next_sate)[0]))  # Bellman
            target = self.model.predict(state)
            target[0][action] = Q_new
            self.model.fit(state, target, epochs=1, verbose=1)  # verbose=0

        # for i in range(len(minibatch)):
        #     state, action, reward, next_state, done = minibatch[i]
        #     Q_new = reward
        #     if not done:
        #         Q_new = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))  # Bellman
        #     target = self.model.predict(state)
        #     target[0][action] = Q_new
        #     self.model.fit(state, target, epochs=1, verbose=0)
        #     print("TRAIN MODEL CALL 5")

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


def driver():
    # initialize agent and env
    agent = DQNagent()
    env = RobotSimulation()

    if not os.path.exists(agent.output_dir):
        os.makedirs(agent.output_dir)

    epsilon_values_file = open(f"{agent.output_dir}epsilon.txt", "w")

    for episode in range(agent.no_episodes):
        print(f"EPISODE{episode}")

        # get current step
        old_state = env.get_states()

        # choose action
        action = agent.get_action(old_state)

        # perform action
        reward, done = env.do_step(action)

        # get new state after action
        new_state = env.get_states()

        # reshape to fit TensorFlow model input
        new_state = np.reshape(new_state, [1, agent.state_size])
        old_state = np.reshape(old_state, [1, agent.state_size])

        # remember feedback to train deep neural network
        agent.remember(old_state, action, reward, new_state, done)

        epsilon_values_file.write(f"episode - {episode}/{agent.no_episodes}, "
                                  f"epsilon = {agent.epsilon}\n")

        if done:
            # if true reset env
            env.reset_env()
            # check if enough data to perform learning
        if len(agent.memory) > agent.batch_size:
            agent.train_model()

        # save weights if the number of episodes is a multiple of 50
        if episode % 30 == 0:
            agent.save(f"{agent.output_dir}episode_{episode}_weights.hdf5")

    epsilon_values_file.close()


if __name__ == "__main__":
    driver()
