# player.py - Phase 1 computer opponent
#
# INTENTIONALLY DUMB. This is the foundation for the AI roadmap, not the
# AI itself. It contains ZERO chess knowledge:
#
#   - It does not know how any piece moves.
#   - It does not know what check, checkmate, or stalemate are.
#   - It does not know castling, en passant, or promotion rules.
#
# All of that already exists in rules/validator.py and friends. This
# class only asks MoveValidator for the fully legal moves available to
# its color and picks one at random. Later phases (capture preference,
# material evaluation, minimax, etc.) will replace the *selection*
# logic in choose_move() - the "ask the validator, get real Move
# objects back" architecture underneath is expected to stay the same.

import random

from rules.validator import MoveValidator
from rules.promotion import PromotionHandler


class AIPlayer:
    """A computer-controlled player for one color."""

    def __init__(self, color):
        self.color = color

    def choose_move(self, board):
        """
        Return one fully legal Move for self.color, chosen at random,
        or None if self.color has no legal moves at all (checkmate or
        stalemate - the caller is expected to detect that separately
        via MoveValidator.get_game_state, but this is a safe fallback).

        The Move objects returned here come straight from
        MoveValidator.get_legal_moves() - the same source the human
        player's clicks use - so every rule (check, castling, en
        passant, promotion) is already correctly encoded in them.
        """

        legal_moves = self._get_all_legal_moves(board)

        if not legal_moves:
            return None

        move = random.choice(legal_moves)

        # A human picks a promotion piece from the on-screen UI. The
        # computer has no UI to pause on, so it must decide right now.
        # Always promoting to a Queen is not "chess intelligence" - it's
        # just the minimum needed for the move to be complete and
        # executable by the existing pipeline.
        if move.is_promotion and move.promotion_choice is None:
            move.promotion_choice = PromotionHandler.get_piece_class(
                PromotionHandler.QUEEN
            )

        return move

    def _get_all_legal_moves(self, board):
        """Every legal Move for self.color, across every piece it owns."""

        all_moves = []

        for piece, row, col in board.get_pieces(self.color):

            legal_moves = MoveValidator.get_legal_moves(board, row, col)

            all_moves.extend(legal_moves.values())

        return all_moves
