"""Races Game"""

from typing import List
from .deck import Deck


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

    def __init__(
        self,
        players: int = 4,
        length: int = 7,
        players_names: List[str] = None,
    ):
        """
        Initializes a Game object.
        Args:
            board (Board): The game board.
        """
        self.deck = Deck(
            ["golds", "cups", "swords", "clubs"][:players],
            12,
            shuffled=True,
        )
        self.discarded = Deck([],0)
        self.length = length
        self.players = players

        if not players_names:
            players_names = [""] * players
        self.players_names = players_names
        self.knights = {
            (n + 1): {
                "card": self.deck.get_card(suit, 11),
                "row": 0,
                "player": players_names[n],
            }
            for n, suit in enumerate(self.deck.suits)
        }
        self.steps = {
            i
            + 1: {
                "card": self.deck.get_card(),
                "hidden": True,
                "pending": False,
            }
            for i in range(self.length)
        }
        self.min_row = 0
        self.top_card = None

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
        self.min_row = min(knight["row"] for knight in self.knights.values())

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

            if not self.deck.remaining():
                self.deck = self.discarded
                self.deck.shuffle()
                self.discarded = Deck([],0)
            self.top_card = self.deck.get_card()
        else:
            if self.top_card:
                card = self.top_card
                self.discarded.insert_card(card)
                self.move_knights(card.suit, +1)
                self.top_card = None
            if self.min_row and self.steps[self.min_row]["hidden"]:
                self.steps[self.min_row]["hidden"] = False
                self.steps[self.min_row]["pending"] = True
            else:
                if not self.deck.remaining():
                    self.deck = self.discarded
                    self.deck.shuffle()
                    self.discarded = Deck([],0)
                self.top_card = self.deck.get_card()

        return any(knight["row"] > self.length for knight in self.knights.values())
