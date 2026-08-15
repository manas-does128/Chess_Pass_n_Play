# promotion.py - Pawn promotion logic
#
# Rewritten against the project's real Piece API: pieces are constructed
# as PieceClass(color) only (no row/col args), and there is no
# piece_type attribute - isinstance() against Pawn is used instead.

from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight


class PromotionHandler:
    """Handles pawn promotion detection and the piece-choice mapping."""

    QUEEN = "queen"
    ROOK = "rook"
    BISHOP = "bishop"
    KNIGHT = "knight"

    CHOICES = [QUEEN, ROOK, BISHOP, KNIGHT]

    PIECE_CLASSES = {
        QUEEN: Queen,
        ROOK: Rook,
        BISHOP: Bishop,
        KNIGHT: Knight,
    }

    @staticmethod
    def is_promotion_square(piece, end_row):
        """True if moving `piece` to end_row reaches the final rank."""

        if not isinstance(piece, Pawn):
            return False

        if piece.color == "white" and end_row == 0:
            return True

        if piece.color == "black" and end_row == 7:
            return True

        return False

    @staticmethod
    def get_piece_class(choice):
        """Map a promotion choice string to its Piece subclass."""

        return PromotionHandler.PIECE_CLASSES.get(choice, Queen)

    @staticmethod
    def get_promotion_choices():
        return list(PromotionHandler.CHOICES)