from random import shuffle
from typing import List, Optional
from .card import Card

class Deck:
    def __init__(self, suits: List[str], q: int, shuffled: bool = False):
        self.suits = suits
        self.cards = [Card(s, v) for v in range(1, q + 1) for s in suits]
        if shuffled:
            self.shuffle()

    def shuffle(self):
        shuffle(self.cards)

    def get_card(self, suit: Optional[str] = None, value: Optional[int] = None) -> Optional[Card]:
        if not suit or not value:
            return self.cards.pop()
        aux = Card(suit, value)
        if aux in self.cards:
            self.cards.remove(aux)
            return aux
        return None

    def insert_card(self, card: Card):
        if card not in self.cards:
            self.cards.append(card)

