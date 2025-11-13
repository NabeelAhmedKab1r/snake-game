import pygame
import json
import os

from settings import SHOP_FILE, COINS_FILE, SNAKE_SKINS, WHITE, GRAY, NEON_YELLOW


# ------------------------------
# LOADING / SAVING
# ------------------------------

def load_shop():
    if not os.path.exists(SHOP_FILE):
        return {"snake_skin": "green", "owned": ["green"], "boost_double_coins": False}

    try:
        with open(SHOP_FILE, "r") as f:
            return json.load(f)
    except:
        return {"snake_skin": "green", "owned": ["green"], "boost_double_coins": False}


def save_shop(data):
    try:
        with open(SHOP_FILE, "w") as f:
            json.dump(data, f)
    except:
        pass


def load_coins():
    try:
        with open(COINS_FILE, "r") as f:
            return int(f.read().strip() or "0")
    except:
        return 0


def save_coins(amount):
    try:
        with open(COINS_FILE, "w") as f:
            f.write(str(amount))
    except:
        pass


# ------------------------------
# SHOP ITEMS
# ------------------------------

ITEMS = [
    {"name": "Green Skin", "id": "green", "price": 0},
    {"name": "Cyan Skin", "id": "cyan", "price": 20},
    {"name": "Pink Skin", "id": "pink", "price": 20},
    {"name": "Double Coins Boost", "id": "boost_double_coins", "price": 50}
]


# ------------------------------
# SHOP UI
# ------------------------------

def show_shop(screen, font, coins, shop_state):
    clock = pygame.time.Clock()
    selected = 0

    while True:
        screen.fill((15, 15, 25))

        # Title
        title = font.render("SHOP", True, WHITE)
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 40))

        # Coins
        coins_text = font.render(f"Coins: {coins}", True, NEON_YELLOW)
        screen.blit(coins_text, (20, 20))

        # Draw items
        y_start = 120
        for i, item in enumerate(ITEMS):
            color = WHITE if i == selected else GRAY
            txt = font.render(f"{item['name']} — {item['price']}c", True, color)
            screen.blit(txt, (80, y_start + i * 40))

            # If owned
            owned = shop_state.get("owned", [])
            if item["id"] in owned or shop_state.get(item["id"], False):
                owned_mark = font.render("(Owned)", True, NEON_YELLOW)
                screen.blit(owned_mark, (400, y_start + i * 40))

        # Instructions
        info = font.render("ENTER: Buy/Equip  |  ESC: Back", True, GRAY)
        screen.blit(info, (screen.get_width() // 2 - info.get_width() // 2,
                           screen.get_height() - 50))

        pygame.display.flip()

        # -------------------------
        # EVENTS
        # -------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return shop_state, coins

            if event.type == pygame.KEYDOWN:

                # Back to menu
                if event.key == pygame.K_ESCAPE:
                    return shop_state, coins

                # Navigation
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(ITEMS)

                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(ITEMS)

                # Buy / Equip
                elif event.key == pygame.K_RETURN:
                    item = ITEMS[selected]
                    item_id = item["id"]
                    price = item["price"]

                    owned_list = shop_state.get("owned", [])

                    # If already owned
                    if item_id in owned_list or shop_state.get(item_id, False):
                        # Equip skin if applicable
                        if item_id in SNAKE_SKINS:
                            shop_state["snake_skin"] = item_id
                            save_shop(shop_state)
                        continue  # DON'T EXIT SHOP

                    # Buy if enough coins
                    if coins >= price:
                        coins -= price

                        # Skins
                        if item_id in SNAKE_SKINS:
                            owned_list.append(item_id)
                            shop_state["snake_skin"] = item_id

                        # Boosts
                        else:
                            shop_state[item_id] = True

                        save_coins(coins)
                        save_shop(shop_state)

        clock.tick(60)
