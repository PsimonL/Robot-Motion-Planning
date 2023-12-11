import numpy as np

size = 650
inner_size = 600
WIDTH, HEIGHT = size, size
INNER_WIDTH, INNER_HEIGHT = inner_size, inner_size
ADJUST_VECTOR = (size - inner_size) // 2

NODE_SIZE = 1

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# NUM_ROWS = ((INNER_WIDTH) // 100) + 1
# NUM_COLS = ((INNER_HEIGHT) // 100) + 1
NUM_ROWS = ((INNER_WIDTH) // 5) + 1
NUM_COLS = ((INNER_HEIGHT) // 5) + 1
# NUM_ROWS = INNER_WIDTH
# NUM_COLS = INNER_HEIGHT

THRASH_NODES = np.array([], dtype=object)