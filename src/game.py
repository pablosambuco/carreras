from .deck import Deck
from .card import Card

# TODO: Permitir eleccion de jugadores
# Issue URL: https://github.com/pablosambuco/carreras/issues/8
#  Se puede jugar de 2 a 4 jugadores. En caso de ser menos que 4, se deben descartar los palos que sobran
#  labels: enhancement
#  assignees: pablosambuco


# TODO: Permitir a los jugadores ingresar su nombre
#  Los jugadores podrán tener un nombre y se les asignará un palo de la baraja
#  labels: enhancement
#  assignees: pablosambuco

class Game:
    def __init__(self, length: int):
        self.deck = Deck(["golds", "cups", "swords", "clubs"], 12, shuffled=True)
        self.length = length
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

    def print_status(self):
        print(self.knights)
        print(self.steps)

    def move_knights(self, suit: str, step: int):
        for knight in self.knights.values():
            if knight["card"].match_suit(suit):
                knight["row"] += step
        self.min_row = min([knight["row"] for knight in self.knights.values()])

    def step(self) -> bool:
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

