import pygame
import os
import time

pygame.init()
pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(BASE_DIR, "assets", "sounds")

sounds = [
    "move.mp3",
    "capture.mp3",
    "check.mp3",
    "castle.mp3",
    "promotion.mp3",
    "game_over.mp3",
    "illegal.mp3",
]

for filename in sounds:

    path = os.path.join(SOUND_DIR, filename)

    print(f"\nPlaying: {filename}")
    print(f"Exists: {os.path.exists(path)}")

    if not os.path.exists(path):
        continue

    sound = pygame.mixer.Sound(path)

    sound.play()

    while pygame.mixer.get_busy():
        time.sleep(0.1)

    time.sleep(0.5)

pygame.quit()
