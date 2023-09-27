import matplotlib.pyplot as plt


def rewards_plots(file_name, plot_title, ox_name, oy_name):
    episodes = []
    rewards = []

    with open(file_name, "r") as file:
        for line in file:
            if "reward = " in line:
                parts = line.split(", ")
                episode_part = parts[0]
                reward_part = parts[1]
                episode_value = int(episode_part.split(" - ")[1].split("/")[0])
                reward_value = int(reward_part.split(" = ")[1])
                episodes.append(episode_value)
                rewards.append(reward_value)

    plt.figure(figsize=(10, 6))
    plt.plot(episodes, rewards)
    plt.title(plot_title)
    plt.xlabel(ox_name)
    plt.ylabel(oy_name)
    plt.grid(True)
    plt.show()
    # plt.savefig('rewards-episodes.jpg')


if __name__ == "__main__":
    rewards_plots(
        file_name="accumulative_reward_values.txt",
        plot_title="Accumulative Reward Progress",
        ox_name="Episode",
        oy_name="Accumulative Reward"
        )

    rewards_plots(
        file_name="reward_values_per_episode_file.txt",
        plot_title="Reward per Episode",
        ox_name="Episode",
        oy_name="Reward"
    )



