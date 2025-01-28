import pygame
from .win_config import Win_Config
from .color import Color
from .piece import Piece

    # def get_index(self, row, col):
    #     return row * WinConfig.BOARD_SIZE + col

    # def get_all_pieces(self, color):
    #     pieces = []
    #     for piece in self.board:
    #         if piece != 0 and piece.color == color:
    #             pieces.append(piece)

# TODO: Implement 2D array to 1D array conversion
# TODO: Implement array exapansion and contraction

class Board:
    BOARD_SIZE = ROW = COL = Win_Config.NO_OF_ROWS
    BOX_COLOR_1 = Color.BEIGE
    BOX_COLOR_2 = Color.BROWN

    def __init__(self):
        self.black_pawns = self.white_pawns = 12
        self.black_kings = self.white_kings = 0
        self.board = []
        self.create_board()

    def create_board(self):
        for row in range(self.ROW):
            self.board.append([])
            for col in range(self.COL):
                if col % 2 == ((row +  1) % 2):
                    if row < self.BOARD_SIZE // 2 - 1:
                        self.board[row].append(Piece(row, col, Piece.P1_COLOR))
                    elif row > self.BOARD_SIZE // 2:
                        self.board[row].append(Piece(row, col, Piece.P2_COLOR))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        was_king = piece.is_king
        piece.move(row, col)
        is_king = piece.is_king
        if was_king != is_king:
            if piece.color == Piece.P1_COLOR:
                self.white_kings += 1
            else:
                self.black_kings += 1

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == Piece.P1_COLOR:
                    if piece.is_king:
                        self.white_kings -= 1
                    else:
                        self.white_pawns -= 1
                elif piece.color == Piece.P2_COLOR:
                    if piece.is_king:
                        self.black_kings -= 1
                    else:
                        self.black_pawns -= 1

    def get_valid_moves(self, piece):
        moves = {}
        row = piece.row
        left = piece.col - 1
        right = piece.col + 1
        if piece.color == Piece.P1_COLOR or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, self.ROW), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, self.ROW), 1, piece.color, right))
        if piece.color == Piece.P2_COLOR or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, self.ROW)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= self.COL:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, self.ROW)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def get_piece(self, row, col):
        return self.board[row][col]
    
    def winner(self):
        if self.black_pawns + self.black_kings <= 0:
            return Piece.P1_COLOR
        elif self.white_pawns + self.white_kings <= 0:
            return Piece.P2_COLOR
        return None

    def evaluate(self):
        return (self.white_pawns - self.black_pawns) + ((self.white_kings - self.black_kings) * 0.5)
    
    def _draw_squares(self, window):
        window.fill(self.BOX_COLOR_1)
        for row in range(self.ROW):
            for col in range(row % 2, self.COL, 2):
                pygame.draw.rect(window, self.BOX_COLOR_2, (row * Win_Config.SQUARE_SIZE, col * Win_Config.SQUARE_SIZE, Win_Config.SQUARE_SIZE, Win_Config.SQUARE_SIZE))

    def draw(self, window):
        self._draw_squares(window)
        for row in range(self.ROW):
            for col in range(self.COL):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)

    def __str__(self):
        board_string = ""
        for row in range(self.ROW):
            board_string += "|" + "|".join([str(self.board[row][col]) for col in range(self.COL)]) + "|\n"
        return board_string

    def __repr__(self):
        return self.__str__()
