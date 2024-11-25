"""Card"""

from typing import Self


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
