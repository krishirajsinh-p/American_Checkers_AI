import os
import json
import random
from collections import defaultdict
from copy import deepcopy
from checkers_env.piece import Piece
from checkers_env.board import Board

class Q_Learning:
    """Class to implement the Q-learning algorithm."""
    Q_TABLE_FILE = "q_table.json"
    
    def __init__(self, alpha: float=0.15, gamma: float=0.95, epsilon: float=0.8, q_table_file: str=Q_TABLE_FILE) -> None:
        self.alpha = alpha  # Learning rate (increased for faster learning)
        self.gamma = gamma  # Discount factor (increased to value future rewards more)
        self.epsilon = epsilon  # Exploration rate
        self.q_table_file = q_table_file
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.load_q_table()
        self.move_count = 0

    def load_q_table(self) -> None:
        """Load Q-table from JSON file."""
        if os.path.exists(self.q_table_file):
            try:
                with open(self.q_table_file, mode='r') as file:
                    data = json.load(file)
                    # Convert back to nested defaultdict structure
                    for state, actions in data.items():
                        for action, value in actions.items():
                            self.q_table[state][action] = value
            except (json.JSONDecodeError, IOError):
                self.q_table = defaultdict(lambda: defaultdict(float))

    def save_q_table(self) -> None:
        """Save Q-table to JSON file."""
        with open(self.q_table_file, mode='w') as file:
            # Convert defaultdict to regular dict for JSON serialization
            data = {state: dict(actions) for state, actions in self.q_table.items()}
            json.dump(data, file, indent=2)

    def _encode_action(self, piece_row: int, piece_col: int, target_row: int, target_col: int) -> str:
        """Encode action as a consistent string."""
        return f"{piece_row},{piece_col},{target_row},{target_col}"

    def get_q_value(self, state: str, action: str) -> float:
        """Get Q-value for a given state-action pair."""
        return self.q_table[state].get(action, 0.0)

    def update_q_value(self, state: str, action: str, reward: float, next_state: str) -> None:
        """Update the Q-value using the Q-learning formula."""
        max_next_q_value = max(self.q_table[next_state].values(), default=0.0)
        q_value = self.get_q_value(state, action)
        new_q_value = q_value + self.alpha * (reward + (self.gamma * max_next_q_value) - q_value)
        self.q_table[state][action] = new_q_value
    
    def _calculate_move_reward(self, state_before: Board, state_after: Board, captured: bool) -> float:
        """Calculate immediate reward for a move (not just end-game)."""
        reward = 0.0
        
        # Reward for capturing opponent pieces
        if captured:
            reward += 2.0
        
        # Reward for piece positioning (advancing towards enemy)
        before_eval = state_before.evaluate()
        after_eval = state_after.evaluate()
        
        # Material advantage
        material_delta = after_eval - before_eval
        if material_delta > 0:
            reward += 0.5 + (material_delta * 0.1)
        elif material_delta < 0:
            reward -= 0.5  # Penalize losing pieces
        
        # Reward for getting closer to kingship (advancing)
        p1_pieces_before = state_before.get_all_pieces(Piece.P1)
        p1_pieces_after = state_after.get_all_pieces(Piece.P1)
        
        kings_promoted = 0
        for piece in p1_pieces_after:
            if piece.is_king and not any(p.row == piece.row and p.col == piece.col for p in p1_pieces_before):
                kings_promoted += 1
        
        reward += kings_promoted * 1.0  # Significant reward for promotion
        
        return reward
    
    def get_best_action(self, state: Board, is_training: bool = True) -> tuple[Board, str]:
        """Get the best action for a given state. Returns (new_board, action_taken)."""
        new_state = deepcopy(state)
        pieces = new_state.get_all_pieces(Piece.P1)
        valid_actions = {p: new_state.get_actions(p) for p in pieces if new_state.get_actions(p)}

        if not valid_actions:
            return new_state, ""

        state_str = state.encode()
        best_piece = None
        best_action = None
        best_skip = None
        action_str = None

        # Epsilon-greedy action selection
        if is_training and random.uniform(0, 1) < self.epsilon:
            # Explore: random action
            best_piece = random.choice(list(valid_actions.keys()))
            best_action, best_skip = random.choice(list(valid_actions[best_piece].items()))
            action_str = self._encode_action(best_piece.row, best_piece.col, best_action[0], best_action[1])
        else:
            # Exploit: best Q-value action
            best_q_value = -float("inf")
            for piece, actions in valid_actions.items():
                for action, skipped in actions.items():
                    action_key = self._encode_action(piece.row, piece.col, action[0], action[1])
                    q_value = self.get_q_value(state_str, action_key)
                    if q_value > best_q_value:
                        best_q_value = q_value
                        best_piece = piece
                        best_action = action
                        best_skip = skipped
                        action_str = action_key

        # Execute the action
        old_piece_count = new_state.p2_pawns + new_state.p2_kings
        new_state.move_piece(best_piece, best_action[0], best_action[1])
        captured = False
        if best_skip:
            new_state.remove_pieces(best_skip)
            captured = True
        
        # Calculate reward for this move
        if is_training:
            reward = self._calculate_move_reward(state, new_state, captured)
            next_state_str = new_state.encode()
            self.update_q_value(state_str, action_str, reward, next_state_str)

        self.move_count += 1
        return new_state, action_str
