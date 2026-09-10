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

        # (row, col) of the square a pawn just skipped over on a two-square
        # first move, or None. Only ever valid for the ONE move right after
        # it's set - every call to apply_move() recomputes it from scratch,
        # so it naturally disappears the moment a different move is played.
        self.en_passant_target = None

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

    def get_pieces(self, color):
        """Return a list of (piece, row, col) for every piece of `color`."""

        result = []

        for row in range(8):

            for col in range(8):

                piece = self.get_piece(row, col)

                if piece is not None and piece.color == color:
                    result.append((piece, row, col))

        return result

    ##################################################
    # MOVE FUNCTIONS
    ##################################################

    def move_piece(self, start_row, start_col, end_row, end_col):
        """
        Simple, unconditional relocation of whatever is on the start
        square. Kept for backward compatibility / simple callers. Does
        NOT know about castling, en passant, or promotion - use
        apply_move() for a real Move that might carry that metadata.
        """

        piece = self.get_piece(start_row, start_col)

        self.set_piece(end_row, end_col, piece)

        self.remove_piece(start_row, start_col)

        if piece:
            piece.has_moved = True

    def apply_move(self, move):
        """
        Execute a fully-resolved Move (see move.py) on this board:
        handles plain moves, captures, castling (relocates the rook
        too), en passant (removes the captured pawn from the square it
        actually stands on), and promotion (swaps the pawn for the
        chosen piece). Also refreshes en_passant_target for the next
        move.

        For promotion moves, move.promotion_choice must already be set
        to a Piece subclass (Queen/Rook/Bishop/Knight) before calling
        this - the caller is responsible for pausing on the promotion
        UI and filling that in first.
        """

        moving_piece = self.get_piece(move.start_row, move.start_col)

        # En passant removes a pawn that is NOT on the destination square.
        if move.is_en_passant and move.captured_square is not None:
            self.remove_piece(*move.captured_square)

        # Move the primary piece.
        self.set_piece(move.end_row, move.end_col, moving_piece)
        self.remove_piece(move.start_row, move.start_col)

        if moving_piece is not None:
            moving_piece.has_moved = True

        # Castling also relocates the rook.
        if move.is_castle and move.rook_start is not None and move.rook_end is not None:

            rook = self.get_piece(*move.rook_start)

            self.set_piece(move.rook_end[0], move.rook_end[1], rook)
            self.remove_piece(move.rook_start[0], move.rook_start[1])

            if rook is not None:
                rook.has_moved = True

        # Promotion swaps the pawn for the chosen piece on the
        # destination square.
        if move.is_promotion and move.promotion_choice is not None:

            promoted = move.promotion_choice(moving_piece.color)
            promoted.has_moved = True

            self.set_piece(move.end_row, move.end_col, promoted)

        self._update_en_passant_target(move, moving_piece)

    def _update_en_passant_target(self, move, moving_piece):

        if (
            isinstance(moving_piece, Pawn)
            and abs(move.end_row - move.start_row) == 2
            and move.start_col == move.end_col
        ):

            mid_row = (move.start_row + move.end_row) // 2

            self.en_passant_target = (mid_row, move.start_col)

        else:

            self.en_passant_target = None

    ##################################################
    # MOVE GENERATOR (PSEUDO-LEGAL - ignores king safety)
    ##################################################

    def get_valid_moves(self, row, col):

        piece = self.get_piece(row, col)

        if piece is None:
            return []

        return piece.get_moves(self, row, col)

    ##################################################
    # KING / ATTACK QUERIES (used by rules/check.py)
    ##################################################

    def get_king(self, color):
        """Return (row, col) of the given color's king, or None."""

        for row in range(8):

            for col in range(8):

                piece = self.get_piece(row, col)

                if piece is not None and piece.color == color and isinstance(piece, King):

                    return (row, col)

        return None

    def is_square_attacked(self, row, col, by_color):
        """
        Return True if any piece belonging to `by_color` attacks (row, col).

        Pawns are handled as a special case: their forward move is not an
        attack (it requires an empty square), only their two diagonal
        squares are. Every other piece's pseudo-legal move set already
        equals its attack set (sliding pieces stop at the first blocker,
        knights/king only add empty-or-enemy squares), so get_moves() is
        reused directly for them.
        """

        for r in range(8):

            for c in range(8):

                piece = self.get_piece(r, c)

                if piece is None or piece.color != by_color:
                    continue

                if isinstance(piece, Pawn):

                    direction = -1 if piece.color == "white" else 1

                    if r + direction == row and abs(c - col) == 1:
                        return True

                    continue

                if (row, col) in piece.get_moves(self, r, c):
                    return True

        return False

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