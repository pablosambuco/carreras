"""Main"""

from .board import Board
from .game import Game
import curses


def main():
    board = Board()
    game = Game(4, 4, ["Ppppppp", "Ssss", "Dddddddddddd", "Ee"])
    board.draw_game(game)
    game = Game(
        3,
        7,
        [
            "Paaeeeeeed",
            "Sasdasdasd",
            "Xyzxyzxyz",
        ],
    )
    for _ in range(10):
        board.draw_game(game)
        game.step()
    board.destroy()


def main2(stdscr):
    curses.curs_set(0)
    curses.start_color()
    sc1 = stdscr
    sc1.box()
    sc2 = sc1.derwin(25, 25, 2, 2)
    sc2.box()
    sc3 = sc2.derwin(20, 20, 2, 2)
    sc3.box()
    sc4 = sc3.derwin(15, 15, 2, 2)
    sc4.box()
    sc5 = sc4.derwin(10, 10, 2, 2)
    sc5.box()
    sc1.getkey()

def main3():
    game = Game(2, 7, ["a", "b"])
    game_ended = False
    while not game_ended:
        game_ended = game.step()

if __name__ == "__main__":
    main3()
