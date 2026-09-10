# validator.py - Central move validation
#
# The single entry point the rest of the game should call. Combines:
#   - CheckDetector    (pseudo-legal moves filtered for king safety)
#   - CastlingHandler  (adds castling as extra king moves)
#   - EnPassantHandler (adds en passant as an extra pawn move)
#   - promotion tagging (flags pawn moves that reach the final rank)
# into one place, and answers "is the game over" (checkmate/stalemate).

from pieces.pawn import Pawn
from pieces.king import King

from .check import CheckDetector
from .castle import CastlingHandler
from .enpassant import EnPassantHandler
from .promotion import PromotionHandler
from move import Move


class MoveValidator:
    """Central move validator - the only rule module game.py talks to."""

    @staticmethod
    def get_legal_moves(board, row, col):
        """
        Return every fully legal move for the piece at (row, col) as a
        dict: {(end_row, end_col): Move}.

        Plain moves/captures come from CheckDetector (already filtered
        for king safety). Castling and en passant are added on top when
        applicable. Pawn moves that land on the final rank are flagged
        is_promotion=True (promotion_choice stays None until the player
        picks one).
        """

        piece = board.get_piece(row, col)

        if piece is None:
            return {}

        moves = {}

        for end_row, end_col in CheckDetector.get_legal_moves(board, row, col):

            captured = board.get_piece(end_row, end_col)

            is_promo = PromotionHandler.is_promotion_square(piece, end_row)

            moves[(end_row, end_col)] = Move(
                (row, col),
                (end_row, end_col),
                piece=piece,
                captured_piece=captured,
                is_promotion=is_promo,
            )

        if isinstance(piece, Pawn):

            ep_move = EnPassantHandler.get_en_passant_move(board, row, col)

            if ep_move is not None and EnPassantHandler.is_safe(board, ep_move, piece.color):

                moves[(ep_move.end_row, ep_move.end_col)] = ep_move

        if isinstance(piece, King):

            for castle_move in CastlingHandler.get_castling_moves(board, piece.color):

                moves[(castle_move.end_row, castle_move.end_col)] = castle_move

        return moves

    @staticmethod
    def has_any_legal_move(board, color):
        """True if `color` has at least one fully legal move anywhere."""

        for piece, row, col in board.get_pieces(color):

            if MoveValidator.get_legal_moves(board, row, col):
                return True

        return False

    @staticmethod
    def get_game_state(board, color):
        """
        Evaluate the game state for `color` (the side about to move).

        Returns one of: "checkmate", "stalemate", "check", "ongoing".
        """

        in_check = CheckDetector.is_in_check(board, color)
        has_moves = MoveValidator.has_any_legal_move(board, color)

        if in_check and not has_moves:
            return "checkmate"

        if not in_check and not has_moves:
            return "stalemate"

        if in_check:
            return "check"

        return "ongoing"