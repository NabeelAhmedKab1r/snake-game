import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, GRID_COLOR


def draw_gradient_background(surface):
    for y in range(WINDOW_HEIGHT):
        ratio = y / WINDOW_HEIGHT
        r = int(10 + ratio * 20)
        g = int(10 + ratio * 30)
        b = int(20 + ratio * 50)
        pygame.draw.line(surface, (r, g, b), (0, y), (WINDOW_WIDTH, y))


def draw_grid(surface):
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))
