class Square:
    """
    Represents one square on the chessboard.
    """

    def __init__(self, row, col, piece=None):

        self.row = row
        self.col = col

        self.piece = piece

    def is_empty(self):
        return self.piece is None

    def has_piece(self):
        return self.piece is not None

    def has_enemy(self, color):
        return self.has_piece() and self.piece.color != color

    def has_friend(self, color):
        return self.has_piece() and self.piece.color == color

    def __repr__(self):
        return f"Square({self.row}, {self.col})"