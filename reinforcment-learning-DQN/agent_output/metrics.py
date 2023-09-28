import matplotlib.pyplot as plt


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
