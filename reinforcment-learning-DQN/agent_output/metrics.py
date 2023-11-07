import matplotlib.pyplot as plt
import re


def episode_plots_for_various_metrics(file_name, plot_title, ox_name, oy_name, oy_value):
    episodes = []
    oy_values = []  # rewards, epsilon, loss

    with open(file_name, "r") as file:
        for line in file:
            if f"{oy_value} = " in line:
                parts = line.split(", ")
                episode_part = parts[0]
                oy_values_part = parts[1]
                episode_value = int(episode_part.split(" - ")[1].split("/")[0])
                oy_valuee = float(oy_values_part.split(" = ")[1])
                episodes.append(episode_value)
                oy_values.append(oy_valuee)

    plt.figure(figsize=(10, 6))
    plt.plot(episodes, oy_values)
    plt.title(plot_title)
    plt.xlabel(ox_name)
    plt.ylabel(oy_name)
    plt.grid(True)
    plt.show()
    # plt.savefig('rewards-episodes.jpg')


def number_of_completed_tasks(file_name, plot_title, ox_name, oy_name, no_episodes):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        num_lines = len(lines)
        print(f"Number of completed tasks = {num_lines}")

        completed_episodes = []
        rest_episodes = []

        for line in lines:
            print(line)
            match = re.search(pattern=rf"episode - (\d+)/{no_episodes}", string=line)
            if match:
                completed_episodes.append(int(match.group(1)))

        for i in range(no_episodes + 1):
            if i not in completed_episodes:
                rest_episodes.append(i)

        data = []
        for episode in range(no_episodes + 1):
            if episode in completed_episodes:
                data.append((episode, 1))
            else:
                data.append((episode, 0))

        data.sort(key=lambda x: x[0])
        x, y = zip(*data)
        plt.scatter(x, y, marker='o')
        plt.title(plot_title)
        plt.xlabel(ox_name)
        plt.ylabel(oy_name)
        plt.show()


def steps_per_episode(file_name, plot_title, ox_name, oy_name):
    steps_data = []
    with open(file_name, 'r') as file:
        for line in file:
            if "steps_per_episode" in line:
                steps_value = float(line.split("= ")[1])
                steps_data.append(steps_value)

    episodes = list(range(1, len(steps_data) + 1))

    plt.figure(figsize=(10, 6))
    plt.scatter(episodes, steps_data, color='skyblue')
    plt.title(plot_title)
    plt.xlabel(ox_name)
    plt.ylabel(oy_name)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    episode_plots_for_various_metrics(
        file_name="accumulative_reward_values.txt",
        plot_title="Accumulative Reward Progress",
        ox_name="Episode",
        oy_name="Accumulative Reward",
        oy_value="reward"
    )

    episode_plots_for_various_metrics(
        file_name="reward_values_per_episode_file.txt",
        plot_title="Reward per Episode",
        ox_name="Episode",
        oy_name="Reward",
        oy_value="reward"
    )

    episode_plots_for_various_metrics(
        file_name="epsilon_values.txt",
        plot_title="Epsilon drop",
        ox_name="Episode",
        oy_name="Epsilon",
        oy_value="epsilon"
    )

    steps_per_episode(
        file_name="steps_per_episode_file.txt",
        plot_title="Steps per episode",
        ox_name="Episode",
        oy_name="Steps/time"
    )

    number_of_completed_tasks(
        file_name="no_finished_games_file.txt",
        plot_title="Completed vs uncompleted episodes",
        ox_name="Status of completion",
        oy_name="Episode",
        no_episodes=100
    )
