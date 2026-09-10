# rules package - Chess rule enforcement modules

from .validator import MoveValidator
from .check import CheckDetector
from .castle import CastlingHandler
from .enpassant import EnPassantHandler
from .promotion import PromotionHandler

__all__ = [
    'MoveValidator',
    'CheckDetector',
    'CastlingHandler',
    'EnPassantHandler',
    'PromotionHandler',
]
# rules package
#
# check.py has zero dependencies. validator.py is the coordinator that
# pulls in check/castle/enpassant/promotion - everything now matches the
# real Board/Piece API, so it's safe to import eagerly.

from .check import CheckDetector
from .validator import MoveValidator