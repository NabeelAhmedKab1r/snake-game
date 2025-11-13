import pygame
from settings import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT

def wrap_position(x, y):
    return x % GRID_WIDTH, y % GRID_HEIGHT

class Snake:
    def __init__(self, skin_colors):
        self.skin_body, self.skin_head = skin_colors
        self.reset()

    def reset(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2 - 3)]
        self.direction = (1, 0)
        self.pending_dir = self.direction

    def set_direction(self, dx, dy):
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.pending_dir = (dx, dy)

    def step(self):
        self.direction = self.pending_dir
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = wrap_position(head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        return new_head

    def pop_tail(self):
        self.body.pop()

    def collides_with_self(self, pos=None):
        if pos is None:
            pos = self.body[0]
        return pos in self.body[1:]

    def draw(self, surface):
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)

            # shadow
            shadow = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(shadow, (0, 0, 0, 140), shadow.get_rect(), border_radius=7)
            surface.blit(shadow, (rect.x + 2, rect.y + 2))

            if i == 0:
                pygame.draw.rect(surface, self.skin_head, rect, border_radius=8)
            else:
                pygame.draw.rect(surface, self.skin_body, rect, border_radius=6)
