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

            game.handle_click(pygame.mouse.get_pos())

    game.draw(screen)

    pygame.display.flip()

pygame.quit()