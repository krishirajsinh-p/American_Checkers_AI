from checkers_env.piece import Piece
from checkers_env.game import Game
from algorithm.minimax import Minimax
from algorithm.q_learning import Q_Learning

def train(episodes=5000) -> None:
    """Trains the Q Learning against the Minimax algorithm."""
    # Improved epsilon decay: use inverse decay instead of exponential
    epsilon_start = 0.8
    epsilon_end = 0.05
    
    win_counts = {"Q-Learning": 0, "Minimax": 0, "Draw": 0}
    move_counts = []
    
    for episode in range(episodes):
        # Inverse decay: epsilon decreases more gradually
        epsilon = epsilon_end + (epsilon_start - epsilon_end) * (1 - episode / episodes)
        epsilon = max(epsilon_end, epsilon)
        
        game = Game(None)
        # Increase depth for stronger minimax opponent to better train the Q-learning agent
        minimax = Minimax(depth=2)
        q_learning = Q_Learning(alpha=0.15, gamma=0.95, epsilon=epsilon)

        while game.winner() is None:
            if game.current_player == Piece.P2:
                new_board = minimax.get_best_action(game.get_board())
                game.AI_move(new_board)
            else:
                new_board, action = q_learning.get_best_action(game.get_board(), is_training=True)
                game.AI_move(new_board)

        winner = game.winner()
        moves = game.moves
        move_counts.append(moves)
        
        # Track winner
        if winner == Piece.P1:
            winner_str = "Q-Learning"
            win_counts["Q-Learning"] += 1
        elif winner == Piece.P2:
            winner_str = "Minimax"
            win_counts["Minimax"] += 1
        else:
            winner_str = "Draw"
            win_counts["Draw"] += 1

        # Print progress with statistics
        if (episode + 1) % 50 == 0:
            avg_moves = sum(move_counts[-50:]) / 50 if len(move_counts) >= 50 else sum(move_counts) / len(move_counts)
            win_rate = win_counts["Q-Learning"] / (episode + 1) * 100
            print(f"Episode {episode + 1}/{episodes} | Winner: {winner_str} | Moves: {moves} | "
                  f"Avg Moves (last 50): {avg_moves:.1f} | Q-Learning Win Rate: {win_rate:.1f}% | "
                  f"Epsilon: {epsilon:.3f}")
            
            # Save progress every 50 episodes
            q_learning.save_q_table()
            print(f"Saved Q-table checkpoint at episode {episode + 1}.")
        elif (episode + 1) % 10 == 0:
            print(f"Episode {episode + 1}/{episodes} | Winner: {winner_str} | Moves: {moves}")
    
    # Print final statistics
    print("\n" + "="*60)
    print("Training completed!")
    print(f"Q-Learning wins: {win_counts['Q-Learning']} ({win_counts['Q-Learning']/episodes*100:.1f}%)")
    print(f"Minimax wins: {win_counts['Minimax']} ({win_counts['Minimax']/episodes*100:.1f}%)")
    print(f"Draws: {win_counts['Draw']} ({win_counts['Draw']/episodes*100:.1f}%)")
    print(f"Average game length: {sum(move_counts)/len(move_counts):.1f} moves")
    print("="*60)

if __name__ == "__main__":
    train(episodes=5000)
