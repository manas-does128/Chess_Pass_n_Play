from .piece import Piece


class Pawn(Piece):

    def __init__(self, color):

        super().__init__(color)

        self.name = "Pawn"

        self.symbol = "P"

    def get_moves(self, board, row, col):

        moves = []

        direction = -1 if self.color == "white" else 1

        # One square forward
        if self.inside(row + direction, col):

            if board.get_piece(row + direction, col) is None:

                moves.append((row + direction, col))

                # Two squares on first move
                if not self.has_moved:

                    if board.get_piece(row + 2 * direction, col) is None:

                        moves.append((row + 2 * direction, col))

        # Diagonal captures
        for dc in (-1, 1):

            r = row + direction
            c = col + dc

            if self.inside(r, c):

                target = board.get_piece(r, c)

                if self.enemy(target):

                    moves.append((r, c))

        return moves