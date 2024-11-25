from typing import Self

class Card:
    JACK = 10
    KNIGHT = 11
    KING = 12

    def __init__(self, suit: str, value: int):
        self.suit = suit
        self.value = value

    def __eq__(self, other: Self) -> bool:
        return self.suit == other.suit and self.value == other.value

    def __str__(self) -> str:
        return f"{self.value} of {self.suit}"

    def __repr__(self) -> str:
        return f"{self.value} of {self.suit}"

    def match_suit(self, suit: str) -> bool:
        return self.suit == suit

