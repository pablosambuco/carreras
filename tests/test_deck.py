from deck import Deck
from card import Card

def test_deck_initialization():
    suits = ["golds", "cups"]
    deck = Deck(suits, 12)
    assert len(deck.cards) == 24
    assert all(isinstance(card, Card) for card in deck.cards)

def test_deck_shuffle():
    suits = ["golds", "cups"]
    deck = Deck(suits, 12)
    original_order = list(deck.cards)
    deck.shuffle()
    assert deck.cards != original_order

def test_get_card():
    deck = Deck(["golds"], 3)
    card = deck.get_card("golds", 2)
    assert card.suit == "golds"
    assert card.value == 2

def test_get_card_pop():
    deck = Deck(["golds"], 3)
    card = deck.get_card()
    assert isinstance(card, Card)
    assert len(deck.cards) == 2

def test_insert_card():
    deck = Deck(["golds"], 3)
    card = Card("golds", 4)
    deck.insert_card(card)
    assert card in deck.cards

