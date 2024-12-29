class GameOverError(Exception):
    """Raised when the game ends due to collision."""
    pass
class InvalidMoveError(Exception):
    """Raised when the player tries to move in an invalid direction."""
    pass
