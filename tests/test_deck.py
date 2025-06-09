"""Tests for the Deck class."""

from carreras.deck import Deck
from carreras.card import Card

def test_deck_initialization():
    """Test Deck initialization with suits and card count."""
    suits = ["coins", "cups"]
    deck = Deck(suits, 12)
    assert len(deck.cards) == 24
    assert all(isinstance(card, Card) for card in deck.cards)

def test_deck_shuffle():
    """Test Deck shuffling changes card order."""
    suits = ["coins", "cups"]
    deck = Deck(suits, 12)
    original_order = list(deck.cards)
    deck.shuffle()
    assert deck.cards != original_order

def test_get_card():
    """Test getting a specific card from the Deck."""
    deck = Deck(["coins"], 3)
    card = deck.get_card("coins", 2)
    assert card.suit == "coins"
    assert card.value == 2

def test_get_card_pop():
    """Test popping a card from the Deck."""
    deck = Deck(["coins"], 3)
    card = deck.get_card()
    assert isinstance(card, Card)
    assert len(deck.cards) == 2

def test_insert_card():
    """Test inserting a card into the Deck."""
    deck = Deck(["coins"], 3)
    card = Card("coins", 4)
    deck.insert_card(card)
    assert card in deck.cards

