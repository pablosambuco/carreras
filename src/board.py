"""Races Game Board curses implementation"""

from typing import Optional, Self
from .game import Game
from .card import Card
import curses
import sys
from time import sleep

# TODO: Agregar menü a la derecha
# Issue URL: https://github.com/pablosambuco/carreras/issues/7
#  Se debe construir un recuadro a la derecha del box principal
#  labels: enhancement
#  assignees: pablosambuco


class Board:
    """
    Represents the game board.

    Attributes:
        CARD_WIDTH (int): The width of a card.
        CARD_HEIGHT (int): The height of a card.
        EXIT_KEYS (list): Keys to exit the game.
        LENGTH_VALUES (dict): Allowed values for the game length.
        PLAYER_VALUES (dict): Allowed values for the playes.
        screen: The screen object for displaying the game.
        parent: The parent board, if any.
    """

    CARD_WIDTH = 6
    CARD_HEIGHT = 3
    EXIT_KEYS = [113]

    LENGTH_VALUES = {52: 4, 53: 5, 54: 6, 55: 7}
    PLAYER_VALUES = {50: 2, 51: 3, 52: 4}

    def __init__(
        self,
        stdscr: Optional[curses.window] = None,
        parent: Optional[Self] = None,
    ):
        """
        Initializes a Board object.

        Args:
            parent (Board, optional): The parent board. Defaults to None.
        """

        if not stdscr:
            stdscr = curses.initscr()
            curses.curs_set(0)
            curses.start_color()
            curses.init_pair(1, curses.COLOR_YELLOW, 0)
            curses.init_pair(2, curses.COLOR_RED, 0)
            curses.init_pair(3, curses.COLOR_CYAN, 0)
            curses.init_pair(4, curses.COLOR_GREEN, 0)
            curses.init_pair(5, curses.COLOR_BLUE, 0)

        self.screen = stdscr
        self.screen.keypad(0)
        self.screen.leaveok(0)
        self.parent = parent

        self.x_pos = 0
        self.y_pos = 0

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
            return_list (dict, optional): A dictionary of allowed keys and their
                return values. Defaults to None.

        Returns:
            The value corresponding to the key pressed.
        """
        while True:
            key = self.screen.getch()
            while key == -1:
                key = self.screen.getch()
                sleep(0.1)
            if key in Board.EXIT_KEYS:
                self.destroy()
                sys.exit()
            if not return_list:
                return
            if key in return_list:
                return return_list[key]

    def destroy(self):
        """
        Ends the curses window
        """
        curses.endwin()

    def message(self, message: str, attribs: int = 0):
        """
        Displays a message on the board.

        Args:
            message (str): The message to display.
            attribs (int, optional): The attributes for the message.
                Defaults to 0.
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

    def get_game_params(self) -> int:
        """
        Prompts the user to select the game players and length.

        Returns:
            int: The selected players
            int: The selected game length.
        """
        self.message("Presiona Q en cualquier momento para salir del juego")
        self.message("Presiona 2, 3 o 4 para definir la cantidad de jugadores: ")
        players = self.read_key(Board.PLAYER_VALUES)
        self.message("Presiona 4, 5, 6 o 7 para definir el largo de la carrera: ")
        length = self.read_key(Board.LENGTH_VALUES)
        self.read_key()
        return players, length

    def draw_box(
        self,
        length: int,
        width: int,
        y: Optional[int] = None,
        x: Optional[int] = None,
        color_pair: Optional[int] = 0,
    ) -> Self:
        """
        Draws a box on the board.

        Args:
            length (int): The length of the box.
            width (int): The width of the box.
            y (int, optional): The y-coordinate. Defaults to None.
            x (int, optional): The x-coordinate. Defaults to None.
            color_pair (int, optional): The color pair for the box.
                0 by default

        Returns:
            Board: A new Board object representing the drawn box.
        """
        if not y:
            y = self.y_pos
        if not x:
            x = self.x_pos

        window = Board(self.screen.subwin(length, width, y, x), self)
        window.screen.attrset(curses.color_pair(color_pair))
        window.screen.box()
        window.screen.attrset(curses.color_pair(0))
        window.x_pos = 1
        window.y_pos = 1
        window.refresh()
        return window

    def draw_card(
        self,
        x: int,
        y: int,
        value: int,
        suit: Optional[str] = None,
    ) -> Self:
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
            self.screen.subwin(height, width, y * height + 1, x * width + 1),
            self,
        )
        card.screen.box()
        card.x_pos = 1
        card.y_pos = 1
        if suit:
            if value in values:
                value = values[value]
            card.message(
                f"{value}{suits[suit]['symbol']}",
                suits[suit]["color"],
            )
        else:
            card.message(f"{value}", curses.color_pair(5))
        card.refresh()
        return card

    def draw_game(self, game: Game):
        """
        Draws the game board.
        """
        self.clear()
        lateral = self.draw_box(
            (game.length + 2) * Board.CARD_HEIGHT + 2,
            2 * (Board.CARD_WIDTH + 1),
            0,
            (game.players + 1) * (Board.CARD_WIDTH) + 2,
            color_pair=0,
        )
        # title = lateral.draw_box(
        #    # Board.CARD_HEIGHT,
        #    # (Board.CARD_WIDTH + 1) - 2,
        #    4,
        #    4,
        #    color_pair=2,
        # )
        # title.message(f"{'Carrera!':^{Board.CARD_WIDTH*2}}")
        # menu = lateral.draw_box(
        #    (game.length +1) * Board.CARD_HEIGHT,
        #    2 * (Board.CARD_WIDTH + 1) - 2,
        #    Board.CARD_HEIGHT + 1,
        #    1,
        #    color_pair = 4
        # )
        # menu.message("Q - Salir")
        box = self.draw_box(
            (game.length + 2) * Board.CARD_HEIGHT + 2,
            (game.players + 1) * (Board.CARD_WIDTH) + 2,
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
        finish.message(f"{'FINISH':^{Board.CARD_WIDTH*(game.players)-3}}")

        if game.top_card is None:
            box.draw_card(0, 0, "░░░░")
        else:
            box.draw_card(0, 0, game.top_card.value, game.top_card.suit)
        for n, step in game.steps.items():
            if step["hidden"]:
                box.draw_card(0, n, "░░░░")
            else:
                box.draw_card(0, n, step["card"].value, step["card"].suit)
        for n, knight in game.knights.items():
            box.draw_card(
                n,
                knight["row"],
                knight["card"].value,
                knight["card"].suit,
            )
        self.read_key()
