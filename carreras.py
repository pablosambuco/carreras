import sys
import time
import curses

CARD_WIDTH=6
CARD_HEIGHT=3

def read_key(stdscr, quit_list, return_list):
    while True:
        key = stdscr.getch()
        while key == -1:
            key = stdscr.getch()
            time.sleep(0.1)
        if key in quit_list:
            sys.exit()
        if key in return_list or not return_list:
            return key


def draw_box(stdscr, length, width):
    n = length * CARD_HEIGHT + 2
    m = width * (CARD_WIDTH + 1) - 2
    for i in range(n):
        for j in range(m):
            if i in (0, n - 1):
                stdscr.addch(i, j, "-")
            elif j in (0, m - 1):
                stdscr.addch(i, j, "|")
            else:
                stdscr.addch(i, j, " ")
    stdscr.refresh()


def draw_card(stdscr, x, y, value, suit):
    width = CARD_WIDTH
    height = CARD_HEIGHT

    for i in range((x - 1) * height + 1, x * height + 1):
        for j in range((y - 1) * width + 1, y * width + 1):
            if i in ((x - 1) * height + 1, x * height):
                stdscr.addch(i, j, "-")
            elif j in ((y - 1) * width + 1, y * width):
                stdscr.addch(i, j, "|")
            else:
                stdscr.addch(i, j, " ")
    stdscr.addstr((x - 1) * height + 2, (y - 1) * width + 2, f"{value:02} {suit}")


def main(stdscr):
    stdscr.clear()
    stdscr.addstr(1, 0, "Presiona Q en cualquier momento para salir del juego")
    stdscr.addstr(2, 0, "Presiona 4, 5, 6 o 7 para definir el largo de la carrera")
    stdscr.refresh()
    key = read_key(stdscr, [113], [52, 53, 54, 55])
    length = key - 48
    stdscr.clear()
    draw_box(stdscr, length, 5)
    draw_card(stdscr, 1, 2, 11, "o")
    draw_card(stdscr, 1, 3, 11, "u")
    draw_card(stdscr, 1, 4, 11, "/")
    draw_card(stdscr, 1, 5, 11, "⊥")
    key = read_key(stdscr, [113], [])


if __name__ == "__main__":
    curses.wrapper(main)
