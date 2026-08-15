# check.py - Check detection and king-safety move filtering
#
# This is the "rule validation layer": it takes the pseudo-legal moves a
# piece generates (piece.get_moves) and filters out any move that would
# leave that player's own king in check.
#
# Pattern (see get_legal_moves / _is_move_safe):
#
#     generate pseudo-legal move
#             |
#     temporarily make the move on the real board
#             |
#     is our own king attacked now?
#             |
#     YES -> illegal, undo          NO -> legal, undo
#
# This is the same generic simulate/undo approach for every piece, so
# pins, discovered checks, and double checks are all handled correctly
# without hard-coding any of them.
#
# Checkmate / stalemate detection is a separate step and is not in this
# file yet.


class CheckDetector:
    """Detects check and filters pseudo-legal moves for king safety."""

    @staticmethod
    def is_in_check(board, color):
        """Return True if `color`'s king is currently under attack."""

        king_pos = board.get_king(color)

        if king_pos is None:
            return False

        king_row, king_col = king_pos

        enemy_color = "black" if color == "white" else "white"

        return board.is_square_attacked(king_row, king_col, enemy_color)

    @staticmethod
    def get_legal_moves(board, row, col):
        """
        Return the fully legal moves for the piece at (row, col):
        pseudo-legal moves with anything that leaves the mover's own
        king in check removed.
        """

        piece = board.get_piece(row, col)

        if piece is None:
            return []

        legal_moves = []

        for end_row, end_col in piece.get_moves(board, row, col):

            if CheckDetector._is_move_safe(board, row, col, end_row, end_col, piece.color):

                legal_moves.append((end_row, end_col))

        return legal_moves

    @staticmethod
    def _is_move_safe(board, start_row, start_col, end_row, end_col, color):
        """
        Temporarily play the move on the real board, check whether
        `color`'s king is in check as a result, then always undo it.

        Deliberately bypasses board.move_piece() and never touches
        has_moved, so simulating a move can never corrupt future castling
        rights - only set_piece/remove_piece are used, both fully
        reversible.
        """

        moving_piece = board.get_piece(start_row, start_col)
        captured_piece = board.get_piece(end_row, end_col)

        # Make the move
        board.set_piece(end_row, end_col, moving_piece)
        board.remove_piece(start_row, start_col)

        king_in_check = CheckDetector.is_in_check(board, color)

        # Undo the move
        board.set_piece(start_row, start_col, moving_piece)
        board.set_piece(end_row, end_col, captured_piece)

        return not king_in_check