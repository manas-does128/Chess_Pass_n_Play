import pygame

from board import Board
from constants import *
from assets import IMAGES
from rules.validator import MoveValidator
from rules.check import CheckDetector
from rules.promotion import PromotionHandler
from sound_manager import SoundManager
from ai.player import AIPlayer


class Game:

    def __init__(self, vs_computer=False, computer_color="black"):

        # V1 behavior (Human vs Human) is the default - Game() with no
        # arguments is unchanged from before. Passing vs_computer=True
        # is the only way any new behavior is triggered.
        self.vs_computer = vs_computer
        self.computer_color = computer_color
        self.ai_player = AIPlayer(computer_color) if vs_computer else None

        self.board = Board()

        self.turn = "white"

        self.selected = None

        # {(end_row, end_col): Move} for whatever piece is selected.
        self.legal_moves = {}

        # Set to the Move waiting on a promotion choice, else None. While
        # this is set, board clicks are routed to the promotion UI
        # instead of normal piece selection.
        self.pending_promotion = None

        # Game-over state.
        self.game_over = False
        self.game_over_reason = None   # "checkmate" or "stalemate"
        self.winner = None             # "white" / "black" / None (draw)

        self.sounds = SoundManager()

    ##################################################
    # DRAW
    ##################################################

    def draw(self, screen):

        self.draw_board(screen)

        self.highlight_selection(screen)

        self.highlight_moves(screen)

        self.board.draw(screen)

        self.highlight_check(screen)

        if self.pending_promotion is not None:

            self.draw_promotion_ui(screen)

        elif self.game_over:

            self.draw_game_over(screen)

    ##################################################
    # BOARD
    ##################################################

    def draw_board(self, screen):

        for row in range(ROWS):

            for col in range(COLS):

                color = LIGHT if (row + col) % 2 == 0 else DARK

                pygame.draw.rect(

                    screen,

                    color,

                    (

                        col * SQUARE_SIZE,

                        row * SQUARE_SIZE,

                        SQUARE_SIZE,

                        SQUARE_SIZE

                    )

                )

    ##################################################
    # HIGHLIGHTS
    ##################################################

    def highlight_selection(self, screen):

        if self.selected is None:
            return

        row, col = self.selected

        pygame.draw.rect(

            screen,

            SELECTED,

            (

                col * SQUARE_SIZE,

                row * SQUARE_SIZE,

                SQUARE_SIZE,

                SQUARE_SIZE

            ),

            4

        )

    def highlight_moves(self, screen):

        for (row, col), move in self.legal_moves.items():

            center = (

                col * SQUARE_SIZE + SQUARE_SIZE // 2,

                row * SQUARE_SIZE + SQUARE_SIZE // 2

            )

            if move.is_capture() or move.is_en_passant:

                pygame.draw.circle(screen, CAPTURE, center, SQUARE_SIZE // 2 - 6, 4)

            else:

                pygame.draw.circle(screen, MOVE, center, 10)

    def highlight_check(self, screen):

        for color in ("white", "black"):

            if not CheckDetector.is_in_check(self.board, color):
                continue

            king_pos = self.board.get_king(color)

            if king_pos is None:
                continue

            row, col = king_pos

            pygame.draw.rect(

                screen,

                CHECK_COLOR,

                (

                    col * SQUARE_SIZE,

                    row * SQUARE_SIZE,

                    SQUARE_SIZE,

                    SQUARE_SIZE

                ),

                4

            )

    ##################################################
    # PROMOTION UI
    ##################################################

    def _promotion_button_rects(self):

        size = 100
        gap = 20
        count = 4

        total_width = count * size + (count - 1) * gap
        start_x = (WIDTH - total_width) // 2
        y = (HEIGHT - size) // 2

        return [
            pygame.Rect(start_x + i * (size + gap), y, size, size)
            for i in range(count)
        ]

    def draw_promotion_ui(self, screen):

        move = self.pending_promotion
        color = move.piece.color

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((*OVERLAY_COLOR, OVERLAY_ALPHA))
        screen.blit(overlay, (0, 0))

        buttons = self._promotion_button_rects()
        choices = PromotionHandler.get_promotion_choices()

        font = pygame.font.Font(None, 28)
        label = font.render("Choose promotion", True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=(WIDTH // 2, buttons[0].top - 30)))

        for choice, rect in zip(choices, buttons):

            pygame.draw.rect(screen, PROMOTION_BUTTON_BG, rect, border_radius=8)
            pygame.draw.rect(screen, PANEL_BORDER, rect, 2, border_radius=8)

            image = IMAGES.get(f"{color}_{choice}")

            if image is not None:
                screen.blit(image, image.get_rect(center=rect.center))

    def _hit_test_promotion_buttons(self, pos):

        choices = PromotionHandler.get_promotion_choices()

        for choice, rect in zip(choices, self._promotion_button_rects()):

            if rect.collidepoint(pos):
                return choice

        return None

    ##################################################
    # GAME OVER UI
    ##################################################

    def _game_over_panel_rect(self):

        panel = pygame.Rect(0, 0, 420, 260)
        panel.center = (WIDTH // 2, HEIGHT // 2)
        return panel

    def _restart_button_rect(self):

        panel = self._game_over_panel_rect()
        button = pygame.Rect(0, 0, 180, 50)
        button.center = (panel.centerx, panel.bottom - 55)
        return button

    def draw_game_over(self, screen):

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((*OVERLAY_COLOR, OVERLAY_ALPHA))
        screen.blit(overlay, (0, 0))

        panel = self._game_over_panel_rect()

        pygame.draw.rect(screen, PANEL_COLOR, panel, border_radius=12)
        pygame.draw.rect(screen, PANEL_BORDER, panel, 3, border_radius=12)

        title_font = pygame.font.Font(None, 48)
        sub_font = pygame.font.Font(None, 36)

        if self.game_over_reason == "checkmate":
            title = "CHECKMATE"
            subtitle = f"{self.winner.upper()} WINS"
        else:
            title = "STALEMATE"
            subtitle = "DRAW"

        title_surface = title_font.render(title, True, (20, 20, 20))
        subtitle_surface = sub_font.render(subtitle, True, (20, 20, 20))

        screen.blit(title_surface, title_surface.get_rect(center=(panel.centerx, panel.top + 70)))
        screen.blit(subtitle_surface, subtitle_surface.get_rect(center=(panel.centerx, panel.top + 120)))

        button = self._restart_button_rect()

        pygame.draw.rect(screen, BUTTON_COLOR, button, border_radius=8)
        pygame.draw.rect(screen, BUTTON_BORDER, button, 2, border_radius=8)

        button_font = pygame.font.Font(None, 32)
        button_label = button_font.render("RESTART", True, BUTTON_TEXT_COLOR)
        screen.blit(button_label, button_label.get_rect(center=button.center))

    def _hit_test_restart_button(self, pos):

        return self._restart_button_rect().collidepoint(pos)

    ##################################################
    # INPUT
    ##################################################

    def handle_click(self, pos):
        """Single entry point for mouse clicks - called from main.py."""

        if self.game_over:
            self.handle_game_over_click(pos)
            return

        if self.pending_promotion is not None:
            self.handle_promotion_click(pos)
            return

        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE

        if 0 <= row < ROWS and 0 <= col < COLS:
            self.select(row, col)

    def handle_promotion_click(self, pos):

        choice = self._hit_test_promotion_buttons(pos)

        if choice is None:
            return

        move = self.pending_promotion
        move.promotion_choice = PromotionHandler.get_piece_class(choice)

        self.pending_promotion = None

        self._apply_and_finish(move)

    def handle_game_over_click(self, pos):

        if self._hit_test_restart_button(pos):
            self.restart()

    def select(self, row, col):

        piece = self.board.get_piece(row, col)

        # Nothing selected yet
        if self.selected is None:

            if piece is None:
                return

            if piece.color != self.turn:
                return

            self.selected = (row, col)

            self.legal_moves = MoveValidator.get_legal_moves(self.board, row, col)

            return

        # Already selected

        # Clicking own piece changes selection
        if piece and piece.color == self.turn:

            self.selected = (row, col)

            self.legal_moves = MoveValidator.get_legal_moves(self.board, row, col)

            return

        # Move if legal
        if (row, col) in self.legal_moves:

            move = self.legal_moves[(row, col)]

            self.selected = None
            self.legal_moves = {}

            self._finalize_move(move)

            return

        # Clicked something that isn't a legal destination for the
        # selected piece.
        self.sounds.play("illegal")

        self.selected = None
        self.legal_moves = {}

    ##################################################
    # MOVE EXECUTION
    ##################################################

    def _finalize_move(self, move):
        """
        Apply a chosen move - unless it's a promotion with no choice
        made yet, in which case pause and wait for the promotion UI.
        """

        if move.is_promotion and move.promotion_choice is None:

            self.pending_promotion = move

            return

        self._apply_and_finish(move)

    def _apply_and_finish(self, move):

        mover = self.turn

        self.board.apply_move(move)

        opponent = "black" if mover == "white" else "white"

        state = MoveValidator.get_game_state(self.board, opponent)

        self._play_move_sound(move, state)

        self.turn = opponent

        if state == "checkmate":

            self.game_over = True
            self.game_over_reason = "checkmate"
            self.winner = mover

        elif state == "stalemate":

            self.game_over = True
            self.game_over_reason = "stalemate"
            self.winner = None

        self._maybe_play_computer_move()

    def _maybe_play_computer_move(self):
        """
        If a computer opponent is enabled and it is now that color's
        turn, ask AIPlayer for a legal move and run it through the
        exact same execution pipeline (_apply_and_finish) a human move
        uses. No board manipulation happens here - only existing V1
        machinery is called.
        """

        if not self.vs_computer or self.game_over:
            return

        if self.turn != self.ai_player.color:
            return

        move = self.ai_player.choose_move(self.board)

        # Should already be caught as checkmate/stalemate above, but
        # guard defensively rather than assume.
        if move is None:
            return

        self._apply_and_finish(move)

    def _play_move_sound(self, move, state):

        if state in ("checkmate", "stalemate"):
            self.sounds.play("game_over")
        elif state == "check":
            self.sounds.play("check")
        elif move.is_castle:
            self.sounds.play("castle")
        elif move.is_promotion:
            self.sounds.play("promotion")
        elif move.is_capture():
            self.sounds.play("capture")
        else:
            self.sounds.play("move")

    ##################################################
    # RESTART
    ##################################################

    def restart(self):

        self.board = Board()
        self.turn = "white"
        self.selected = None
        self.legal_moves = {}
        self.pending_promotion = None
        self.game_over = False
        self.game_over_reason = None
        self.winner = None