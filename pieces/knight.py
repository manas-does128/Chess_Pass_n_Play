from .piece import Piece


class Knight(Piece):

    def __init__(self, color):

        super().__init__(color)

        self.name = "Knight"

        self.symbol = "N"

    def get_moves(self, board, row, col):

        moves = []

        directions = [

            (-2, -1),
            (-2, 1),

            (-1, -2),
            (-1, 2),

            (1, -2),
            (1, 2),

            (2, -1),
            (2, 1)

        ]

        for dr, dc in directions:

            r = row + dr
            c = col + dc

            if not self.inside(r, c):
                continue

            target = board.get_piece(r, c)

            if target is None or self.enemy(target):

                moves.append((r, c))

        return moves