import sys
import time
import curses
import random


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value

    def __str__(self):
        return f"{self.value} of {self.suit}"

    def __repr__(self):
        return f"{self.value} of {self.suit}"

    def match_suit(self, suit):
        return self.suit == suit


class Deck:
    def __init__(self, suits, q, shuffled=False):
        self.suits = suits
        self.cards = [Card(s, v) for v in range(1, q + 1) for s in suits]
        if shuffled:
            self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def get_card(self, suit=None, value=None):
        if not suit or not value:
            return self.cards.pop()
        aux = Card(suit, value)
        if aux in self.cards:
            self.cards.remove(aux)
            return aux
        return None

    def insert_card(self, card):
        if card not in self.cards:
            self.cards.append(card)


class Game:
    def __init__(self, board):
        self.deck = Deck(["golds", "cups", "swords", "clubs"], 12, shuffled=True)
        self.board = board
        self.length = board.get_game_length()
        self.horses = {
            n + 1: {"card": self.deck.get_card(suit, 11), "row": 0}
            for n, suit in enumerate(self.deck.suits)
        }
        self.steps = {
            i + 1: {"card": self.deck.get_card(), "hidden": True, "pending": False}
            for i in range(self.length)
        }
        self.min_row = 0
        self.top_card = None

    def draw_game(self): 
        # TODO: Move to Board.
        #  Game should be agnostic of the final representation
        self.board.clear()
        box = self.board.draw_box(
            (self.length + 2) * Board.CARD_HEIGHT + 2,
            5 * (Board.CARD_WIDTH + 1) - 2,
            color_pair=5,
        )
        finish_y, finish_x = box.screen.getmaxyx()
        finish = box.draw_box(
            Board.CARD_HEIGHT,
            finish_x - Board.CARD_WIDTH - 2,
            finish_y - Board.CARD_HEIGHT - 1,
            Board.CARD_WIDTH + 1,
            4,
        )
        finish.message(f"{'FINISH':^{Board.CARD_WIDTH*4-2}}")

        if self.top_card is None:
            box.draw_card(0, 0, "░░░░")
        else:
            box.draw_card(0, 0, self.top_card.value, self.top_card.suit)
        for n, step in self.steps.items():
            if step["hidden"]:
                box.draw_card(0, n, "░░░░")
            else:
                box.draw_card(0, n, step["card"].value, step["card"].suit)
        for n, horse in self.horses.items():
            box.draw_card(n, horse["row"], horse["card"].value, horse["card"].suit)
        self.board.read_key()

    def print_status(self):
        print(self.horses)
        print(self.steps)

    def move_horses(self, suit, step):
        for horse in self.horses.values():
            if horse["card"].match_suit(suit):
                horse["row"] += step
        self.min_row = min([horse["row"] for horse in self.horses.values()])

    def step(self):
        if self.min_row and self.steps[self.min_row]["pending"]:
            self.steps[self.min_row]["pending"] = False
            card = self.steps[self.min_row]["card"]
            self.move_horses(card.suit, -1)
            self.top_card = self.deck.get_card()
        else:
            if self.top_card:
                card = self.top_card
                self.move_horses(card.suit, +1)
                self.top_card = None
            if self.min_row and self.steps[self.min_row]["hidden"]:
                self.steps[self.min_row]["hidden"] = False
                self.steps[self.min_row]["pending"] = True
            else:
                self.top_card = self.deck.get_card()

        return any([horse["row"] > self.length for horse in self.horses.values()])


class Board:

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
            if key in Board.EXIT_KEYS:
                sys.exit()
            if not return_list:
                return
            if key in return_list:
                return return_list[key]

    def message(self, message, attribs=0):
        self.screen.addstr(self.y_pos, self.x_pos, message, attribs)
        self.refresh()
        self.y_pos += 1

    def add_char(self, y, x, c):
        self.screen.addch(self.y_pos + y, self.x_pos + x, c)

    def add_string(self, y, x, s):
        self.screen.addstr(self.y_pos + y, self.x_pos + x, s)

    def get_game_length(self):
        self.screen.bkgd(" ")
        self.message("Presiona Q en cualquier momento para salir del juego")
        self.message("Presiona 4, 5, 6 o 7 para definir el largo de la carrera")
        return self.read_key(Board.ALLOWED_VALUES)

    def draw_box(self, length, width, y=None, x=None, color_pair=None):
        if not y:
            y = self.y_pos
        if not x:
            x = self.x_pos
        if not color_pair:
            color_pair = 0

        window = Board(self.screen.subwin(length, width, y, x), self)
        window.screen.attrset(curses.color_pair(color_pair))
        window.screen.box()
        window.screen.attrset(curses.color_pair(0))
        window.x_pos = 1
        window.y_pos = 1
        window.refresh()
        return window

    def draw_card(self, x, y, value, suit=None):
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

        width = Board.CARD_WIDTH
        height = Board.CARD_HEIGHT
        card = Board(
            self.screen.subwin(height, width, y * height + 1, x * width + 1), self
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
        self.screen.mvwin(y * Board.CARD_HEIGHT + 3, x * Board.CARD_WIDTH + 1)
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

    board = Board(stdscr)
    game = Game(board)
    game.draw_game()
    game_ended = False
    while not game_ended:
        game_ended = game.step()
        game.draw_game()


if __name__ == "__main__":
    curses.wrapper(main)
