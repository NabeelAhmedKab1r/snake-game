import pygame
import math
import random

from settings import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT,
    NEON_YELLOW, NEON_ORANGE
)


class Food:
    def __init__(self):
        self.pos = (0, 0)

    # -----------------------------------
    # Spawn at a random tile not occupied
    # -----------------------------------
    def respawn(self, snake_body, obstacles):
        occupied = set(snake_body) | set(obstacles)
        while True:
            pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if pos not in occupied:
                self.pos = pos
                return

    # -----------------------------------
    # Draw normal pulsing neon food
    # -----------------------------------
    def draw(self, surface, time_sec):
        fx, fy = self.pos
        base_x = fx * GRID_SIZE
        base_y = fy * GRID_SIZE

        # pulse scale
        pulse = 0.25 * math.sin(time_sec * 4.0)
        scale = 0.7 + pulse
        size = int(GRID_SIZE * scale)
        offset = (GRID_SIZE - size) // 2

        center_rect = pygame.Rect(
            base_x + offset,
            base_y + offset,
            size,
            size
        )

        # Glow
        glow_size = int(GRID_SIZE * (scale + 0.5))
        glow_offset = (GRID_SIZE - glow_size) // 2
        glow_rect = pygame.Rect(
            base_x + glow_offset,
            base_y + glow_offset,
            glow_size,
            glow_size
        )

        glow_surf = pygame.Surface(
            (glow_rect.width, glow_rect.height),
            pygame.SRCALPHA
        )
        pygame.draw.ellipse(
            glow_surf,
            (*NEON_ORANGE, 90),
            glow_surf.get_rect()
        )
        surface.blit(glow_surf, (glow_rect.x, glow_rect.y))

        # Center
        pygame.draw.rect(surface, NEON_YELLOW, center_rect, border_radius=8)
