import pygame
import math
import random

from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE,
    WHITE, GRAY, DIFFICULTY_NAMES,
    HIGHSCORE_FILE, NEON_YELLOW, OBSTACLE_COLOR,
    SNAKE_SKINS
)

from theme import draw_gradient_background, draw_grid
from obstacles import get_obstacles_for_difficulty
from snake import Snake
from food import Food
from particles import spawn_particles, update_particles, draw_particles
from shop import load_shop, load_coins, save_coins, save_shop
import os


# ---------------------------
# HIGH SCORE HELPERS
# ---------------------------

def load_high_score():
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read().strip() or "0")
    except:
        return 0

def save_high_score(score):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(int(score)))
    except:
        pass


# ---------------------------
# RAINBOW COLOR (for SPECIAL FOOD)
# ---------------------------

def rainbow_color(t):
    r = int((math.sin(t) + 1) * 127.5)
    g = int((math.sin(t + 2) + 1) * 127.5)
    b = int((math.sin(t + 4) + 1) * 127.5)
    return (r, g, b)


# ---------------------------
# MAIN MENU (with glow title)
# ---------------------------

def main_menu(screen, font, coins):
    clock = pygame.time.Clock()
    selected_diff_index = 1  # Medium default

    while True:
        draw_gradient_background(screen)
        t = pygame.time.get_ticks() / 1000.0

        # Neon pulsing color
        glow = int((math.sin(t * 2) + 1) * 127)
        title_color = (glow, 80, 255)

        title = font.render("SNAKE NEON", True, title_color)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 60))

        play_text = font.render("Press ENTER to Play", True, WHITE)
        screen.blit(play_text, (WINDOW_WIDTH // 2 - play_text.get_width() // 2, 120))

        shop_text = font.render("Press S for Shop", True, WHITE)
        screen.blit(shop_text, (WINDOW_WIDTH // 2 - shop_text.get_width() // 2, 160))

        diff_label = font.render("Difficulty:", True, GRAY)
        screen.blit(diff_label, (WINDOW_WIDTH // 2 - diff_label.get_width() // 2, 230))

        for i, name in enumerate(DIFFICULTY_NAMES):
            color = WHITE if i == selected_diff_index else GRAY
            text = font.render(name, True, color)

            x = WINDOW_WIDTH // 2 - text.get_width() // 2
            y = 270 + i * 30
            screen.blit(text, (x, y))

            if i == selected_diff_index:
                arrow = font.render(">", True, color)
                screen.blit(arrow, (x - 30, y))

        # Coin display
        coins_text = font.render(f"Coins: {coins}", True, WHITE)
        screen.blit(coins_text, (20, WINDOW_HEIGHT - 40))

        quit_text = font.render("Press Q to Quit", True, GRAY)
        screen.blit(quit_text, (WINDOW_WIDTH // 2 - quit_text.get_width() // 2,
                                WINDOW_HEIGHT - 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", selected_diff_index
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    return "quit", selected_diff_index

                elif event.key == pygame.K_s:
                    return "shop", selected_diff_index

                elif event.key in (pygame.K_UP, pygame.K_w):
                    selected_diff_index = (selected_diff_index - 1) % len(DIFFICULTY_NAMES)

                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected_diff_index = (selected_diff_index + 1) % len(DIFFICULTY_NAMES)

                elif event.key == pygame.K_RETURN:
                    return "play", selected_diff_index

        clock.tick(60)


# ---------------------------
# GAME LOOP
# ---------------------------

def run_game(screen, clock, diff_index, shop_state, coins, high_score):

    # SKIN SELECTION
    skin_id = shop_state.get("snake_skin", "green")
    snake = Snake(SNAKE_SKINS[skin_id])

    food = Food()
    obstacles = get_obstacles_for_difficulty(diff_index)
    food.respawn(snake.body, obstacles)

    # SPECIAL FOOD
    special_food = None
    special_expire = 0
    next_special_spawn = pygame.time.get_ticks() / 1000.0 + 20  # every 20 seconds

    score = 0
    particles = []
    base_speed = 10
    game_over = False
    new_high = False
    last_time = pygame.time.get_ticks() / 1000.0

    running = True

    while running:
        current_time = pygame.time.get_ticks() / 1000.0
        dt = current_time - last_time
        last_time = current_time

        # -------------------------------------
        # INPUT HANDLING
        # -------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score, high_score, coins, True

            if event.type == pygame.KEYDOWN:

                # Movement
                if event.key in (pygame.K_UP, pygame.K_w):
                    snake.set_direction(0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    snake.set_direction(0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    snake.set_direction(-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    snake.set_direction(1, 0)

                # Restart
                elif event.key == pygame.K_r and game_over:
                    running = False

        # -------------------------------------
        # SPECIAL FOOD SPAWN
        # -------------------------------------
        if special_food is None and current_time >= next_special_spawn:
            special_food = Food()
            special_food.respawn(snake.body, obstacles)
            special_expire = current_time + 3  # lasts 3 seconds
            next_special_spawn = current_time + 20

        if special_food and current_time >= special_expire:
            special_food = None

        # -------------------------------------
        # GAME LOGIC
        # -------------------------------------
        if not game_over:
            new_head = snake.step()

            # collisions
            if snake.collides_with_self(new_head) or new_head in obstacles:
                game_over = True
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                    new_high = True

            else:
                # SPECIAL FOOD
                if special_food and new_head == special_food.pos:
                    score += 3
                    coins += 5 if shop_state.get("boost_double_coins") else 3
                    spawn_particles(particles, new_head, GRID_SIZE)
                    special_food = None

                # NORMAL FOOD
                elif new_head == food.pos:
                    score += 1
                    coins += 2 if shop_state.get("boost_double_coins") else 1
                    spawn_particles(particles, new_head, GRID_SIZE)
                    food.respawn(snake.body, obstacles)

                else:
                    snake.pop_tail()

        update_particles(particles, dt)

        # -------------------------------------
        # DRAW EVERYTHING
        # -------------------------------------
        draw_gradient_background(screen)
        draw_grid(screen)

        # Obstacles
        for (ox, oy) in obstacles:
            rect = pygame.Rect(ox * GRID_SIZE, oy * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, OBSTACLE_COLOR, rect, border_radius=5)

        # Food
        food.draw(screen, current_time)

        # Special food (rainbow)
        if special_food:
            color = rainbow_color(current_time * 5)
            pygame.draw.circle(
                screen, color,
                (special_food.pos[0] * GRID_SIZE + GRID_SIZE // 2,
                 special_food.pos[1] * GRID_SIZE + GRID_SIZE // 2),
                GRID_SIZE // 2
            )

        # Snake
        snake.draw(screen)

        # Particles
        draw_particles(screen, particles)

        # -------------------------------------
        # GAME OVER UI
        # -------------------------------------
        if game_over:
            font_big = pygame.font.SysFont("consolas", 26)
            font_small = pygame.font.SysFont("consolas", 22)

            msg = font_big.render("Game Over! Press R to return to menu", True, WHITE)
            screen.blit(msg, (WINDOW_WIDTH // 2 - msg.get_width() // 2,
                              WINDOW_HEIGHT // 2 - 20))

            hs = font_small.render(f"High Score: {high_score}", True, WHITE)
            screen.blit(hs, (WINDOW_WIDTH // 2 - hs.get_width() // 2,
                              WINDOW_HEIGHT // 2 + 20))

            if new_high:
                nh = font_small.render("NEW HIGH SCORE!", True, NEON_YELLOW)
                screen.blit(nh, (WINDOW_WIDTH // 2 - nh.get_width() // 2,
                                  WINDOW_HEIGHT // 2 + 50))

        pygame.display.flip()

        speed = base_speed + score // 3
        clock.tick(speed)

    return score, high_score, coins, False
