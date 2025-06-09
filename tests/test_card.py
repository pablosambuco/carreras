from carreras.card import Card

def test_card_initialization():
    card = Card("coins", 10)
    assert card.suit == "coins"
    assert card.value == 10

def test_card_equality():
    card1 = Card("coins", 10)
    card2 = Card("coins", 10)
    card3 = Card("cups", 10)
    assert card1 == card2
    assert card1 != card3

def test_card_str_representation():
    card = Card("coins", 10)
    assert str(card) == "10 of coins"

def test_card_repr_representation():
    card = Card("coins", 10)
    assert repr(card) == "10 of coins"

def test_card_match_suit():
    card = Card("coins", 10)
    assert card.match_suit("coins")
    assert not card.match_suit("cups")

