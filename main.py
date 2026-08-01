import pygame

from constants import *
from game import Game

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Chess")

clock = pygame.time.Clock()

game = Game()

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            x, y = pygame.mouse.get_pos()

            row = y // SQUARE_SIZE

            col = x // SQUARE_SIZE

            game.select(row, col)

    game.draw(screen)

    pygame.display.flip()

pygame.quit()