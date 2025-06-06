"""Deck"""

from random import shuffle
from typing import List, Optional
from card import Card


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

    def remaining(self) -> int:
        return len(self.cards)

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
