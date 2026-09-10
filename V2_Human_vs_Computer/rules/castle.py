# castle.py - Castling logic
#
# Rewritten against the project's real Board/Piece API: pieces do not
# store their own row/col (the Board's Square grid is the source of
# truth for position), and there is no piece_type attribute - isinstance
# checks against the actual piece classes are used instead.

from pieces.rook import Rook
from move import Move


class CastlingHandler:
    """Handles castling validation and execution."""

    # king_dest_col / rook_dest_col: where king/rook end up.
    # rook_col: the rook's starting column.
    # path_cols: squares that must be completely empty.
    # check_cols: squares (including the king's own square) that must
    #             not be attacked - covers "can't castle out of, through,
    #             or into check".
    CASTLING_CONFIG = {
        "kingside": {
            "king_dest_col": 6,
            "rook_col": 7,
            "rook_dest_col": 5,
            "path_cols": [5, 6],
            "check_cols": [4, 5, 6],
        },
        "queenside": {
            "king_dest_col": 2,
            "rook_col": 0,
            "rook_dest_col": 3,
            "path_cols": [1, 2, 3],
            "check_cols": [4, 3, 2],
        },
    }

    @staticmethod
    def get_castling_moves(board, color):
        """
        Return a list of legal castling Move objects for `color`'s king,
        given the board's CURRENT state (called fresh each time a king
        is selected - nothing is cached).
        """

        from .check import CheckDetector

        king_pos = board.get_king(color)

        if king_pos is None:
            return []

        row, col = king_pos

        king = board.get_piece(row, col)

        if king is None or king.has_moved:
            return []

        # Can't castle while in check.
        if CheckDetector.is_in_check(board, color):
            return []

        enemy_color = "black" if color == "white" else "white"

        moves = []

        for side, config in CastlingHandler.CASTLING_CONFIG.items():

            rook_row, rook_col = row, config["rook_col"]

            rook = board.get_piece(rook_row, rook_col)

            if (
                rook is None
                or not isinstance(rook, Rook)
                or rook.color != color
                or rook.has_moved
            ):
                continue

            # Every square strictly between king and rook must be empty.
            path_clear = all(
                board.get_piece(row, c) is None
                for c in config["path_cols"]
            )

            if not path_clear:
                continue

            # King must not start on, pass through, or land on an
            # attacked square.
            squares_safe = all(
                not board.is_square_attacked(row, c, enemy_color)
                for c in config["check_cols"]
            )

            if not squares_safe:
                continue

            moves.append(
                Move(
                    (row, col),
                    (row, config["king_dest_col"]),
                    piece=king,
                    is_castle=True,
                    rook_start=(rook_row, rook_col),
                    rook_end=(row, config["rook_dest_col"]),
                )
            )

        return moves