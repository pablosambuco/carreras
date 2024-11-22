import sys
import time
import curses


class Game:
    def __init__(self, length):
        self.length = length


class Screen:

    CARD_WIDTH = 6
    CARD_HEIGHT = 3
    EXIT_KEYS = [113]

    ALLOWED_VALUES = {52: 4, 53: 5, 54: 6, 55: 7}

    def __init__(self, stdscr, parent=None):
        self.screen = stdscr
        self.screen.keypad(0)
        self.screen.leaveok(0)
        self.parent = parent
        self.clear()

    def clear(self):
        self.screen.clear()
        self.x_pos = 0
        self.y_pos = 0

    def refresh(self):
        self.screen.refresh()

    def read_key(self, return_list=None):
        while True:
            key = self.screen.getch()
            while key == -1:
                key = self.screen.getch()
                time.sleep(0.1)
            if key in Screen.EXIT_KEYS:
                sys.exit()
            if not return_list:
                return
            if key in return_list:
                return return_list[key]

    def message(self, message, attribs=0):
        self.screen.addstr(self.y_pos, self.x_pos, message, attribs)
        self.refresh()
        self.y_pos += 1

    def addchr(self, y, x, c):
        self.screen.addch(self.y_pos + y, self.x_pos + x, c)

    def addstr(self, y, x, s):
        self.screen.addstr(self.y_pos + y, self.x_pos + x, s)

    def box(self, length, width, color_pair):
        n = length * Screen.CARD_HEIGHT + 2
        m = width * (Screen.CARD_WIDTH + 1) - 2

        window = Screen(self.screen.subwin(n, m, self.y_pos, self.x_pos), self)
        window.screen.attrset(curses.color_pair(color_pair))
        window.screen.box()
        window.screen.attrset(curses.color_pair(0))
        window.x_pos = 1
        window.y_pos = 1
        window.refresh()
        return window

    def card(self, x, y, value, suit=None):

        suits = {
            "golds": {"symbol": "🪙", "color": curses.color_pair(1)},
            "cups": {"symbol": "🍷", "color": curses.color_pair(2)},
            "swords": {"symbol": "⚔", "color": curses.color_pair(3)},
            "clubs": {"symbol": "🌳", "color": curses.color_pair(4)},
        }
        values = {
            10: "🕺",
            11: "🐴",
            12: "👑",
        }

        width = Screen.CARD_WIDTH
        height = Screen.CARD_HEIGHT
        card = Screen(
            self.screen.subwin(height, width, y * height + 3, x * width + 1), self
        )
        card.screen.box()
        card.x_pos = 1
        card.y_pos = 1
        if suit:
            if value in values:
                value = values[value]
            card.message(f"{value}{suits[suit]['symbol']}", suits[suit]["color"])
        else:
            card.message(f"{value}", curses.color_pair(5))
        card.refresh()
        return card

    def move_card(self, x, y):
        self.screen.mvwin(y * Screen.CARD_HEIGHT + 3, x * Screen.CARD_WIDTH + 1)
        self.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    # curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_YELLOW, 0)
    curses.init_pair(2, curses.COLOR_RED, 0)
    curses.init_pair(3, curses.COLOR_CYAN, 0)
    curses.init_pair(4, curses.COLOR_GREEN, 0)
    curses.init_pair(5, curses.COLOR_BLUE, 0)

    screen = Screen(stdscr)
    screen.screen.bkgd(" ")
    # screen.clear()
    screen.message("Presiona Q en cualquier momento para salir del juego")
    screen.message("Presiona 4, 5, 6 o 7 para definir el largo de la carrera")
    length = screen.read_key(Screen.ALLOWED_VALUES)
    game = Game(length)
    window = screen.box(length, 5, 5)
    for i in range(length):
        window.card(0, i, "░░░░")
    h1 = window.card(1, 0, 11, "golds")
    h2 = window.card(2, 0, 11, "cups")
    h3 = window.card(3, 0, 11, "swords")
    h4 = window.card(4, 0, 11, "clubs")
    key = screen.read_key()
    h1.move_card(1, 1)
    key = screen.read_key()
    h1.move_card(1, 2)
    key = screen.read_key()
    h1.move_card(1, 3)
    key = screen.read_key()


if __name__ == "__main__":
    curses.wrapper(main)
