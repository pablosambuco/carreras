"""Main"""

from .board import Board
from .game import Game


def iniciar_juego(
    board: Board,
    players: int,
    length: int,
    players_names: list[str],
) -> Game:
    game = Game(players, length, players_names)
    board.draw_game(game)
    return game


def main():
    restart = True
    board = Board()
    players, length, players_names = board.get_game_params()
    while restart:
        game = iniciar_juego(board, players, length, players_names)
        game_ended = False
        while not game_ended:
            game_ended = game.step()
            board.draw_game(game)
        restart, same_params = board.ask_restart()
        if restart and not same_params:
            players, length, players_names = board.get_game_params()
    board.destroy()


if __name__ == "__main__":
    main()
