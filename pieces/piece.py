# Base class for all chess pieces


class Piece:

    def __init__(self, color):

        self.color = color

        self.name = ""

        self.symbol = ""

        self.has_moved = False

    def inside(self, row, col):
        """Check if the given position is within the board boundaries."""

        return 0 <= row < 8 and 0 <= col < 8

    def enemy(self, other):
        """Check if the other piece is an enemy (different color)."""

        if other is None:
            return False

        return self.color != other.color

    def get_moves(self, board, row, col):
        """Return a list of valid moves. Subclasses must override this."""

        raise NotImplementedError("Subclasses must implement get_moves")

    def __repr__(self):

        return f"{self.color} {self.name}"
