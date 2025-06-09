"""Tests for the Card class."""

from carreras.card import Card

def test_card_initialization():
    """Test Card initialization with suit and value."""
    card = Card("coins", 10)
    assert card.suit == "coins"
    assert card.value == 10

def test_card_equality():
    """Test Card equality and inequality."""
    card1 = Card("coins", 10)
    card2 = Card("coins", 10)
    card3 = Card("cups", 10)
    assert card1 == card2
    assert card1 != card3

def test_card_str_representation():
    """Test string representation of Card."""
    card = Card("coins", 10)
    assert str(card) == "10 of coins"

def test_card_repr_representation():
    """Test repr representation of Card."""
    card = Card("coins", 10)
    assert repr(card) == "10 of coins"

def test_card_match_suit():
    """Test match_suit method of Card."""
    card = Card("coins", 10)
    assert card.match_suit("coins")
    assert not card.match_suit("cups")

