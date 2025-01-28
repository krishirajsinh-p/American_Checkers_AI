import pygame
from .win_config import Win_Config
from .color import Color

# TODO: Implement Direction

class Piece:
    PADDING = 30
    BORDER = 15
    RADIUS = (Win_Config.SQUARE_SIZE // 2) - PADDING
    P1_COLOR = Color.LIGHT_BLUE
    P2_COLOR = Color.LIGHT_RED
    PAWN_BORDER_COLOR = Color.DARK_GREEN
    KING_BORDER_COLOR = Color.DARK_RED

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.border_color = self.PAWN_BORDER_COLOR
        self.is_king = False
        self.calc_xy(row, col)

    def calc_xy(self, row, col):
        self.x = (Win_Config.SQUARE_SIZE * col) + (Win_Config.SQUARE_SIZE // 2)
        self.y = (Win_Config.SQUARE_SIZE * row) + (Win_Config.SQUARE_SIZE // 2)

    def move(self, row, col):
        self.row, self.col = row, col
        self.calc_pos(row, col)
        if row == 0 or row == Win_Config.ROW - 1:
            self._make_king()

    def _make_king(self):
        if not self.is_king:
            self.is_king = True
            self.border_color = self.KING_BORDER_COLOR

    def draw(self, window):
        pygame.draw.circle(window, self.border_color, (self.x, self.y), Piece.RADIUS + Piece.BORDER)
        pygame.draw.circle(window, self.color, (self.x, self.y), Piece.RADIUS)

    def __str__(self):
        if self.color == self.P1_COLOR:
            if self.is_king:
                return "W"
            else:
                return "w"
        elif self.color == self.P2_COLOR:
            if self.is_king:
                return "B"
            else:
                return "b"
        return "X"

    def __repr__(self):
        return self.__str__()
