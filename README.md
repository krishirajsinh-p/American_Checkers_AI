# Checkers AI

An interactive American Checkers game featuring AI opponents powered by **Minimax** with alpha-beta pruning and **Q-Learning** reinforcement learning algorithms. Play against intelligent agents!

## Features

- **Two AI Algorithms**:
  - **Minimax Algorithm**: Uses adversarial search with alpha-beta pruning for optimal strategic gameplay
  - **Q-Learning Agent**: Reinforcement learning agent trained through self-play against Minimax
- **Interactive Gameplay**: Play as against either AI opponent
- **Training Mode**: Train the Q-Learning agent against the Minimax algorithm
- **Visual Interface**: Built with Pygame for smooth graphics and intuitive controls
- **Game Mechanics**: Full implementation of American Checkers rules including:
  - Regular moves and captures
  - Multi-jump sequences
  - King promotion
  - Win/draw detection

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/krishirajsinh-p/Checkers-AI.git
   cd Checkers-AI
   ```

2. **Execute run.sh script**:
    ```bash
    ./run.sh
    ```

    Then select your opponent:
    - `1` - Play against Minimax algorithm
    - `2` - Play against Q-Learning agent

## 🎮 Game Controls

- Mouse Click: Select and move pieces
- ESC or Close Window: Exit game
- Valid Moves: Orange circles indicate possible moves for selected piece

## 📏 Game Rules

### American Checkers (6x6 Board)

1. **Setup**: 6 pieces per player on a 6x6 board
2. **Movement**: 
   - Pawns move diagonally forward
   - Kings move diagonally in all directions
3. **Capturing**:
   - Jump over opponent pieces to capture
   - Multiple jumps allowed in single turn
   - Captures are mandatory if available
4. **King Promotion**: Pieces reaching the opposite end become kings
5. **Winning**: 
   - Capture all opponent pieces, or
   - Block all opponent moves
6. **Draw**: Game ends in draw if no progress after extended moves

## 🎨 Board Configuration

- **Board Size**: 6x6 grid
- **Window**: 800x800 pixels
- **Colors**:
  - Pawn Pieces: Blue and Red with Green border
  - King Pieces: with Dark Red border
  - Board: Beige and Brown squares
  - Valid moves: Orange indicators

## 📁 Project Structure

```
American_Checkers_AI/
├── algorithm/
│   ├── __init__.py
│   ├── minimax.py          # Minimax with alpha-beta pruning
│   └── q_learning.py       # Q-Learning reinforcement learning
├── checkers_env/
│   ├── __init__.py
│   ├── board.py            # Game board logic
│   ├── color.py            # Color constants
│   ├── game.py             # Game state management
│   ├── piece.py            # Piece representation and logic
│   └── win_config.py       # Window and game configuration
├── play_against_minimax.py # Play against Minimax agent
├── play_against_qlearning.py # Play against Q-Learning agent
├── training.py             # Train Q-Learning agent
├── requirements.txt        # Python dependencies
├── run.sh                  # Quick start script
└── q_table.json           # Saved Q-Learning model (generated after training)
```

## 🧠 Algorithms

### Minimax with Alpha-Beta Pruning

The Minimax algorithm explores the game tree to find the optimal move by:
- Evaluating board positions based on piece count and positioning
- Using alpha-beta pruning to reduce computation by eliminating branches
- Default search depth: 4 levels ahead
- Evaluation heuristic considers:
  - Material advantage (piece count)
  - King vs pawn values
  - Board position

**Key Features**:
- Deterministic gameplay
- Strong tactical and strategic play

### Q-Learning (Reinforcement Learning)

The Q-Learning agent learns optimal play through experience:
- **State Representation**: Board configuration encoded as string
- **Action Space**: All possible moves from current position
- **Reward System**:
  - +10 for winning
  - -10 for losing
  - +2 for capturing opponent pieces
  - +1 for king promotion
  - Position-based rewards for strategic advancement
- **Learning Parameters**:
  - Learning rate (α): 0.15
  - Discount factor (γ): 0.95
  - Epsilon decay: From 0.8 to 0.05 over training

**Training Process**:
- Trains against Minimax opponent (depth 2)
- Default: 5000 episodes
- Saves Q-table every 50 episodes
- Tracks win rates and performance metrics

## 🏋️ Training the Q-Learning Agent

To train or improve the Q-Learning agent:

```bash
python3 training.py
```

**Training Configuration**:
- **Episodes**: default 5000
- **Opponent**: Minimax agent with default depth 2
- **Progress Tracking**: Prints statistics every 10 episodes
- **Checkpoints**: Saves Q-table every 50 episodes

**Sample Training Output**:
```
Episode 50/2000 | Winner: Minimax | Moves: 45 | Avg Moves (last 50): 42.3 | Q-Learning Win Rate: 24.0% | Epsilon: 0.760
Saved Q-table checkpoint at episode 50.
...
Training completed!
Q-Learning wins: 654 (32.7%)
Minimax wins: 1298 (64.9%)
Draws: 48 (2.4%)
Average game length: 38.5 moves
```

The trained model is saved to `q_table.json` and automatically loaded when playing against the Q-Learning agent.

## 🔧 Customization

### Adjust Minimax Difficulty

In [play_against_minimax.py](play_against_minimax.py), modify the depth:
```python
minimax = Minimax(depth=4)  # Increase/Decrease depth for harder/weaker opponent
```

### Modify Training Parameters

In [training.py](training.py):
```python
def train(episodes=5000):  # Change episode count
    # ...
    minimax = Minimax(depth=2)  # Adjust opponent strength by adjusting depth
    q_learning = Q_Learning(alpha=0.15, gamma=0.95, epsilon=epsilon)
```

### Change Board Size

In [checkers_env/win_config.py](checkers_env/win_config.py):
```python
WINDOW_SIZE = 800
NO_OF_ROWS = 6  # Change for different board sizes
```

## 📊 Performance

- **Minimax**: Plays at expert level with depth 4 search
- **Q-Learning**: Achieves ~15-20% win rate against Minimax at depth 2 after training
- **Game Length**: Average 35-45 moves per game

---

**Enjoy playing against the AI! 🎮♟️**
