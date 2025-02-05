from copy import deepcopy
from checkers_env.color import Color
from checkers_env.piece import Piece
from checkers_env.board import Board

class Minimax:
    """Class to implement the minimax algorithm with alpha-beta pruning."""
    def __init__(self, depth: int=4) -> None:
        self.depth = depth

    def get_best_action(self, board: Board) -> Board:
        """Get the best action for a given state."""
        _, new_board = self.minimax(board, self.depth, float('-inf'), float('inf'), True)
        return new_board

    def minimax(self, board: Board, depth: int, alpha: float, beta: float, maximizing_player: bool) -> tuple[int, Board]:
        """Minimax algorithm with alpha-beta pruning to determine the best outcome for the AI."""
        if depth == 0 or board.winner() is not None:
            return (-board.evaluate(), board)
        
        best_outcome = None
        if maximizing_player:
            maxEval = float('-inf')
            # player 2 is minimax algorithm (this will be used to train the model, Player 1 is the AI)
            for outcome in self.get_all_outcomes(board, Piece.P2):
                evaluation, _ = self.minimax(outcome, depth - 1, alpha, beta, False)
                if evaluation > maxEval:
                    maxEval = evaluation
                    best_outcome = outcome
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return (maxEval, best_outcome)
        else:
            minEval = float('inf')
            for outcome in self.get_all_outcomes(board, Piece.P1):
                evaluation, _ = self.minimax(outcome, depth - 1, alpha, beta, True)
                if evaluation < minEval:
                    minEval = evaluation
                    best_outcome = outcome
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return (minEval, best_outcome)

    def get_all_outcomes(self, board: Board, player: Color) -> list[Board]:
        """Get all the possible outcomes for a given player."""
        outcomes = []
        for piece in board.get_all_pieces(player):
            actions = board.get_actions(piece)
            for action, skip in actions.items():
                new_board = self.simulate_action(piece, action, board, skip)
                outcomes.append(new_board)
        return outcomes

    def simulate_action(self, piece: Piece, action: tuple[int, int], board: Board, skip: list[Piece]) -> Board:
        """Simulate an action on a temporary/copy board."""
        new_board = deepcopy(board)
        temp_piece = new_board.get_piece(piece.row, piece.col)
        new_board.move_piece(temp_piece, action[0], action[1])
        if skip:
            new_board.remove_pieces(skip)
        return new_board
