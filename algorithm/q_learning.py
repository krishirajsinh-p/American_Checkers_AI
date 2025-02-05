import os
import csv
import random
from copy import deepcopy
from checkers_env.piece import Piece
from checkers_env.board import Board

class Q_Learning:
    """Class to implement the Q-learning algorithm."""
    Q_TABLE_FILE = "q_table.csv"
    
    def __init__(self, alpha: float=0.1, gamma: float=0.9, epsilon: float=0.1, q_table_file: str=Q_TABLE_FILE) -> None:
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table_file = q_table_file
        self.load_q_table()

    def load_q_table(self) -> None:
        """Load Q-table from CSV file."""
        self.q_table = {}
        if os.path.exists(self.q_table_file):
            with open(self.q_table_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    state, action, q_value = row
                    if state not in self.q_table:
                        self.q_table[state] = {}
                    self.q_table[state][eval(action)] = float(q_value)

    def save_q_table(self) -> None:
        """Save Q-table to CSV file."""
        with open(self.q_table_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            for state, actions in self.q_table.items():
                for action, value in actions.items():
                    writer.writerow([state, action, value])

    def get_q_value(self, state: Board, action: tuple[int, int, tuple[int, int]]) -> float:
        """Get Q-value for a given state-action pair."""
        return self.q_table.get(state.encode(), {}).get(action, 0.0)

    def update_q_value(self, state: Board, action: tuple[int, int, tuple[int, int]], reward: float, next_state: Board) -> None:
        """Update the Q-value using the Q-learning formula."""
        state_str = state.encode()
        if state_str not in self.q_table:
            self.q_table[state_str] = {}
        next_state_str = next_state.encode()
        
        max_next_q_value = max(self.q_table.get(next_state_str, {}).values(), default=0)
        q_value = self.get_q_value(state, action)
        new_q_value = q_value * (1 - self.alpha) + self.alpha * (reward + (self.gamma * max_next_q_value))
        
        self.q_table[state_str][action] = new_q_value
    
    # check this function
    def get_best_action(self, state: Board) -> Board:
        """Get the best action for a given state."""
        new_state = deepcopy(state)
        pieces = new_state.get_all_pieces(Piece.P1)
        valid_actions = {p: new_state.get_actions(p) for p in pieces if new_state.get_actions(p)}

        if random.uniform(0, 1) < self.epsilon:
            best_piece = random.choice(list(valid_actions.keys()))
            best_action, skip = random.choice(list(valid_actions[best_piece].items()))  
        else:
            best_q_value = -float("inf")
            for piece, actions in valid_actions.items():
                for action, skipped in actions.items():
                    q_value = self.get_q_value(new_state.encode(), str((piece.row, piece.col, action)))
                    if q_value > best_q_value:
                        best_q_value = q_value
                        best_piece, best_action, skip = piece, action, skipped

        new_state.move_piece(best_piece, best_action[0], best_action[1])
        if skip:
            new_state.remove_pieces(skip)

        self.update_q_value(state, str((best_piece.row, best_piece.col, best_action)), new_state.evaluate(), new_state)

        return new_state
