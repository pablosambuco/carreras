"""Game of races"""

from sys import exit as sys_exit
from time import sleep
import curses
from random import shuffle
from typing import Self, List, Optional


class Card:
    """
    Represents a single card in a deck.

    Attributes:
        suit (str): The suit of the card (e.g., 'golds', 'cups').
        value (int): The value of the card (1-12).
    """

    JACK = 10
    KNIGHT = 11
    KING = 12

    def __init__(self, suit: str, value: int):
        """
        Initializes a Card object with the given suit and value.

        Args:
            suit (str): The suit of the card.
            value (int): The value of the card.
        """
        self.suit = suit
        self.value = value

    def __eq__(self, other: Self) -> bool:
        """
        Compares this card with another card for equality.

        Args:
            other (Card): The card to compare with.

        Returns:
            bool: True if both cards have the same suit and value, False otherwise.
        """
        return self.suit == other.suit and self.value == other.value

    def __str__(self) -> str:
        """
        Returns a string representation of the card.

        Returns:
            str: The value and suit of the card.
        """
        return f"{self.value} of {self.suit}"

    def __repr__(self) -> str:
        """
        Returns a string representation of the card for debugging.

        Returns:
            str: The value and suit of the card.
        """
        return f"{self.value} of {self.suit}"

    def match_suit(self, suit: str) -> bool:
        """
        Checks if the card's suit matches the given suit.

        Args:
            suit (str): The suit to compare with.

        Returns:
            bool: True if the suits match, False otherwise.
        """
        return self.suit == suit


class Deck:
    """
    Represents a deck of cards.

    Attributes:
        suits (list): A list of suits in the deck.
        cards (list): A list of Card objects in the deck.
    """

    def __init__(self, suits: List[str], q: int, shuffled: bool = False):
        """
        Initializes a Deck object with the given suits and card quantity.

        Args:
            suits (list): A list of suits for the deck.
            q (int): The number of cards per suit.
            shuffled (bool): If True, shuffle the deck after creating it.
        """
        self.suits = suits
        self.cards = [Card(s, v) for v in range(1, q + 1) for s in suits]
        if shuffled:
            self.shuffle()

    def shuffle(self):
        """
        Shuffles the cards in the deck.
        """
        shuffle(self.cards)

    def get_card(
        self, suit: Optional[str] = None, value: Optional[int] = None
    ) -> Optional[Card]:
        """
        Retrieves a card from the deck.

        Args:
            suit (str, optional): The suit of the card to retrieve. Defaults to None.
            value (int, optional): The value of the card to retrieve. Defaults to None.

        Returns:
            Card: The retrieved card, or None if the card is not found.
        """
        if not suit or not value:
            return self.cards.pop()
        aux = Card(suit, value)
        if aux in self.cards:
            self.cards.remove(aux)
            return aux
        return None

    def insert_card(self, card: Card):
        """
        Inserts a card back into the deck.

        Args:
            card (Card): The card to insert.
        """
        if card not in self.cards:
            self.cards.append(card)


class Board:
    """
    Represents the game board.

    Attributes:
        CARD_WIDTH (int): The width of a card.
        CARD_HEIGHT (int): The height of a card.
        EXIT_KEYS (list): Keys to exit the game.
        ALLOWED_VALUES (dict): Allowed values for the game length.
        screen: The screen object for displaying the game.
        parent: The parent board, if any.
    """

    CARD_WIDTH = 6
    CARD_HEIGHT = 3
    EXIT_KEYS = [113]

    ALLOWED_VALUES = {52: 4, 53: 5, 54: 6, 55: 7}

    def __init__(self, stdscr, parent: Optional[Self] = None):
        """
        Initializes a Board object.

        Args:
            stdscr: The standard screen object.
            parent (Board, optional): The parent board. Defaults to None.
        """
        self.screen = stdscr
        self.screen.keypad(0)
        self.screen.leaveok(0)
        self.parent = parent
        self.clear()

    def clear(self):
        """
        Clears the screen.
        """
        self.screen.clear()
        self.x_pos = 0
        self.y_pos = 0

    def refresh(self):
        """
        Refreshes the screen.
        """
        self.screen.refresh()

    def read_key(self, return_list: Optional[dict] = None) -> Optional[int]:
        """
        Reads a key input from the user.

        Args:
            return_list (dict, optional): A dictionary of allowed keys and their return values. Defaults to None.

        Returns:
            The value corresponding to the key pressed.
        """
        while True:
            key = self.screen.getch()
            while key == -1:
                key = self.screen.getch()
                sleep(0.1)
            if key in Board.EXIT_KEYS:
                sys_exit()
            if not return_list:
                return
            if key in return_list:
                return return_list[key]

    def message(self, message: str, attribs: int = 0):
        """
        Displays a message on the board.

        Args:
            message (str): The message to display.
            attribs (int, optional): The attributes for the message. Defaults to 0.
        """
        self.screen.addstr(self.y_pos, self.x_pos, message, attribs)
        self.refresh()
        self.y_pos += 1

    def add_char(self, y: int, x: int, c: str):
        """
        Adds a character to the board at the specified position.

        Args:
            y (int): The y-coordinate.
            x (int): The x-coordinate.
            c (str): The character to add.
        """
        self.screen.addch(self.y_pos + y, self.x_pos + x, c)

    def add_string(self, y: int, x: int, s: str):
        """
        Adds a string to the board at the specified position.

        Args:
            y (int): The y-coordinate.
            x (int): The x-coordinate.
            s (str): The string to add.
        """
        self.screen.addstr(self.y_pos + y, self.x_pos + x, s)

    def get_game_length(self) -> int:
        """
        Prompts the user to select the game length.

        Returns:
            int: The selected game length.
        """
        self.screen.bkgd(" ")
        self.message("Presiona Q en cualquier momento para salir del juego")
        self.message("Presiona 4, 5, 6 o 7 para definir el largo de la carrera")
        return self.read_key(Board.ALLOWED_VALUES)

    def draw_box(
        self,
        length: int,
        width: int,
        y: Optional[int] = None,
        x: Optional[int] = None,
        color_pair: Optional[int] = None,
    ) -> Self:
        """
        Draws a box on the board.

        Args:
            length (int): The length of the box.
            width (int): The width of the box.
            y (int, optional): The y-coordinate. Defaults to None.
            x (int, optional): The x-coordinate. Defaults to None.
            color_pair (int, optional): The color pair for the box. Defaults to None.

        Returns:
            Board: A new Board object representing the drawn box.
        """
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

    def draw_card(self, x: int, y: int, value: int, suit: Optional[str] = None) -> Self:
        """
        Draws a card on the board.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.
            value (int or str): The value of the card or back fill character
            suit (str, optional): The suit of the card. Defaults to None.

        Returns:
            Board: A new Board object representing the drawn card.
        """
        suits = {
            "golds": {"symbol": "🪙", "color": curses.color_pair(1)},
            "cups": {"symbol": "🍷", "color": curses.color_pair(2)},
            "swords": {"symbol": "⚔", "color": curses.color_pair(3)},
            "clubs": {"symbol": "🌳", "color": curses.color_pair(4)},
        }
        values = {
            Card.JACK: "🕺",
            Card.KNIGHT: "🐴",
            Card.KING: "👑",
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


class Game:
    """
    Represents a races game.

    Attributes:
        deck (Deck): The deck of cards used in the game.
        board (Board): The game board.
        length (int): The length of the game.
        knights (dict): The knights in the game.
        steps (dict): The steps in the game.
        min_row (int): The minimum row value among the knights.
        top_card (Card): The top card in the deck.
    """

    def __init__(self, board: Board):
        """
        Initializes a Game object.

        Args:
            board (Board): The game board.
        """
        self.deck = Deck(["golds", "cups", "swords", "clubs"], 12, shuffled=True)
        self.board = board
        self.length = board.get_game_length()
        self.knights = {
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
        """
        Draws the game board.
        """
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
        for n, knight in self.knights.items():
            box.draw_card(n, knight["row"], knight["card"].value, knight["card"].suit)
        self.board.read_key()

    def print_status(self):
        """
        Prints the current status of the game.
        """
        print(self.knights)
        print(self.steps)

    def move_knights(self, suit: str, step: int):
        """
        Moves the knights based on the suit and step value.

        Args:
            suit (str): The suit of the card.
            step (int): The step value.
        """
        for knight in self.knights.values():
            if knight["card"].match_suit(suit):
                knight["row"] += step
        self.min_row = min([knight["row"] for knight in self.knights.values()])

    def step(self) -> bool:
        """
        Executes a step in the game.

        Returns:
            bool: True if the game has ended, False otherwise.
        """
        if self.min_row and self.steps[self.min_row]["pending"]:
            self.steps[self.min_row]["pending"] = False
            card = self.steps[self.min_row]["card"]
            self.move_knights(card.suit, -1)
            self.top_card = self.deck.get_card()
        else:
            if self.top_card:
                card = self.top_card
                self.move_knights(card.suit, +1)
                self.top_card = None
            if self.min_row and self.steps[self.min_row]["hidden"]:
                self.steps[self.min_row]["hidden"] = False
                self.steps[self.min_row]["pending"] = True
            else:
                self.top_card = self.deck.get_card()

        return any([knight["row"] > self.length for knight in self.knights.values()])


def main(stdscr):
    """
    The main function to run the game.

    Args:
        stdscr: The standard screen object.
    """
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
