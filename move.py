class Move:
    """
    Describes one full chess move.

    Kept backward compatible with the original two-argument form
    (Move(start, end)) - every extra field is optional and defaults to
    "this is just a plain move with nothing special about it".
    """

    def __init__(
        self,
        start,
        end,
        piece=None,
        captured_piece=None,
        is_castle=False,
        rook_start=None,
        rook_end=None,
        is_en_passant=False,
        captured_square=None,
        is_promotion=False,
        promotion_choice=None,
    ):

        self.start_row = start[0]
        self.start_col = start[1]

        self.end_row = end[0]
        self.end_col = end[1]

        # The piece being moved (useful once it's already off the board
        # after apply_move()).
        self.piece = piece

        # The piece captured by this move, if any. For en passant this is
        # NOT the piece on (end_row, end_col) - see captured_square below.
        self.captured_piece = captured_piece

        # Castling: also relocate a rook as part of this one move.
        self.is_castle = is_castle
        self.rook_start = rook_start
        self.rook_end = rook_end

        # En passant: the captured pawn sits on a different square than
        # the destination square.
        self.is_en_passant = is_en_passant
        self.captured_square = captured_square

        # Promotion: destination reaches the final rank. promotion_choice
        # is filled in later (a Piece subclass), once the player picks
        # from the promotion UI - it is None until then.
        self.is_promotion = is_promotion
        self.promotion_choice = promotion_choice

    @property
    def start(self):
        return (self.start_row, self.start_col)

    @property
    def end(self):
        return (self.end_row, self.end_col)

    def is_capture(self):
        return self.captured_piece is not None

    def __eq__(self, other):
        return (
            self.start_row == other.start_row
            and self.start_col == other.start_col
            and self.end_row == other.end_row
            and self.end_col == other.end_col
        )

    def __repr__(self):
        return f"({self.start_row},{self.start_col}) -> ({self.end_row},{self.end_col})"