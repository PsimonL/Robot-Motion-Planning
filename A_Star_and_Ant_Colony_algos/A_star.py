import pygame
import math

WIDTH = 600
HEIGHT = 600

NODE_SIZE = 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Nodes:
    def __init__(self, x, y, row, col):
        self.x, self.y = x, y
        self.row, self.col = row, col  # multiple of 5, distance on diangonals will be 7 and horizontal as well as vertical would be 5
        # G - distance from current node to start node , H - distance from current node to end node
        self.G, self.H = None, None
        self.F = None  # F (node in nodes) = G (node in nodes) + H (node in nodes)
        self.checked = None


def create_grid():
    margin_x = 10
    margin_y = 10

    num_rows = (WIDTH - margin_x) // 5
    num_cols = (HEIGHT - margin_y) // 5

    print(f"num_rows = {num_rows}")
    print(f"num_cols = {num_cols}")

    grid = []
    for row in range(num_rows):
        for col in range(num_cols):
            x = margin_x + col * 30
            y = margin_y + row * 30
            node = Nodes(x, y, row, col)
            grid.append(node)

    node_id = 0
    for node in grid:
        print(f"Node {node_id} at ({node.x}, {node.y}) - Row: {node.row}, Col: {node.col}")
        node_id += 1

    return grid


def ui_runner():
    grid = create_grid()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        for node in grid:
            pygame.draw.circle(screen, WHITE, (node.x, node.y), NODE_SIZE)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    ui_runner()
