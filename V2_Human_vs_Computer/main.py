import pygame

from constants import *
from game import Game

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Chess")

clock = pygame.time.Clock()

# Minimal opponent selection for V2 Phase 1 - a plain terminal prompt,
# not a GUI menu. Answering "n" or just pressing Enter reproduces V1
# (Human vs Human) exactly.
answer = input("Play against the computer? (y/N): ").strip().lower()
vs_computer = answer.startswith("y")

game = Game(vs_computer=vs_computer)

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            game.handle_click(pygame.mouse.get_pos())

    game.draw(screen)

    pygame.display.flip()

pygame.quit()