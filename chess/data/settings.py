import pygame

# Screen components
TILE_SIZE = 64
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_SIZE = TILE_SIZE * 8
BOARD_X = (SCREEN_WIDTH-BOARD_SIZE)//2
BOARD_Y = int((SCREEN_HEIGHT / 2) - (BOARD_SIZE / 2))
IMG_SCALE = (TILE_SIZE, TILE_SIZE)

# Colors
WHITE = (255, 255, 255)             # White
BLACK = (0, 0, 0)                   # Black

SMALL_TEXT_COLOR = (241, 250, 238)  # Pale White
LARGE_TEXT_COLOR = (230, 57, 70)    # Red

BG_COLOR = (29, 53, 87)             # Dark Blue
BG_COLOR_LIGHT = (70, 70, 70)       # Gray

TILE_COLOR_LIGHT = (241, 250, 238)  # White
TILE_COLOR_DARK = (69, 123, 157)    # Blue

HIGHLIGHT_COLOR = (51, 153, 255)    # Light Blue

# Create screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def to_coords(x, y):
    """Converts 8x8 grid positions to pixel coordinates

    :param x: x-axis coordinate
    :param y: y-axis coordinate
    :return: pixel coordinates (int)
    """

    return BOARD_X + x * TILE_SIZE, BOARD_Y + y * TILE_SIZE
