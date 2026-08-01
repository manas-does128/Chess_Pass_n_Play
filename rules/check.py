# check.py - Check and checkmate detection

from ..constants import COLOR_WHITE, COLOR_BLACK, KING


class CheckDetector:
    """Detects check, checkmate, and stalemate conditions."""

    @staticmethod
    def is_square_attacked(board, row, col, by_color):
        """
        Determine if a square is attacked by any piece of the given color.

        Args:
            board: The Board object.
            row (int): Target row.
            col (int): Target column.
            by_color (str): The attacking color ('white' or 'black').

        Returns:
            bool: True if the square is under attack.
        """
        for piece in board.get_pieces(by_color):
            possible_moves = piece.get_possible_moves(board)
            if (row, col) in possible_moves:
                return True
        return False

    @staticmethod
    def is_in_check(board, color):
        """
        Check whether the given color's king is in check.

        Args:
            board: The Board object.
            color (str): The color whose king to check.

        Returns:
            bool: True if the king is in check.
        """
        king = board.get_king(color)
        if king is None:
            return False
        enemy_color = COLOR_BLACK if color == COLOR_WHITE else COLOR_WHITE
        return CheckDetector.is_square_attacked(board, king.row, king.col, enemy_color)

    @staticmethod
    def is_checkmate(board, color):
        """
        Determine if the given color is in checkmate.

        Checkmate = in check AND no legal moves available.

        Args:
            board: The Board object.
            color (str): The color to test.

        Returns:
            bool: True if checkmate.
        """
        if not CheckDetector.is_in_check(board, color):
            return False
        return not CheckDetector._has_legal_moves(board, color)

    @staticmethod
    def is_stalemate(board, color):
        """
        Determine if the given color is in stalemate.

        Stalemate = NOT in check AND no legal moves available.

        Args:
            board: The Board object.
            color (str): The color to test.

        Returns:
            bool: True if stalemate.
        """
        if CheckDetector.is_in_check(board, color):
            return False
        return not CheckDetector._has_legal_moves(board, color)

    @staticmethod
    def _has_legal_moves(board, color):
        """
        Check if the given color has any legal moves.

        Tries every pseudo-legal move and tests whether it leaves
        the king in check. Returns True as soon as one legal move is found.
        """
        for piece in board.get_pieces(color):
            for move in piece.get_possible_moves(board):
                # Simulate the move and see if king is still in check
                if CheckDetector._is_move_legal(board, piece, move):
                    return True
        return False

    @staticmethod
    def _is_move_legal(board, piece, target_square):
        """
        Test if a move is legal by simulating it and checking for self-check.

        Args:
            board: The Board object.
            piece: The piece to move.
            target_square: (row, col) destination.

        Returns:
            bool: True if the move does not leave own king in check.
        """
        target_row, target_col = target_square

        # Save state
        original_row, original_col = piece.row, piece.col
        captured_piece = board.get_piece(target_row, target_col)

        # Make the move on the board
        board.set_piece(original_row, original_col, None)
        board.set_piece(target_row, target_col, piece)
        piece.row = target_row
        piece.col = target_col

        # Check if own king is in check after the move
        in_check = CheckDetector.is_in_check(board, piece.color)

        # Undo the move
        piece.row = original_row
        piece.col = original_col
        board.set_piece(original_row, original_col, piece)
        board.set_piece(target_row, target_col, captured_piece)

        return not in_check

    @staticmethod
    def get_checking_pieces(board, color):
        """
        Find all enemy pieces that are giving check to the given color's king.

        Args:
            board: The Board object.
            color (str): The color whose king is being checked.

        Returns:
            list[Piece]: List of enemy pieces delivering check.
        """
        king = board.get_king(color)
        if king is None:
            return []
        enemy_color = COLOR_BLACK if color == COLOR_WHITE else COLOR_WHITE
        checkers = []
        for piece in board.get_pieces(enemy_color):
            if (king.row, king.col) in piece.get_possible_moves(board):
                checkers.append(piece)
        return checkers
