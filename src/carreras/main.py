"""Main"""

import argparse

from carreras.board import Board
from carreras.graphicboard import GraphicBoard
from carreras.game import Game


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
    parser = argparse.ArgumentParser(description="CARRERAS - Horse Racing Game")
    parser.add_argument('--gui', action='store_true', help='Usar interfaz gráfica (pygame) en vez de curses')
    args = parser.parse_args()

    if args.gui:
        board = GraphicBoard()
    else:
        board = Board()

    restart = True
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
