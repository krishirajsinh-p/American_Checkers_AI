import pygame
from .win_config import Win_Config
from .color import Color
from .piece import Piece
from .board import Board

class Game:
    def __init__(self, window: pygame.Surface) -> None:
        self.board = Board()
        # Player 1 starts the game
        self.current_player = Piece.P1
        self.selected_piece = None
        self.valid_actions = {}
        self.window = window
        self.moves = 0
    
    def change_player(self) -> None:
        """Change the turn of the game."""
        self.moves += 1
        self.selected_piece = None
        self.valid_actions = {}
        if self.current_player == Piece.P1:
            self.current_player = Piece.P2
        else:
            self.current_player = Piece.P1

    def select_pos(self, row: int, col: int) -> None:
        """Select a piece on the board."""
        if not self.selected_piece:
            piece = self.board.get_piece(row, col)
            if piece != 0 and piece.player == self.current_player:
                self.selected_piece = piece
                self.valid_actions = self.board.get_actions(piece)
        else:
            result = self._move(row, col)
            if not result:
                self.selected_piece = None
                self.valid_actions = {}
                self.select_pos(row, col)
    
    def _move(self, row: int, col: int) -> bool:
        """Move a piece on the board."""
        piece = self.board.get_piece(row, col)
        if piece == 0 and (row, col) in self.valid_actions:
            self.board.move_piece(self.selected_piece, row, col)
            skipped = self.valid_actions[(row, col)]
            if skipped:
                self.board.remove_pieces(skipped)
            self.change_player()
            return True
        else:
            return False

    def AI_move(self, board: Board) -> None:
        """Mimics the AI move."""
        self.board = board
        self.change_player()

    def update(self) -> None:
        """Update the game state and refresh the window."""
        self.board.draw(self.window)
        self.draw_valid_actions(self.valid_actions, self.window)
        pygame.display.update()

    def winner(self) -> Color | None:
        """Return the winner of the game."""
        return self.board.winner()
    
    def get_board(self) -> Board:
        """Return the current board state."""
        return self.board
    
    def mouse_pos_to_board_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        """Get the row and column of the clicked square."""
        x, y = pos
        col = x // Win_Config.SQUARE_SIZE
        row = y // Win_Config.SQUARE_SIZE
        return (row, col)

    def draw_valid_actions(self, actions: dict[tuple[int, int], list[Piece]], window: pygame.Surface) -> None:
        """Draw valid actions on the board."""
        for action in actions:
            row, col = action
            pygame.draw.circle(window, Color.DARK_ORANGE, (col * Win_Config.SQUARE_SIZE + Win_Config.SQUARE_SIZE // 2, row * Win_Config.SQUARE_SIZE + Win_Config.SQUARE_SIZE // 2), 15)

    def __str__(self) -> str:
        return str(self.board) + f"\nPlayer: {"P1" if self.player == Piece.P1 else "P2"}\nMoves: {self.moves}\nWinner: {"P1" if self.winner() == Piece.P1 else 'P2' if self.winner() == Piece.P2 else 'None'}"
    
    def __repr__(self) -> str:
        self.__str__()
