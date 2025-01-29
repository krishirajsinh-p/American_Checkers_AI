import pygame
from checkers_env.win_config import Win_Config
from checkers_env.piece import Piece
from checkers_env.game import Game
from checkers_env.minimax import minimax

window = pygame.display.set_mode((Win_Config.WINDOW_SIZE, Win_Config.WINDOW_SIZE))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // Win_Config.SQUARE_SIZE
    col = x // Win_Config.SQUARE_SIZE
    return row, col

def main():
    game = Game(window)
    clock = pygame.time.Clock()
    run = True
    while run and game.winner() == None:
        clock.tick(Win_Config.FPS)

        if game.player == Piece.P1:
            _, new_board = minimax(game.get_board(), 4, float('-inf'), float('inf'), True)
            game.AI_action(new_board)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select_piece(row, col)

            if event.type == pygame.QUIT:
                run = False
            
        game.update()
    pygame.quit()
    print(game)

if __name__ == '__main__':
    main()