import pygame
from .win_config import Win_Config
from .color import Color

class Piece:
    PADDING = 30
    BORDER = 15
    RADIUS = (Win_Config.SQUARE_SIZE // 2) - PADDING
    P1 = Color.LIGHT_BLUE
    P2 = Color.LIGHT_RED
    PAWN_BORDER = Color.DARK_GREEN
    KING_BORDER = Color.DARK_RED

    def __init__(self, row: int, col: int, player: tuple[int, int, int]) -> None:
        self.row = row
        self.col = col
        self.player = player
        self.border_color = self.PAWN_BORDER
        self.is_king = False
        self.x, self.y = self.calculate_position()
        self.direction = 1 if self.player == self.P1 else -1

    def calculate_position(self) -> tuple[int, int]:
        """Calculate the pixel coordinates for the piece."""
        x = (Win_Config.SQUARE_SIZE * self.col) + (Win_Config.SQUARE_SIZE // 2)
        y = (Win_Config.SQUARE_SIZE * self.row) + (Win_Config.SQUARE_SIZE // 2)
        return x, y

    def move(self, row: int, col: int) -> None:
        """Move the piece to a new position and promote it if necessary."""
        self.row, self.col = row, col
        self.x, self.y = self.calculate_position()
        if row == 0 or row == Win_Config.NO_OF_ROWS - 1:
            self.promote_to_king()

    def promote_to_king(self) -> None:
        """Promote the piece to a king."""
        if not self.is_king:
            self.is_king = True
            self.border_color = self.KING_BORDER

    def draw(self, window: pygame.Surface) -> None:
        """Draw the piece on the board."""
        pygame.draw.circle(window, self.border_color, (self.x, self.y), Piece.RADIUS + Piece.BORDER)
        pygame.draw.circle(window, self.player, (self.x, self.y), Piece.RADIUS)

    def __str__(self) -> str:
        if self.player == self.P1:
            if self.is_king:
                return "B"
            else:
                return "b"
        elif self.player == self.P2:
            if self.is_king:
                return "R"
            else:
                return "r"
        return " "

    def __repr__(self) -> str:
        return self.__str__()
