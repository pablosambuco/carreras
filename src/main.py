from .board import Board
from .game import Game

def main():
    board = Board()
    game = Game(board.get_game_length())

    board.draw_game(game)
    game_ended = False
    while not game_ended:
        game_ended = game.step()
        board.draw_game(game)
    board.destroy()

if __name__ == "__main__":
    main()

