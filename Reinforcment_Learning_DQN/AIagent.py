import random
import os
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque
from datetime import datetime
import time
import subprocess

import environment


def configure_pytorch():  # Tensorflow sets GPU automatically (even without Keras), Pytorch doesn't.
    print("PyTorch version:", torch.__version__)
    print("Is PyTorch CUDA accessible:", torch.cuda.is_available())
    if torch.cuda.is_available():
        try:
            result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True, check=True)
            nvcc_version = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            nvcc_version = f"Error: {e}"
        print(nvcc_version)
        print("GPU dostępne i skonfigurowane.")
    else:
        print("Nie znaleziono urządzenia GPU. Uczenie będzie odbywać się na CPU.")


class QNetwork(nn.Module):  # Predict future reward using regression for DQN agent.
    def __init__(self, state_size, action_size):
        super(QNetwork, self).__init__()
        self.dense1 = nn.Linear(state_size, 64)
        self.relu1 = nn.ReLU()
        self.dense2 = nn.Linear(64, 64)
        self.relu2 = nn.ReLU()
        self.dense3 = nn.Linear(64, action_size)

    def forward(self, x):
        x = self.relu1(self.dense1(x))
        x = self.relu2(self.dense2(x))
        return self.dense3(x)


class DQNagent:
    def __init__(self):
        self.state_size = 13
        self.action_size = 8   # możliwe akcje, czyli ruchy, 8 możliwych
        self.batch_size = 100
        self.no_episodes = 10_000
        self.max_memory = 50_000
        self.trial_points_memory = []
        self.output_dir = "agent_output/"
        self.memory = deque(maxlen=self.max_memory)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.999
        self.epsilon_min = 0.01
        self.learning_rate = 0.001
        self.loss = []
        self.reward_per_episode = 0
        self.accumulative_reward = 0
        self.steps_per_episode = 0
        self.q_network = QNetwork(self.state_size, self.action_size)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.learning_rate)

    def remember(self, state, action, reward, next_state, done):  # done for episode
        self.memory.append((state, action, reward, next_state, done))

    def get_action(self, state):  # Based on epsilon explore randomly or exploit current data.
        if np.random.rand() <= self.epsilon:  # Exploration mode.
            return random.randrange(self.action_size)
        state_tensor = torch.from_numpy(state).float()
        action_values = self.q_network(state_tensor)  # Exploit, over epsilon decay, more exploration.
        return np.argmax(action_values.detach().numpy())

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
        criterion = nn.MSELoss()

        for batchmini in minibatch:
            state, action, reward, next_state, done = batchmini
            state_tensor = torch.from_numpy(state).float()
            next_state_tensor = torch.from_numpy(next_state).float()
            Q_values = self.q_network(state_tensor)
            Q_action = Q_values[0][action]

            Q_target = reward + (1 - done) * self.gamma * torch.max(self.q_network(next_state_tensor))   # Bellman Equation
            loss = criterion(Q_action, Q_target)

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            self.loss = loss.item()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def find_shortest_path(self):
        if not self.trial_points_memory:
            return None
        return min(self.trial_points_memory, key=len)

    def load(self, name, should_load, agent):
        if should_load:
            if name is not None:
                self.q_network.load_state_dict(torch.load(f"{agent.output_dir}weights/{name}"))
            else:
                files = os.listdir(f"{self.output_dir}weights/")
                files = [file for file in files if file.startswith("episode_") and file.endswith(".pt")]
                if files:
                    latest_file = files[-1]
                    self.q_network.load_state_dict(torch.load(f"{agent.output_dir}weights/{latest_file}"))
                else:
                    print("No weight files found.")
        else:
            pass

    def save(self, name):
        torch.save(self.q_network.state_dict(), f"{name}")


def driver():
    # initialize agent and env
    agent = DQNagent()
    agent.load(name=None, should_load=False, agent=agent)
    env = environment.RobotSimulation()

    if not os.path.exists(agent.output_dir):
        os.makedirs(agent.output_dir)

    start_time = datetime.now()
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    with open(f"{agent.output_dir}execution_time.txt", "a") as execution_time_file:
        execution_time_file.write(f"Execution started at: {start_time_str}\n")
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
            print("action = ", action)
            # perform action
            reward, done, episode_finished, trial_points = env.do_step(action)
            agent.trial_points_memory.append(trial_points)

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
                steps_per_episode_file.write(
                    f"episode - {episode}/{agent.no_episodes}, "f"steps_per_episode = {agent.steps_per_episode}\n")
                loss_values_file.write(f"episode - {episode}/{agent.no_episodes}, loss = {agent.loss}\n")
                epsilon_values_file.write(f"episode - {episode}/{agent.no_episodes}, "f"epsilon = {agent.epsilon}\n")
                # reset env
                env.reset_env()
                # break and take another episode
                break

            if agent.no_episodes % 50 == 0:
                agent.save(name=f"{agent.output_dir}weights/episode_{episode}_weights.pt")

    end_time = datetime.now()
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
    elapsed_time = end_time - start_time
    with open(f"{agent.output_dir}execution_time.txt", "a") as execution_time_file:
        execution_time_file.write(f"Execution finished at: {end_time_str}\n")
        execution_time_file.write(f"Total execution time: {elapsed_time}\n")
        execution_time_file.write("================================================\n")

    execution_time_file.close()
    no_finished_games_file.close()
    loss_values_file.close()
    epsilon_values_file.close()
    accumulative_reward_values_file.close()
    reward_values_per_episode_file.close()
    steps_per_episode_file.close()

    shortest_path = agent.find_shortest_path()
    print(f"shortest_path = {shortest_path}")


if __name__ == "__main__":  # lookforward
    start_time = time.time()
    print("Start")
    configure_pytorch()
    driver()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Czas wykonania: {execution_time} sekundy")  # Czas wykonania 100 epizodów: 12.388508558273315 sekundy