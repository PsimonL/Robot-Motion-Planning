import pygame

from Graph_Algorithms.ConstVars import WIDTH, HEIGHT, WHITE, BLACK, ADJUST_VECTOR, NODE_SIZE, BLUE, YELLOW, GREEN, RED, INNER_HEIGHT, \
    INNER_WIDTH, ORANGE

def rrt_ui_runner(start_pt, goal_pt, obstacles, room_coords, path, rrt_tree):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(BLACK)

        for obstacle in obstacles:
            pygame.draw.rect(screen, BLUE,
                             (obstacle[0] + ADJUST_VECTOR, obstacle[1] + ADJUST_VECTOR, obstacle[2], obstacle[3]))

        pygame.draw.circle(screen, YELLOW, (start_pt[0] + ADJUST_VECTOR, start_pt[1] + ADJUST_VECTOR), NODE_SIZE * 8)
        pygame.draw.circle(screen, GREEN, (goal_pt[0] + ADJUST_VECTOR, goal_pt[1] + ADJUST_VECTOR), NODE_SIZE * 8)

        pygame.draw.circle(screen, RED, (INNER_WIDTH + ADJUST_VECTOR, INNER_HEIGHT + ADJUST_VECTOR), NODE_SIZE * 10)

        for node in rrt_tree:
            pygame.draw.circle(screen, WHITE, (int(node.x + ADJUST_VECTOR), int(node.y + ADJUST_VECTOR)), NODE_SIZE)

            if node.parent:
                pygame.draw.line(screen, WHITE,
                                 (int(node.x + ADJUST_VECTOR), int(node.y + ADJUST_VECTOR)),
                                 (int(node.parent.x + ADJUST_VECTOR), int(node.parent.y + ADJUST_VECTOR)),
                                 NODE_SIZE // 2)

        if path:
            adjusted_path = [(node.x + ADJUST_VECTOR, node.y + ADJUST_VECTOR) for node in path]
            for i in range(1, len(adjusted_path)):
                pygame.draw.line(screen, RED, adjusted_path[i - 1], adjusted_path[i], NODE_SIZE * 4)

        for node in rrt_tree:
            if node.parent:
                pygame.draw.line(screen, WHITE,
                                 (int(node.x + ADJUST_VECTOR), int(node.y + ADJUST_VECTOR)),
                                 (int(node.parent.x + ADJUST_VECTOR), int(node.parent.y + ADJUST_VECTOR)),
                                 NODE_SIZE)

        if len(room_coords) > 1:
            pygame.draw.lines(screen, ORANGE, True,
                              [(x + ADJUST_VECTOR, y + ADJUST_VECTOR) for x, y in room_coords], NODE_SIZE)

        pygame.display.update()

    pygame.quit()