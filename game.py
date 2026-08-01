import pygame

from board import Board
from constants import *


class Game:

    def __init__(self):

        self.board = Board()

        self.turn = "white"

        self.selected = None

        self.valid_moves = []

    ##################################################
    # DRAW
    ##################################################

    def draw(self, screen):

        self.draw_board(screen)

        self.highlight_selection(screen)

        self.highlight_moves(screen)

        self.board.draw(screen)

    ##################################################
    # BOARD
    ##################################################

    def draw_board(self, screen):

        for row in range(ROWS):

            for col in range(COLS):

                color = LIGHT if (row + col) % 2 == 0 else DARK

                pygame.draw.rect(

                    screen,

                    color,

                    (

                        col * SQUARE_SIZE,

                        row * SQUARE_SIZE,

                        SQUARE_SIZE,

                        SQUARE_SIZE

                    )

                )

    ##################################################
    # HIGHLIGHTS
    ##################################################

    def highlight_selection(self, screen):

        if self.selected is None:
            return

        row, col = self.selected

        pygame.draw.rect(

            screen,

            (0, 0, 255),

            (

                col * SQUARE_SIZE,

                row * SQUARE_SIZE,

                SQUARE_SIZE,

                SQUARE_SIZE

            ),

            4

        )

    def highlight_moves(self, screen):

        radius = 10

        for row, col in self.valid_moves:

            pygame.draw.circle(

                screen,

                (0, 255, 0),

                (

                    col * SQUARE_SIZE + SQUARE_SIZE // 2,

                    row * SQUARE_SIZE + SQUARE_SIZE // 2

                ),

                radius

            )

    ##################################################
    # MOUSE
    ##################################################

    def select(self, row, col):

        piece = self.board.get_piece(row, col)

        # Nothing selected yet
        if self.selected is None:

            if piece is None:
                return

            if piece.color != self.turn:
                return

            self.selected = (row, col)

            self.valid_moves = self.board.get_valid_moves(row, col)

            return

        # Already selected

        start_row, start_col = self.selected

        # Clicking own piece changes selection
        if piece and piece.color == self.turn:

            self.selected = (row, col)

            self.valid_moves = self.board.get_valid_moves(row, col)

            return

        # Move if legal
        if (row, col) in self.valid_moves:

            self.board.move_piece(

                start_row,

                start_col,

                row,

                col

            )

            self.change_turn()

        self.selected = None

        self.valid_moves = []

    ##################################################
    # TURN
    ##################################################

    def change_turn(self):

        if self.turn == "white":

            self.turn = "black"

        else:

            self.turn = "white"