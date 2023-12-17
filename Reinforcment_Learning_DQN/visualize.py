import matplotlib.pyplot as plt

import matplotlib.patches as patches
import numpy as np


def visualize_dqn(start_pt, goal_pt, obstacles, room_coords, path, path_id=6376):
    NODE_SIZE = 1
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')

    for obstacle in obstacles:
        rect = patches.Rectangle((obstacle[0], obstacle[1]), obstacle[2], obstacle[3], linewidth=1, edgecolor='blue',
                                 facecolor='blue')
        ax.add_patch(rect)

    ax.add_patch(plt.Circle((start_pt[0], start_pt[1]), NODE_SIZE * 8, color='yellow', fill=True))
    ax.add_patch(plt.Circle((goal_pt[0], goal_pt[1]), NODE_SIZE * 8, color='green', fill=True))

    if path:
        path_array = np.array(path)
        plt.plot(path_array[:, 0], path_array[:, 1], color='red', linewidth=NODE_SIZE * 2)

    if len(room_coords) > 1:
        room_array = np.array(room_coords + [room_coords[0]])
        plt.plot(room_array[:, 0], room_array[:, 1], color='orange', linewidth=NODE_SIZE)

    plt.title(f"Path wit id = {path_id}")
    plt.gca().invert_yaxis()
    plt.show()


# file_path = 'agent_output/successful_paths.txt'
# with open(file_path, 'r') as file:
#     lines = file.readlines()
# paths = []
# for line in lines:
#     parts = line.strip().split(' - ')
#     id = int(parts[0])
#     tuples_str = parts[1].strip('[]')
#
#     # Remove the outer parentheses and split into pairs, then convert to tuples
#     tuples = [tuple(map(float, pair.split(', '))) for pair in tuples_str[1:-1].split('), (')]
#
#     paths.append({'id': id, 'path': tuples})

# for path in paths:
#     print(path['path'])
#     visualize_dqn(
#         start_pt=(200, 200),
#         goal_pt=(400, 200),
#         obstacles=[(300, 175, 10, 400)],
#         room_coords=[(0, 0), (600, 0), (600, 600), (0, 600)],
#         path=path['path'],
#         path_id=path['id']
#     )

visualize_dqn(
    start_pt=(200, 200),
    goal_pt=(400, 200),
    obstacles=[(300, 175, 10, 400)],
    room_coords=[(0, 0), (600, 0), (600, 600), (0, 600)],
    path=[(200, 200), (235.0, 185.0), (260.0, 160.0), (285.0, 160.0), (310.0, 160.0), (335.0, 160.0), (360.0, 160.0), (385.0, 185.0), (410.0, 210.0)]
)