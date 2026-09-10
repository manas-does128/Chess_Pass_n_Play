import pygame

# Window
WIDTH = 800
HEIGHT = 800

ROWS = 8
COLS = 8

SQUARE_SIZE = WIDTH // COLS

FPS = 60

# Board colors
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)

# UI colors
HIGHLIGHT = (0, 255, 0)
MOVE = (100, 255, 100)
CHECK_COLOR = (255, 0, 0)
SELECTED = (50, 150, 255)
CAPTURE = (255, 100, 100)

# Player colors
WHITE = "white"
BLACK = "black"

COLOR_WHITE = WHITE
COLOR_BLACK = BLACK

# Piece types
PAWN = "pawn"
ROOK = "rook"
KNIGHT = "knight"
BISHOP = "bishop"
QUEEN = "queen"
KING = "king"

# Game state
ONGOING = "ongoing"
CHECK = "check"
CHECKMATE = "checkmate"
STALEMATE = "stalemate"

# Castling sides
KINGSIDE = "kingside"
QUEENSIDE = "queenside"

# Promotion choices
PROMOTION_CHOICES = [
    QUEEN,
    ROOK,
    BISHOP,
    KNIGHT
]

# Overlay / panel UI (game-over screen, promotion picker)
OVERLAY_COLOR = (0, 0, 0)
OVERLAY_ALPHA = 170
PANEL_COLOR = (245, 245, 245)
PANEL_BORDER = (30, 30, 30)
BUTTON_COLOR = (70, 130, 70)
BUTTON_BORDER = (20, 20, 20)
BUTTON_TEXT_COLOR = (255, 255, 255)
PROMOTION_BUTTON_BG = (235, 235, 235)