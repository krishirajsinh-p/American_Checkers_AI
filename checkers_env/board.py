import pygame
from .win_config import Win_Config
from .color import Color
from .piece import Piece

class Board:
    BOARD_SIZE = ROW = COL = Win_Config.NO_OF_ROWS
    BOX_COLOR_1 = Color.BEIGE
    BOX_COLOR_2 = Color.BROWN

    def __init__(self) -> None:
        self.p2_pawns = self.p1_pawns = 6
        self.p2_kings = self.p1_kings = 0
        self.board = []
        self.create_board()

    def create_board(self) -> None:
        """Initialize the board with pieces in starting positions."""
        for row in range(self.ROW):
            self.board.append([])
            for col in range(self.COL):
                if (row + col) % 2 == 1:
                    if row < self.BOARD_SIZE // 2 - 1:
                        self.board[row].append(Piece(row, col, Piece.P1))
                    elif row > self.BOARD_SIZE // 2:
                        self.board[row].append(Piece(row, col, Piece.P2))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def move_piece(self, piece: Piece, row: int, col: int) -> None:
        """Move a piece to a new position and handle promotion."""
        self.board[piece.row][piece.col], self.board[row][col] = 0, piece
        was_king = piece.is_king
        piece.move(row, col)
        is_king = piece.is_king
        if was_king != is_king:
            if piece.player == Piece.P1:
                self.p1_kings += 1
            else:
                self.p2_kings += 1

    def remove_pieces(self, pieces: list[Piece]) -> None:
        """Remove pieces from the board."""
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece.player == Piece.P1:
                if piece.is_king:
                    self.p1_kings -= 1
                else:
                    self.p1_pawns -= 1
            elif piece.player == Piece.P2:
                if piece.is_king:
                    self.p2_kings -= 1
                else:
                    self.p2_pawns -= 1

    def get_actions(self, piece: Piece) -> dict[tuple[int, int], list[Piece]]:
        """Returns all valid actions for a given piece."""
        actions = {}
        row = piece.row
        left = piece.col - 1
        right = piece.col + 1
        
        # For P1 and Kings, traverse down-right and down-left
        if piece.player == Piece.P1 or piece.is_king:
            actions.update(self._traverse_left(row + 1, min(row + 3, self.ROW), 1, piece.player, left))
            actions.update(self._traverse_right(row + 1, min(row + 3, self.ROW), 1, piece.player, right))
        
        # For P2 and Kings, traverse up-right and up-left
        if piece.player == Piece.P2 or piece.is_king:
            actions.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.player, left))
            actions.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.player, right))
        
        return actions

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        """Traverse to the left (diagonal) to check for valid actions."""
        actions = {}
        last = []
        
        # Traverse in the specified direction (up or down) until the stop condition
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            
            if current == 0:
                # If the square is empty, check if we can make a regular move or a jump
                if skipped and not last:
                    break
                elif skipped:
                    # If we have a skipped piece, record this as a valid jump
                    actions[(r, left)] = last + skipped
                else:
                    # Regular move to an empty space
                    actions[(r, left)] = last
                
                if last:
                    # After a jump, we recursively check the further diagonals
                    row = r + step
                    actions.update(self._traverse_left(row, max(row - 3, 0), step, color, left - 1, skipped=last))
                    actions.update(self._traverse_right(row, max(row - 3, 0), step, color, left + 1, skipped=last))
                break
            elif current.player == color:
                # If the piece belongs to the same player, stop traversing
                break
            else:
                # Otherwise, it's an opponent's piece, and we can "skip" over it for a jump
                last = [current]

            left -= 1
        
        return actions

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        """Traverse to the right (diagonal) to check for valid actions."""
        actions = {}
        last = []
        
        # Traverse in the specified direction (up or down) until the stop condition
        for r in range(start, stop, step):
            if right >= self.COL:
                break

            current = self.board[r][right]
            
            if current == 0:
                # If the square is empty, check if we can make a regular move or a jump
                if skipped and not last:
                    break
                elif skipped:
                    # If we have a skipped piece, record this as a valid jump
                    actions[(r, right)] = last + skipped
                else:
                    # Regular move to an empty space
                    actions[(r, right)] = last
                
                if last:
                    # After a jump, we recursively check the further diagonals
                    row = r + step
                    actions.update(self._traverse_left(row, min(row + 3, self.ROW), step, color, right - 1, skipped=last))
                    actions.update(self._traverse_right(row, min(row + 3, self.ROW), step, color, right + 1, skipped=last))
                break
            elif current.player == color:
                # If the piece belongs to the same player, stop traversing
                break
            else:
                # Otherwise, it's an opponent's piece, and we can "skip" over it for a jump
                last = [current]

            right += 1
        
        return actions

    def get_all_pieces(self, color: tuple[int, int, int]) -> list[Piece]:
        """Get all the pieces of a given color."""
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.player == color:
                    pieces.append(piece)
        return pieces

    def winner(self) -> tuple[int, int, int] | None:
        if self.p2_pawns + self.p2_kings <= 0:
            return Piece.P1
        elif self.p1_pawns + self.p1_kings <= 0:
            return Piece.P2
        p1_pieces = self.get_all_pieces(Piece.P1)
        p2_pieces = self.get_all_pieces(Piece.P2)
        p1actions = any(self.get_actions(piece) for piece in p1_pieces)
        p2actions = any(self.get_actions(piece) for piece in p2_pieces)
        if not p1actions and not p2actions:
            return Piece.P2 if self.evaluate() < 0 else Piece.P1
        if not p1actions:
            return Piece.P2
        if not p2actions:
            return Piece.P1
        return None

    def evaluate(self) -> float:
        """Evaluate the board state for the AI."""
        return (self.p1_pawns - self.p2_pawns) + ((self.p1_kings - self.p2_kings) * 1.5)

    def get_piece(self, row: int, col: int) -> Piece | int:
        """Get the piece at a given position."""
        return self.board[row][col]

    def draw(self, window: pygame.Surface) -> None:
        """Draw the board on the window."""
        window.fill(self.BOX_COLOR_1)
        for row in range(self.ROW):
            for col in range(row % 2, self.COL, 2):
                pygame.draw.rect(window, self.BOX_COLOR_2, (row * Win_Config.SQUARE_SIZE, col * Win_Config.SQUARE_SIZE, Win_Config.SQUARE_SIZE, Win_Config.SQUARE_SIZE))
        for row in self.board:
            for piece in row:
                if piece != 0:
                    piece.draw(window)

    def encode(self) -> str:
        """Encode the board state as a string."""
        return "".join([str(piece) for row in self.board for piece in row])

    def __str__(self) -> str:
        return "\n".join(["|".join([str(piece) for piece in row]) for row in self.board])

    def __repr__(self) -> str:
        return self.__str__()
