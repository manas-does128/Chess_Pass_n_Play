# promotion.py - Pawn promotion logic

from ..constants import PAWN, QUEEN, ROOK, BISHOP, KNIGHT, COLOR_WHITE, PROMOTION_CHOICES
from ..pieces import Queen, Rook as RookPiece, Bishop as BishopPiece, Knight as KnightPiece


class PromotionHandler:
    """Handles pawn promotion detection and execution."""

    @staticmethod
    def is_promotion(piece, target_row):
        """
        Check if a move results in pawn promotion.

        Args:
            piece: The piece being moved.
            target_row (int): The destination row.

        Returns:
            bool: True if this pawn reaches the promotion rank.
        """
        if piece.piece_type != PAWN:
            return False

        if piece.color == COLOR_WHITE and target_row == 0:
            return True
        if piece.color != COLOR_WHITE and target_row == 7:
            return True

        return False

    @staticmethod
    def promote(board, pawn, target_row, target_col, choice=QUEEN):
        """
        Execute pawn promotion by replacing the pawn with the chosen piece.

        Args:
            board: The Board object.
            pawn: The pawn being promoted.
            target_row (int): The promotion row.
            target_col (int): The promotion column.
            choice (str): The piece type to promote to (default: queen).

        Returns:
            Piece: The newly created promoted piece.
        """
        if choice not in PROMOTION_CHOICES:
            choice = QUEEN

        # Create the promoted piece
        new_piece = PromotionHandler._create_piece(choice, pawn.color, target_row, target_col)

        # Place on board
        board.set_piece(target_row, target_col, new_piece)

        return new_piece

    @staticmethod
    def _create_piece(piece_type, color, row, col):
        """
        Factory method to create a new piece for promotion.

        Args:
            piece_type (str): Type of piece to create.
            color (str): Color of the piece.
            row (int): Row position.
            col (int): Column position.

        Returns:
            Piece: The new piece instance.
        """
        piece_map = {
            QUEEN: Queen,
            ROOK: RookPiece,
            BISHOP: BishopPiece,
            KNIGHT: KnightPiece,
        }
        piece_class = piece_map.get(piece_type, Queen)
        new_piece = piece_class(color, row, col)
        new_piece.has_moved = True
        return new_piece

    @staticmethod
    def get_promotion_choices():
        """Return the list of valid promotion piece types."""
        return list(PROMOTION_CHOICES)
