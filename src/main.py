"""Main"""
from .board import Board
from .game import Game

def main():
    board = Board()
    players, length = board.get_game_params()
    game = Game(players, length)

    board.draw_game(game)
    game_ended = False
    while not game_ended:
        game_ended = game.step()
        board.draw_game(game)
    # TODO: Permitir reiniciar el juego
    # Issue URL: https://github.com/pablosambuco/carreras/issues/10
    #  Si ek juego termina, quizas quieran otra partida
    #  asignees: pablosambuco
    #  labels: enhancement 
    board.destroy()

if __name__ == "__main__":
    main()

