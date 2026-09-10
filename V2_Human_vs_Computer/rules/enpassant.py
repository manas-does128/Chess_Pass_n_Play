# enpassant.py - En passant logic
#
# Rewritten against the project's real Board/Piece API. Timing is
# tracked via board.en_passant_target (set fresh by Board.apply_move()
# after every single move - see board.py), not by inspecting piece
# history, so the opportunity automatically disappears the instant any
# other move is played.

from pieces.pawn import Pawn
from move import Move


class EnPassantHandler:
    """Handles en passant capture detection and legality."""

    @staticmethod
    def get_en_passant_move(board, row, col):
        """
        If the pawn at (row, col) has an en passant capture available
        RIGHT NOW, return the (not-yet-safety-checked) Move for it,
        else None.
        """

        piece = board.get_piece(row, col)

        if piece is None or not isinstance(piece, Pawn):
            return None

        target = board.en_passant_target

        if target is None:
            return None

        target_row, target_col = target

        direction = -1 if piece.color == "white" else 1

        # The capturing pawn must be one diagonal step from the target
        # square (i.e. sitting right next to the pawn that just double-
        # stepped, on the correct side to capture "forward").
        if row + direction != target_row:
            return None

        if abs(col - target_col) != 1:
            return None

        # The pawn being captured sits on the capturing pawn's own row,
        # in the target's column - NOT on the (empty) target square.
        captured_square = (row, target_col)
        captured_piece = board.get_piece(*captured_square)

        if (
            captured_piece is None
            or not isinstance(captured_piece, Pawn)
            or captured_piece.color == piece.color
        ):
            return None

        return Move(
            (row, col),
            (target_row, target_col),
            piece=piece,
            captured_piece=captured_piece,
            is_en_passant=True,
            captured_square=captured_square,
        )

    @staticmethod
    def is_safe(board, move, color):
        """
        Simulate the en passant capture and confirm it doesn't leave
        `color`'s own king in check (classic case: two pawns are the
        only thing blocking a rook/queen on the same rank as the king -
        capturing en passant removes one of them and opens a discovered
        check). Always undoes the simulation before returning.
        """

        from .check import CheckDetector

        moving_piece = board.get_piece(move.start_row, move.start_col)
        captured_piece = board.get_piece(*move.captured_square)

        # Simulate
        board.remove_piece(*move.captured_square)
        board.set_piece(move.end_row, move.end_col, moving_piece)
        board.remove_piece(move.start_row, move.start_col)

        king_in_check = CheckDetector.is_in_check(board, color)

        # Undo
        board.set_piece(move.start_row, move.start_col, moving_piece)
        board.remove_piece(move.end_row, move.end_col)
        board.set_piece(move.captured_square[0], move.captured_square[1], captured_piece)

        return not king_in_check