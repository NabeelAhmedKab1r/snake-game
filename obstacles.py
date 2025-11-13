import random
from settings import GRID_WIDTH, GRID_HEIGHT


def get_obstacles_for_difficulty(diff):
    total_tiles = GRID_WIDTH * GRID_HEIGHT

    if diff == 0:   # Easy
        count = total_tiles // 50
    elif diff == 1:  # Medium
        count = total_tiles // 35
    elif diff == 2:  # Hard
        count = total_tiles // 25
    else:            # Insane (reduced density)
        count = total_tiles // 18

    obstacles = set()
    while len(obstacles) < count:
        ox = random.randint(0, GRID_WIDTH - 1)
        oy = random.randint(0, GRID_HEIGHT - 1)
        obstacles.add((ox, oy))

    return list(obstacles)
