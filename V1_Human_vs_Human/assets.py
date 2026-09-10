import pygame
import os
from constants import SQUARE_SIZE

IMAGES = {}

pieces = ["pawn", "rook", "knight", "bishop", "queen", "king"]

for color in ["white", "black"]:
    for piece in pieces:

        path = os.path.join(
            "assets",
            color,
            f"{piece}.png"
        )

        image = pygame.image.load(path)

        image = pygame.transform.smoothscale(
            image,
            (SQUARE_SIZE - 10, SQUARE_SIZE - 10)
        )

        IMAGES[f"{color}_{piece}"] = image