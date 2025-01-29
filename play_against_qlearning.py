import pygame
import os
import csv
import random
from checkers_env.win_config import Win_Config
from checkers_env.piece import Piece
from checkers_env.game import Game

Q_TABLE_FILE = "q_table.csv"
EPSILON = 0.1  # Exploration rate

window = pygame.display.set_mode((Win_Config.WINDOW_SIZE, Win_Config.WINDOW_SIZE))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // Win_Config.SQUARE_SIZE
    col = x // Win_Config.SQUARE_SIZE
    return row, col

def load_q_table(file: str) -> dict:
    """Load Q-table from CSV file."""
    q_table = {}
    if os.path.exists(file):
        with open(file, mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                state, action, value = row
                if state not in q_table:
                    q_table[state] = {}
                q_table[state][eval(action)] = float(value)
    return q_table

def choose_best_action(q_table, state, valid_moves):
    """Choose the best action from the Q-table or explore randomly."""
    if state in q_table and random.random() > EPSILON:
        best_action = max(q_table[state], key=q_table[state].get, default=None)
        if best_action in valid_moves:
            return best_action
    return random.choice(list(valid_moves.keys())) if valid_moves else None

def ai_move(game, q_table):
    """Make a move for the AI using the Q-table."""
    state = game.get_board().encode()
    valid_moves = {}
    
    for piece in game.board.get_all_pieces(Piece.P1):
        moves = game.board.get_actions(piece)
        for move in moves:
            valid_moves[(piece.row, piece.col, move[0], move[1])] = (piece, move)
    
    action = choose_best_action(q_table, state, valid_moves)
    if action:
        piece, move = valid_moves[action]
        game.selected_piece = piece
        game._move(*move)

def main():
    pygame.init()
    game = Game(window)
    clock = pygame.time.Clock()
    run = True
    q_table = load_q_table(Q_TABLE_FILE)
    
    while run and game.winner() is None:
        clock.tick(Win_Config.FPS)
        
        if game.player == Piece.P1:
            ai_move(game, q_table)
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select_piece(row, col)
            
            if event.type == pygame.QUIT:
                run = False
                
        game.update()
    
    pygame.quit()

if __name__ == '__main__':
    main()
