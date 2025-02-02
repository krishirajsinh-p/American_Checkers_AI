from .color import Color
from .piece import Piece
from .board import Board
from copy import deepcopy

class Minimax:
    def __init__(self, depth: int = 4) -> None:
        self.depth = depth

    def get_best_move(self, board: Board) -> Board:
        _, new_board = self.minimax(board, self.depth, float('-inf'), float('inf'), True)
        return new_board

    def minimax(self, board: Board, depth: int, alpha: float, beta: float, maximizing_player: bool) -> tuple[int, Board]:
        """Minimax algorithm with alpha-beta pruning to determine the best move for the AI."""
        if depth == 0 or board.winner() is not None:
            return board.evaluate(), board
        
        if maximizing_player:
            maxEval = float('-inf')
            best_move = None
            for move in self.get_all_moves(board, Piece.P1):
                evaluation, _ = self.minimax(move, depth - 1, alpha, beta, False)
                if evaluation > maxEval:
                    maxEval = evaluation
                    best_move = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return maxEval, best_move
        else:
            minEval = float('inf')
            best_move = None
            for move in self.get_all_moves(board, Piece.P2):
                evaluation, _ = self.minimax(move, depth - 1, alpha, beta, True)
                if evaluation < minEval:
                    minEval = evaluation
                    best_move = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return minEval, best_move

    def simulate_move(self, piece: Piece, move, board: Board, skip) -> Board:
        """Simulate a move on a temporary/copy board."""
        temp_board = deepcopy(board)
        temp_piece = temp_board.get_piece(piece.row, piece.col)
        temp_board.move_piece(temp_piece, move[0], move[1])
        if skip:
            temp_board.remove_pieces(skip)
        return temp_board

    def get_all_moves(self, board: Board, player: Color) -> list:
        """Get all the possible moves for a given player."""
        moves = []
        for piece in board.get_all_pieces(player):
            actions = board.get_actions(piece)
            for move, skip in actions.items():
                new_board = self.simulate_move(piece, move, board, skip)
                moves.append(new_board)
        return moves
