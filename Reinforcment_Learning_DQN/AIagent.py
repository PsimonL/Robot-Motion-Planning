import random
import os
# import torch
import tensorflow as tf
# import random as rd
import numpy as np
import keras.models
import keras.layers
import keras.optimizers
from collections import deque
from numba import cuda, jit

import environment


def configure_tensorflow(use_gpu):
    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    print("Dostępne urządzenia GPU:", physical_devices)
    if use_gpu:
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
            print("GPU dostępne i skonfigurowane.")
        else:
            print("Nie znaleziono urządzenia GPU. Uczenie będzie odbywać się na CPU.")
    else:
        tf.config.set_visible_devices([], 'GPU')
        print("Uczenie będzie odbywać się na CPU.")


class DQNagent:
    def __init__(self):
        self.state_size = 5
        self.action_size = 8  # możliwe akcje, czyli ruchy, 8 możliwych
        self.batch_size = 100
        self.no_episodes = 1000
        self.max_memory = 50_000

        self.output_dir = "agent_output/"

        self.memory = deque(maxlen=self.max_memory)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = 0.001
        self.loss = []
        self.reward_per_episode = 0
        self.accumulative_reward = 0
        self.steps_per_episode = 0
        self.model = self._build_model()

    def _build_model(self):  # Predict future reward using regression for DQN agent.
        model = keras.models.Sequential([
            keras.layers.Input(shape=(self.state_size,)),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(self.action_size, activation='linear')
        ])

        model.compile(
            optimizer=keras.optimizers.Adam(
                learning_rate=self.learning_rate
            ),
            loss='mse'
        )

        return model

    def remember(self, state, action, reward, next_sate, done):  # done for episode
        self.memory.append((state, action, reward, next_sate, done))

    def get_action(self, state):  # Based on epsilon explore randomly or exploit current data.
        if np.random.rand() <= self.epsilon:  # Exploration mode.
            return random.randrange(self.action_size)
        print("=====================================================")
        print(f"STATE = {state}; STATE.SHAPE = {state.shape}")
        action_values = self.model.predict(state.reshape(1, -1))  # Exploit, over epsilon decay, more exploration.
        return np.argmax(action_values[0])

    def train_short_memory(self, old_state, action, reward, new_state, done):
        single_minibatch = [(old_state, action, reward, new_state, done)]
        self.train_model(single_minibatch, done)

    def train_long_memory(self):
        if len(self.memory) > self.batch_size:
            minibatch = random.sample(self.memory, self.batch_size)
        else:
            minibatch = self.memory
        self.train_model(minibatch, True)

    def train_model(self, minibatch, is_episode_done):
        for batchmini in minibatch:
            state, action, reward, next_state, done = batchmini
            Q_new = reward
            if not done:
                Q_new = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))  # Bellman Equation
            target = self.model.predict(state)
            target[0][action] = Q_new
            history = self.model.fit(state, target, epochs=1, verbose=1)  # verbose=0
            self.loss = history.history['loss']

        if is_episode_done is True and self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name, should_load):
        if should_load:
            if name is not None:
                self.model.load_weights(f"{agent.output_dir}weights/{name}")
            else:
                files = os.listdir(f"{self.output_dir}weights/")
                files = [file for file in files if file.startswith("episode_") and file.endswith("weights.hdf5")]
                if files:
                    # latest_file = max(files, key=lambda x: int(x.split("_")[1]))
                    latest_file = files[-1]
                    self.model.load_weights(f"{self.output_dir}weights/{latest_file}")
                else:
                    print("No weight files found.")
        else:
            pass

    def save(self, name):
        self.model.save_weights(name)


def driver():
    # initialize agent and env
    agent = DQNagent()
    agent.load(name=None, should_load=False)
    env = environment.RobotSimulation()

    if not os.path.exists(agent.output_dir):
        os.makedirs(agent.output_dir)

    epsilon_values_file = open(f"{agent.output_dir}epsilon_values.txt", "w")
    loss_values_file = open(f"{agent.output_dir}loss_values.txt", "w")
    accumulative_reward_values_file = open(f"{agent.output_dir}accumulative_reward_values.txt", "w")
    reward_values_per_episode_file = open(f"{agent.output_dir}reward_values_per_episode_file.txt", "w")
    no_finished_games_file = open(f"{agent.output_dir}no_finished_games_file.txt", "w")
    steps_per_episode_file = open(f"{agent.output_dir}steps_per_episode_file.txt", "w")

    for episode in range(agent.no_episodes):
        print(f"EPISODE{episode}")

        agent.accumulative_reward += agent.reward_per_episode
        accumulative_reward_values_file.write(
            f"episode - {episode}/{agent.no_episodes}, "f"accumulative_reward = {agent.accumulative_reward}\n")
        reward_values_per_episode_file.write(
            f"episode - {episode}/{agent.no_episodes}, "f"reward_per_episode = {agent.reward_per_episode}\n")
        agent.reward_per_episode = 0
        agent.steps_per_episode = 0

        # Episode lasts until done returns True flag and penalty is given or if aim is reached
        while True:
            # get current step
            old_state = env.get_states()

            # choose action
            action = agent.get_action(old_state)

            # perform action
            reward, done, episode_finished = env.do_step(action)
            agent.steps_per_episode += 1

            if episode_finished:
                no_finished_games_file.write(f"episode - {episode}/{agent.no_episodes}, STATUS: AIM REACHED\n")

            agent.reward_per_episode += reward

            # get new state after action
            new_state = env.get_states()

            # reshape to fit TensorFlow model input
            new_state = np.reshape(new_state, [1, agent.state_size])
            old_state = np.reshape(old_state, [1, agent.state_size])

            # remember feedback to train deep neural network
            agent.remember(old_state, action, reward, new_state, done)

            # use short memory to train
            agent.train_short_memory(old_state, action, reward, new_state, done)

            if done:
                # use long memory to train
                agent.train_long_memory()
                agent.save(name=f"{agent.output_dir}weights/episode_{episode}_weights.hdf5")
                steps_per_episode_file.write(f"episode - {episode}/{agent.no_episodes}, "f"steps_per_episode = {agent.steps_per_episode}\n")
                loss_values_file.write(f"episode - {episode}/{agent.no_episodes}, loss = {agent.loss[0]}\n")
                epsilon_values_file.write(f"episode - {episode}/{agent.no_episodes}, "f"epsilon = {agent.epsilon}\n")
                # reset env
                env.reset_env()
                # break and take another episode
                break

    no_finished_games_file.close()
    loss_values_file.close()
    epsilon_values_file.close()
    accumulative_reward_values_file.close()
    reward_values_per_episode_file.close()
    steps_per_episode_file.close()


if __name__ == "__main__":
    print("Start")
    configure_tensorflow(use_gpu=False)
    driver()
