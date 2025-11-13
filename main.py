import pygame
import sys

from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    COINS_FILE, SHOP_FILE
)

from shop import load_shop, save_shop, load_coins, save_coins, show_shop
from game import main_menu, run_game, load_high_score
from settings import SNAKE_SKINS


# ----------------------------------------
# Safe sound loader (avoids crash if missing)
# ----------------------------------------
def safe_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        return None


# ----------------------------------------
# MAIN ENTRY POINT
# ----------------------------------------
def main():
    pygame.init()
    pygame.mixer.init()

    # Window (Resizable)
    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT),
        pygame.RESIZABLE
    )
    pygame.display.set_caption("Snake Neon")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 24)

    # ----------------------------------------
    # Load data files
    # ----------------------------------------
    coins = load_coins()
    shop_state = load_shop()
    high_score = load_high_score()

    # Ensure default skin exists
    if "snake_skin" not in shop_state:
        shop_state["snake_skin"] = "green"
        save_shop(shop_state)

    # ----------------------------------------
    # Load sound effects
    # ----------------------------------------
    sfx_eat = safe_sound("assets/sfx/eat.wav")
    sfx_special = safe_sound("assets/sfx/special.wav")
    sfx_gameover = safe_sound("assets/sfx/gameover.wav")

    # Make available globally (import inside functions)
    import game
    game.sfx_eat = sfx_eat
    game.sfx_special = sfx_special
    game.sfx_gameover = sfx_gameover

    # ----------------------------------------
    # GAME LOOP (menu → game → menu → shop…)
    # ----------------------------------------
    while True:

        # Bring user to main menu
        action, diff_index = main_menu(screen, font, coins)

        # Quit
        if action == "quit":
            save_coins(coins)
            save_shop(shop_state)
            pygame.quit()
            sys.exit()

        # Open Shop
        elif action == "shop":
            new_shop_state, new_coins = show_shop(screen, font, coins, shop_state)

            shop_state = new_shop_state
            coins = new_coins

            save_coins(coins)
            save_shop(shop_state)

        # Start Game
        elif action == "play":
            score, high_score, coins, quit_now = run_game(
                screen, clock, diff_index, shop_state, coins, high_score
            )

            save_coins(coins)
            save_shop(shop_state)

            if quit_now:
                pygame.quit()
                sys.exit()


# Entry point
if __name__ == "__main__":
    main()
