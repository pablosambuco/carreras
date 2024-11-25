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
    # TODO: Permitir reiniciar el juego
    #  Si ek juego termina, quizas quieran otra partida
    #  asignees: pablosambuco
    #  labels: enhancement 
    board.destroy()

if __name__ == "__main__":
    main()

