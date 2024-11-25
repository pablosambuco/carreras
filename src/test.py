"""Main"""
from .board import Board
from .game import Game

def main():
    board = Board()
    players = 4
    length = 4
    players_names = ["P","S","D","E"] 
    game = Game(players, length, players_names)

    board.draw_game(game)
    board.destroy()

if __name__ == "__main__":
    main()

