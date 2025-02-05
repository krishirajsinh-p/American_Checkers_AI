import pygame
from checkers_env.win_config import Win_Config
from checkers_env.piece import Piece
from checkers_env.game import Game
from algorithm.minimax import Minimax

def main():
    window = pygame.display.set_mode((Win_Config.WINDOW_SIZE, Win_Config.WINDOW_SIZE))
    pygame.display.set_caption('Checkers Game - Play against Minimax Algorithm')
    clock = pygame.time.Clock()
    
    game = Game(window)
    minimax = Minimax()
    
    run = True
    while run and game.winner() is None:
        clock.tick(Win_Config.FPS)

        if game.current_player == Piece.P2:
            game.AI_move(minimax.get_best_action(game.board))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = game.mouse_pos_to_board_pos(pygame.mouse.get_pos())
                game.select_pos(row, col)

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
            
        game.update()
    
    pygame.quit()

if __name__ == '__main__':
    main()
