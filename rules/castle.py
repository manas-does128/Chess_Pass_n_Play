# castle.py - Castling logic

from ..constants import (
    COLOR_WHITE, COLOR_BLACK, KING, ROOK,
    KINGSIDE, QUEENSIDE
)


class CastlingHandler:
    """Handles castling validation and execution."""

    # Castling configuration: (king_col, rook_col, king_dest_col, rook_dest_col, check_cols)
    CASTLING_CONFIG = {
        KINGSIDE: {
            'king_dest_col': 6,
            'rook_col': 7,
            'rook_dest_col': 5,
            'path_cols': [5, 6],       # Squares that must be empty
            'check_cols': [4, 5, 6],   # Squares that must not be attacked
        },
        QUEENSIDE: {
            'king_dest_col': 2,
            'rook_col': 0,
            'rook_dest_col': 3,
            'path_cols': [1, 2, 3],    # Squares that must be empty
            'check_cols': [2, 3, 4],   # Squares that must not be attacked
        },
    }

    @staticmethod
    def get_castling_moves(board, king):
        """
        Return a list of valid castling moves for the given king.

        Args:
            board: The Board object.
            king: The King piece.

        Returns:
            list[tuple]: List of (row, col) destinations for castling.
        """
        from .check import CheckDetector

        moves = []
        if king.has_moved:
            return moves

        # Can't castle while in check
        enemy_color = COLOR_BLACK if king.color == COLOR_WHITE else COLOR_WHITE
        if CheckDetector.is_in_check(board, king.color):
            return moves

        row = king.row

        for side, config in CastlingHandler.CASTLING_CONFIG.items():
            rook = board.get_piece(row, config['rook_col'])

            # Rook must exist, be a rook, be same color, and not have moved
            if (rook is None or
                    rook.piece_type != ROOK or
                    rook.color != king.color or
                    rook.has_moved):
                continue

            # Path between king and rook must be clear
            path_clear = all(
                board.get_piece(row, c) is None
                for c in config['path_cols']
            )
            if not path_clear:
                continue

            # King must not pass through or land on attacked squares
            squares_safe = all(
                not CheckDetector.is_square_attacked(board, row, c, enemy_color)
                for c in config['check_cols']
            )
            if not squares_safe:
                continue

            moves.append((row, config['king_dest_col']))

        return moves

    @staticmethod
    def is_castling_move(king, target_col):
        """Check if a king move is a castling move based on distance."""
        return abs(king.col - target_col) == 2

    @staticmethod
    def get_castling_side(king, target_col):
        """Determine which side the king is castling to."""
        if target_col > king.col:
            return KINGSIDE
        return QUEENSIDE

    @staticmethod
    def execute_castle(board, king, target_row, target_col):
        """
        Execute a castling move — move both king and rook.

        Args:
            board: The Board object.
            king: The King piece.
            target_row (int): Destination row for the king.
            target_col (int): Destination column for the king.

        Returns:
            tuple: (rook, rook_original_col, rook_dest_col) for undo purposes.
        """
        side = CastlingHandler.get_castling_side(king, target_col)
        config = CastlingHandler.CASTLING_CONFIG[side]

        rook = board.get_piece(target_row, config['rook_col'])

        # Move king
        board.set_piece(king.row, king.col, None)
        king.move_to(target_row, target_col)
        board.set_piece(target_row, target_col, king)

        # Move rook
        board.set_piece(target_row, config['rook_col'], None)
        rook.move_to(target_row, config['rook_dest_col'])
        board.set_piece(target_row, config['rook_dest_col'], rook)

        return rook, config['rook_col'], config['rook_dest_col']
