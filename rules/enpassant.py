# enpassant.py - En passant logic

from ..constants import PAWN, COLOR_WHITE


class EnPassantHandler:
    """Handles en passant capture validation and execution."""

    @staticmethod
    def check_en_passant_trigger(piece, start_row, end_row):
        """
        Determine if a pawn move creates an en passant opportunity.

        A pawn that advances two squares from its starting row creates
        an en passant target square on the square it passed through.

        Args:
            piece: The piece that just moved.
            start_row (int): The row the piece moved from.
            end_row (int): The row the piece moved to.

        Returns:
            tuple or None: The en passant target square (row, col), or None.
        """
        if piece.piece_type != PAWN:
            return None

        if abs(start_row - end_row) != 2:
            return None

        # The en passant target is the square the pawn "passed through"
        ep_row = (start_row + end_row) // 2
        return (ep_row, piece.col)

    @staticmethod
    def is_en_passant_capture(board, piece, target_row, target_col):
        """
        Check if a pawn move to (target_row, target_col) is an en passant capture.

        Args:
            board: The Board object.
            piece: The moving pawn.
            target_row (int): Destination row.
            target_col (int): Destination column.

        Returns:
            bool: True if this is an en passant capture.
        """
        if piece.piece_type != PAWN:
            return False

        if board.en_passant_square is None:
            return False

        if (target_row, target_col) != board.en_passant_square:
            return False

        # Pawn must be moving diagonally
        if abs(piece.col - target_col) != 1:
            return False

        return True

    @staticmethod
    def execute_en_passant(board, piece, target_row, target_col):
        """
        Execute an en passant capture.

        Removes the captured pawn from the board and moves the
        capturing pawn to the target square.

        Args:
            board: The Board object.
            piece: The capturing pawn.
            target_row (int): Destination row.
            target_col (int): Destination column.

        Returns:
            Piece: The captured pawn (for undo purposes).
        """
        # The captured pawn is on the same row as the capturing pawn,
        # in the target column
        captured_pawn_row = piece.row  # same row as attacker before move
        captured_pawn = board.get_piece(captured_pawn_row, target_col)

        # Remove captured pawn
        board.set_piece(captured_pawn_row, target_col, None)

        # Move attacking pawn
        board.set_piece(piece.row, piece.col, None)
        piece.move_to(target_row, target_col)
        board.set_piece(target_row, target_col, piece)

        return captured_pawn

    @staticmethod
    def get_captured_pawn_position(piece, target_col):
        """
        Get the position of the pawn that would be captured en passant.

        Args:
            piece: The capturing pawn.
            target_col (int): The column of the en passant target square.

        Returns:
            tuple: (row, col) of the pawn to be captured.
        """
        return (piece.row, target_col)
