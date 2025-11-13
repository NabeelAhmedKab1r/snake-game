import pygame
import random
import math


class Particle:
    def __init__(self, x, y, size, vx, vy, life, color):
        self.x = x
        self.y = y
        self.size = size
        self.vx = vx
        self.vy = vy
        self.life = life
        self.color = color

    def update(self, dt):
        self.life -= dt
        self.x += self.vx * dt
        self.y += self.vy * dt


def spawn_particles(particles, grid_pos, grid_size):
    gx, gy = grid_pos
    base_x = gx * grid_size + grid_size / 2
    base_y = gy * grid_size + grid_size / 2

    for _ in range(12):
        angle = random.random() * math.tau
        speed = random.uniform(40, 140)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        size = random.randint(2, 5)
        life = random.uniform(0.2, 0.6)
        color = (
            random.randint(150, 255),
            random.randint(80, 255),
            random.randint(150, 255)
        )
        particles.append(Particle(base_x, base_y, size, vx, vy, life, color))


def update_particles(particles, dt):
    particles[:] = [p for p in particles if p.life > 0]
    for p in particles:
        p.update(dt)


def draw_particles(surface, particles):
    for p in particles:
        rect = pygame.Rect(int(p.x), int(p.y), p.size, p.size)
        pygame.draw.rect(surface, p.color, rect)
