from square import Square

from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.knight import Knight
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.king import King

from assets import IMAGES
from constants import SQUARE_SIZE


class Board:

    def __init__(self):

        self.squares = [
            [Square(r, c) for c in range(8)]
            for r in range(8)
        ]

        self.setup_board()

    ##################################################
    # INITIAL SETUP
    ##################################################

    def setup_board(self):

        # Black Pieces
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for col, piece in enumerate(order):
            self.squares[0][col].piece = piece("black")
            self.squares[7][col].piece = piece("white")

        for col in range(8):
            self.squares[1][col].piece = Pawn("black")
            self.squares[6][col].piece = Pawn("white")

    ##################################################
    # BASIC FUNCTIONS
    ##################################################

    def inside(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def get_square(self, row, col):
        return self.squares[row][col]

    def get_piece(self, row, col):
        return self.squares[row][col].piece

    def set_piece(self, row, col, piece):
        self.squares[row][col].piece = piece

    def remove_piece(self, row, col):
        self.squares[row][col].piece = None

    def is_empty(self, row, col):
        return self.get_piece(row, col) is None

    ##################################################
    # MOVE FUNCTIONS
    ##################################################

    def move_piece(self, start_row, start_col, end_row, end_col):

        piece = self.get_piece(start_row, start_col)

        self.set_piece(end_row, end_col, piece)

        self.remove_piece(start_row, start_col)

        if piece:
            piece.has_moved = True

    ##################################################
    # MOVE GENERATOR
    ##################################################

    def get_valid_moves(self, row, col):

        piece = self.get_piece(row, col)

        if piece is None:
            return []

        return piece.get_moves(self, row, col)

    ##################################################
    # DRAW
    ##################################################

    def draw(self, screen):

        padding = 8

        for row in range(8):

            for col in range(8):

                piece = self.get_piece(row, col)

                if piece is None:
                    continue

                key = f"{piece.color}_{piece.name.lower()}"

                image = IMAGES[key]

                screen.blit(
                    image,
                    (
                        col * SQUARE_SIZE + padding,
                        row * SQUARE_SIZE + padding,
                    ),
                )

    ##################################################
    # DEBUG
    ##################################################

    def print_board(self):

        for row in self.squares:

            line = []

            for square in row:

                if square.piece:

                    line.append(square.piece.symbol)

                else:

                    line.append(".")

            print(" ".join(line))