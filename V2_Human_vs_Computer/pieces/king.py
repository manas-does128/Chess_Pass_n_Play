from .piece import Piece


class King(Piece):

    def __init__(self, color):

        super().__init__(color)

        self.name = "King"

        self.symbol = "K"

    def get_moves(self, board, row, col):

        moves = []

        directions = [

            (-1, -1),
            (-1, 0),
            (-1, 1),

            (0, -1),
            (0, 1),

            (1, -1),
            (1, 0),
            (1, 1)

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