from .piece import Piece


class Bishop(Piece):

    def __init__(self, color):

        super().__init__(color)

        self.name = "Bishop"

        self.symbol = "B"

    def get_moves(self, board, row, col):

        moves = []

        directions = [

            (-1, -1),
            (-1, 1),

            (1, -1),
            (1, 1)

        ]

        for dr, dc in directions:

            r = row
            c = col

            while True:

                r += dr
                c += dc

                if not self.inside(r, c):
                    break

                target = board.get_piece(r, c)

                if target is None:

                    moves.append((r, c))

                elif self.enemy(target):

                    moves.append((r, c))
                    break

                else:

                    break

        return moves