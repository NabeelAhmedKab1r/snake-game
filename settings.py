import os

# Grid & window
GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 30
WINDOW_WIDTH = GRID_SIZE * GRID_WIDTH
WINDOW_HEIGHT = GRID_SIZE * GRID_HEIGHT

# Colors
BLACK = (5, 5, 10)
GRID_COLOR = (40, 40, 70)

WHITE = (255, 255, 255)
GRAY = (170, 170, 190)

NEON_GREEN = (0, 255, 150)
NEON_GREEN_HEAD = (120, 255, 200)

NEON_YELLOW = (255, 220, 100)
NEON_ORANGE = (255, 150, 50)

NEON_PINK = (255, 100, 200)
NEON_CYAN = (100, 220, 255)

OBSTACLE_COLOR = (140, 140, 170)

DIFFICULTY_NAMES = ["Easy", "Medium", "Hard", "Insane"]

# NEW — Snake skin colors
SNAKE_SKINS = {
    "green": ((0, 255, 150), (120, 255, 200)),
    "cyan":  ((50, 230, 255), (120, 255, 255)),
    "pink":  ((255, 120, 210), (255, 160, 240)),
}

# Data paths
DATA_DIR = "data"
HIGHSCORE_FILE = os.path.join(DATA_DIR, "highscore.txt")
COINS_FILE = os.path.join(DATA_DIR, "coins.txt")
SHOP_FILE = os.path.join(DATA_DIR, "shop.json")

os.makedirs(DATA_DIR, exist_ok=True)
