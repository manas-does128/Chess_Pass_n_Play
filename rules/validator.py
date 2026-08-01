# validator.py - Central move validation

from ..constants import KING, PAWN, COLOR_WHITE, COLOR_BLACK
from .check import CheckDetector
from .castle import CastlingHandler
from .enpassant import EnPassantHandler
from .promotion import PromotionHandler


class MoveValidator:
    """
    Central move validator that coordinates all rule modules
    to determine if a move is fully legal.
    """

    def __init__(self):
        self.check_detector = CheckDetector()
        self.castling_handler = CastlingHandler()
        self.en_passant_handler = EnPassantHandler()
        self.promotion_handler = PromotionHandler()

    def get_legal_moves(self, board, piece):
        """
        Get all legal moves for a piece, accounting for:
        - Basic piece movement rules
        - Check constraints (can't move into or stay in check)
        - Castling
        - En passant

        Args:
            board: The Board object.
            piece: The piece to get moves for.

        Returns:
            list[tuple]: List of legal (row, col) destinations.
        """
        pseudo_legal = piece.get_possible_moves(board)
        legal_moves = []

        for move in pseudo_legal:
            if CheckDetector._is_move_legal(board, piece, move):
                legal_moves.append(move)

        # Add castling moves for king
        if piece.piece_type == KING:
            castle_moves = CastlingHandler.get_castling_moves(board, piece)
            legal_moves.extend(castle_moves)

        return legal_moves

    def is_legal_move(self, board, piece, target_row, target_col):
        """
        Check if a specific move is legal.

        Args:
            board: The Board object.
            piece: The piece to move.
            target_row (int): Destination row.
            target_col (int): Destination column.

        Returns:
            bool: True if the move is legal.
        """
        legal = self.get_legal_moves(board, piece)
        return (target_row, target_col) in legal

    def is_capture(self, board, target_row, target_col):
        """Check if the target square contains an enemy piece."""
        return board.get_piece(target_row, target_col) is not None

    def is_castling(self, piece, target_col):
        """Check if a king move is a castling attempt."""
        if piece.piece_type != KING:
            return False
        return CastlingHandler.is_castling_move(piece, target_col)

    def is_en_passant(self, board, piece, target_row, target_col):
        """Check if the move is an en passant capture."""
        return EnPassantHandler.is_en_passant_capture(board, piece, target_row, target_col)

    def is_promotion(self, piece, target_row):
        """Check if a pawn move results in promotion."""
        return PromotionHandler.is_promotion(piece, target_row)

    def get_game_state(self, board, color):
        """
        Evaluate the game state for the given color.

        Args:
            board: The Board object.
            color (str): The color whose turn it is.

        Returns:
            str: 'checkmate', 'stalemate', 'check', or 'ongoing'.
        """
        from ..constants import CHECKMATE, STALEMATE, CHECK, ONGOING

        if CheckDetector.is_checkmate(board, color):
            return CHECKMATE
        if CheckDetector.is_stalemate(board, color):
            return STALEMATE
        if CheckDetector.is_in_check(board, color):
            return CHECK
        return ONGOING
