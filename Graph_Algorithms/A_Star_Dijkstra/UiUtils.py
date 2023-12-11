import pygame
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import plotly.express as px

from Graph_Algorithms.ConstVars import WIDTH, HEIGHT, WHITE, BLACK, ADJUST_VECTOR, NODE_SIZE, BLUE, YELLOW, GREEN, RED, \
    INNER_HEIGHT, \
    INNER_WIDTH, ORANGE


# def ui_runner(start_pt, goal_pt, grid, obstacles, room_coords, path):
#     fig = go.Figure()
#
#     for node in grid:
#         fig.add_trace(go.Scatter(x=[node.x], y=[node.y], mode='markers', marker=dict(size=NODE_SIZE, color='white')))
#
#     for obstacle in obstacles:
#         rect_x = [obstacle[0], obstacle[0] + obstacle[2], obstacle[0] + obstacle[2], obstacle[0], obstacle[0]]
#         rect_y = [obstacle[1], obstacle[1], obstacle[1] + obstacle[3], obstacle[1] + obstacle[3], obstacle[1]]
#         fig.add_trace(go.Scatter(x=rect_x, y=rect_y, mode='lines', line=dict(color='blue'), fill='toself', fillcolor='blue'))
#
#     fig.add_trace(go.Scatter(x=[start_pt[0]], y=[start_pt[1]], mode='markers', marker=dict(size=NODE_SIZE * 8, color='yellow')))
#     fig.add_trace(go.Scatter(x=[goal_pt[0]], y=[goal_pt[1]], mode='markers', marker=dict(size=NODE_SIZE * 8, color='green')))
#
#     if path:
#         path_x = [point[0] for point in path]
#         path_y = [point[1] for point in path]
#         fig.add_trace(go.Scatter(x=path_x, y=path_y, mode='lines', line=dict(color='red', width=NODE_SIZE * 2)))
#
#     if len(room_coords) > 1:
#         room_x = [coord[0] for coord in room_coords + [room_coords[0]]]
#         room_y = [coord[1] for coord in room_coords + [room_coords[0]]]
#         fig.add_trace(go.Scatter(x=room_x, y=room_y, mode='lines', line=dict(color='orange', width=NODE_SIZE)))
#
#     fig.update_layout(
#         autosize=False,
#         width=800,
#         height=800,
#         showlegend=False,
#         xaxis=dict(scaleanchor='y', scaleratio=1),
#         yaxis=dict(scaleanchor='x', scaleratio=1),
#     )
#
#     fig.show()


# def ui_runner(start_pt, goal_pt, grid, obstacles, room_coords, path):
#     fig, ax = plt.subplots()
#     ax.set_aspect('equal', adjustable='box')
#
#
#     for node in grid:
#         circle = plt.Circle((node.x, node.y), NODE_SIZE, color='white', fill=True)
#         ax.add_patch(circle)
#
#     for obstacle in obstacles:
#         rect = patches.Rectangle((obstacle[0], obstacle[1]), obstacle[2], obstacle[3], linewidth=1, edgecolor='blue', facecolor='blue')
#         ax.add_patch(rect)
#
#     ax.add_patch(plt.Circle((start_pt[0], start_pt[1]), NODE_SIZE * 8, color='yellow', fill=True))
#     ax.add_patch(plt.Circle((goal_pt[0], goal_pt[1]), NODE_SIZE * 8, color='green', fill=True))
#
#     if path:
#         path_array = np.array(path)
#         plt.plot(path_array[:, 0], path_array[:, 1], color='red', linewidth=NODE_SIZE * 2)
#
#     if len(room_coords) > 1:
#         room_array = np.array(room_coords + [room_coords[0]])
#         plt.plot(room_array[:, 0], room_array[:, 1], color='orange', linewidth=NODE_SIZE)
#
#     plt.show()

def ui_runner(start_pt, goal_pt, grid, obstacles, room_coords, path, algorithm_choice):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(algorithm_choice)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(BLACK)

        for node in grid:
            pygame.draw.circle(screen, WHITE, (node.x + ADJUST_VECTOR, node.y + ADJUST_VECTOR), NODE_SIZE)

        for obstacle in obstacles:
            pygame.draw.rect(screen, BLUE,
                             (obstacle[0] + ADJUST_VECTOR, obstacle[1] + ADJUST_VECTOR, obstacle[2], obstacle[3]))

        pygame.draw.circle(screen, YELLOW, (start_pt[0] + ADJUST_VECTOR, start_pt[1] + ADJUST_VECTOR), NODE_SIZE * 8)
        pygame.draw.circle(screen, GREEN, (goal_pt[0] + ADJUST_VECTOR, goal_pt[1] + ADJUST_VECTOR), NODE_SIZE * 8)


        if path:
            adjusted_path = [(x + ADJUST_VECTOR, y + ADJUST_VECTOR) for x, y in path]
            for i in range(1, len(adjusted_path)):
                pygame.draw.line(screen, RED, adjusted_path[i - 1], adjusted_path[i], NODE_SIZE * 4)

        if len(room_coords) > 1:
            pygame.draw.lines(screen, ORANGE, True,
                              [(x + ADJUST_VECTOR, y + ADJUST_VECTOR) for x, y in room_coords], NODE_SIZE)

        pygame.display.update()

    pygame.quit()
