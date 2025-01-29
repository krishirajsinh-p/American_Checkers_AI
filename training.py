import csv
import random
import os
from copy import deepcopy
from checkers_env.piece import Piece
from checkers_env.board import Board
from checkers_env.game import Game
from checkers_env.minimax import Minimax

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.3, epsilon_decay=0.995, q_table_file="./q_table.csv"):
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.epsilon_decay = epsilon_decay
        self.q_table_file = q_table_file
        self.q_table = self.load_q_table()

    def load_q_table(self):
        """Load Q-table from CSV file."""
        q_table = {}
        if os.path.exists(self.q_table_file):
            with open(self.q_table_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    state, action, value = row
                    if state not in q_table:
                        q_table[state] = {}
                    q_table[state][action] = float(value)
        return q_table

    def save_q_table(self):
        """Save Q-table to CSV file."""
        with open(self.q_table_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            for state, actions in self.q_table.items():
                for action, value in actions.items():
                    writer.writerow([state, action, value])

    def get_q_value(self, state, action):
        """Get Q-value for a given state-action pair."""
        state_str = state.encode()
        return self.q_table.get(state_str, {}).get(action, 0.0)

    def update_q_value(self, state, action, reward, next_state):
        """Update the Q-value using the Q-learning formula."""
        state_str = state.encode()
        next_state_str = next_state.encode()

        if state_str not in self.q_table:
            self.q_table[state_str] = {}
        
        max_next_q = max(self.q_table.get(next_state_str, {}).values(), default=0)
        current_q = self.get_q_value(state, action)
        new_q = (1 - self.alpha) * current_q + self.alpha * (reward + self.gamma * max_next_q)

        self.q_table[state_str][action] = new_q
        self.save_q_table()

    def choose_action(self, board: Board, player):
        """Choose an action using epsilon-greedy policy."""
        pieces = board.get_all_pieces(player)
        valid_moves = {p: board.get_actions(p) for p in pieces if board.get_actions(p)}
        if not valid_moves:
            return None, None

        if random.uniform(0, 1) < self.epsilon:
            piece = random.choice(list(valid_moves.keys()))
            move = random.choice(list(valid_moves[piece].keys()))
        else:
            best_q = -float("inf")
            piece, move = None, None
            for p, moves in valid_moves.items():
                for m in moves.keys():
                    q_value = self.get_q_value(board.encode(), str((p.row, p.col, m)))
                    if q_value > best_q:
                        best_q = q_value
                        piece, move = p, m
        return piece, move

    def train(self, episodes=1000):
        """Train the agent against the Minimax algorithm."""
        for episode in range(episodes):
            game = Game(None)
            minimax = Minimax()

            while game.winner() is None:
                board = deepcopy(game.get_board())
                
                if game.player == Piece.P1:
                    game.AI_action(minimax.get_best_move(game.get_board()))
                else:
                    piece, move = self.choose_action(game.get_board(), game.player)
                    if piece and move:
                        game.get_board().move_piece(piece, move[0], move[1])
                        self.update_q_value(board, str((piece.row, piece.col, move)), game.get_board().evaluate(), game.get_board())
                        game.change_player()

            self.epsilon = max(0.1, self.epsilon * self.epsilon_decay)
            print(f"Episode {episode + 1}/{episodes} completed.")
            
            if (episode + 1) % 100 == 0:
                self.save_q_table()
        
        print("Training completed.")

if __name__ == "__main__":
    agent = QLearningAgent()
    agent.train()
