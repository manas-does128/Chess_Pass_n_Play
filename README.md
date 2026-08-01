# ♔ Chess Engine ♚

A fully-featured chess engine built in Python with modular architecture.

## Project Structure

```
chess/
│
├── main.py          # Entry point — terminal-based game loop
├── game.py          # Game controller & state management
├── board.py         # Board representation (8×8 grid)
├── move.py          # Move representation & algebraic notation
├── constants.py     # Game-wide constants
│
├── pieces/          # Chess piece implementations
│   ├── __init__.py
│   ├── piece.py     # Abstract base class for all pieces
│   ├── pawn.py      # Pawn (incl. double-advance, en passant awareness)
│   ├── rook.py      # Rook (sliding along ranks/files)
│   ├── knight.py    # Knight (L-shaped jumps)
│   ├── bishop.py    # Bishop (diagonal sliding)
│   ├── queen.py     # Queen (all 8 directions)
│   └── king.py      # King (single-square movement)
│
├── rules/           # Rule enforcement modules
│   ├── __init__.py
│   ├── validator.py # Central move validation coordinator
│   ├── check.py     # Check, checkmate & stalemate detection
│   ├── castle.py    # Castling validation & execution
│   ├── enpassant.py # En passant logic
│   └── promotion.py # Pawn promotion logic
│
├── assets/          # Piece images for GUI (optional)
│   ├── white/
│   └── black/
│
└── README.md
```

## Features

- **Complete chess rules**: All standard moves including castling, en passant, and pawn promotion
- **Check/Checkmate/Stalemate detection**: Full game-state analysis after every move
- **Move validation**: Prevents illegal moves (moving into check, pinned pieces, etc.)
- **Undo support**: Take back moves with full state restoration
- **Algebraic notation**: Moves displayed in standard algebraic notation
- **FEN support**: Load custom positions from FEN strings
- **Draw detection**: Fifty-move rule, threefold repetition, insufficient material
- **PGN output**: Export move list in PGN format

## How to Run

```bash
# From the project root (parent of chess/)
python -m chess.main
```

## How to Play

Once the game starts, enter moves using **coordinate notation**:

```
[1. White] Enter move: e2 e4
[1. Black] Enter move: e7 e5
[2. White] Enter move: g1 f3
```

### Available Commands

| Command   | Description                        |
|-----------|------------------------------------|
| `e2 e4`   | Move piece from e2 to e4          |
| `undo`    | Take back the last move            |
| `resign`  | Resign the game                    |
| `draw`    | Offer/accept a draw                |
| `history` | Show move history in PGN format    |
| `board`   | Redisplay the board                |
| `quit`    | Exit the program                   |

## Using as a Library

```python
from chess import Game

game = Game()

# Get a piece and its legal moves
piece = game.board.get_piece(6, 4)  # White pawn on e2
legal = game.get_legal_moves(piece)
print(legal)  # [(5, 4), (4, 4)]

# Make a move
move = game.make_move(piece, 4, 4)  # e2 → e4
print(move)  # "e4"

# Check game state
print(game.game_state)  # "ongoing"
```

## Architecture

- **Pieces** generate pseudo-legal moves (ignoring check constraints)
- **Rules** validate and filter moves to ensure full legality
- **Game** orchestrates turns, execution, undo, and state tracking
- **Board** manages the grid and provides piece-access utilities

## License

MIT
