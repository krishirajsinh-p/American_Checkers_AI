from checkers_env.piece import Piece
from checkers_env.game import Game
from algorithm.minimax import Minimax
from algorithm.q_learning import Q_Learning

def train(episodes=1000) -> None:
    """Trains the Q Learning against the Minimax algorithm."""
    epsilon = 0.8
    epsilon_decay = 0.995
    minimum_epsilon = 0.2
    for episode in range(episodes):
        epsilon = max(minimum_epsilon, epsilon * epsilon_decay)
        game = Game(None)
        minimax = Minimax(depth=2)
        q_learning = Q_Learning(epsilon=epsilon)

        while game.winner() is None:
            if game.current_player == Piece.P2:
                game.AI_move(minimax.get_best_action(game.get_board()))
            else:
                game.AI_move(q_learning.get_best_action(game.get_board()))

        winner, moves, reward = game.winner(), game.moves, game.board.evaluate()

        winner = "AI" if winner == Piece.P1 else ("Minimax" if winner == Piece.P2 else "Draw")
        print(f"Episode {episode + 1}/{episodes} completed, winner is {winner}, played {moves} moves, cummulative reward is {reward}.")
        
        if (episode + 1) % 50 == 0:
            q_learning.save_q_table()
            print(f"Saved Q-table until {episode + 1} episode.")
    
    print("Training completed.")

if __name__ == "__main__":
    train()
